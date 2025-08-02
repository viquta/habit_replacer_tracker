"""
Database Access Layer for Habit Tracker Application
Handles all database operations using the DAO pattern
"""
import pyodbc
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from contextlib import contextmanager
import sys
import os

# Add the parent directory to the path to import db_connection
db_scripts_path = os.path.join(os.path.dirname(__file__), '..', 'backend_and_DB_setup', 'mssql-express', 'scripts')
if db_scripts_path not in sys.path:
    sys.path.insert(0, db_scripts_path)

try:
    from db_connection import get_connection  # type: ignore
except ImportError:
    # Fallback if db_connection is not available
    def get_connection():
        """Fallback connection function"""
        raise ImportError("Database connection module not found. Please ensure SQL Server is set up.")

from backend.models import (
    User, Habit, HabitCompletion, HabitPeriod, 
    HabitNotFoundException, UserNotFoundException, DatabaseException
)


class BaseDAO:
    """Base Data Access Object with common database operations"""
    
    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        connection = None
        try:
            connection = get_connection()
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            raise DatabaseException(f"Database operation failed: {str(e)}")
        finally:
            if connection:
                connection.close()


class UserDAO(BaseDAO):
    """Data Access Object for User operations"""
    
    def create_user(self, user: User) -> int:
        """Create a new user and return the user ID"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # Use OUTPUT clause to get the identity value directly
                cursor.execute("""
                    INSERT INTO Users (Username, PasswordHash, Email, CreatedAt)
                    OUTPUT INSERTED.UserID
                    VALUES (?, ?, ?, ?)
                """, user.username, user.password_hash, user.email, user.created_at)
                
                result = cursor.fetchone()
                
                if not result or result[0] is None:
                    raise DatabaseException("Failed to get identity value from OUTPUT clause - insert may have failed")
                
                user_id = result[0]
                
                # OUTPUT clause typically returns int directly, but handle edge cases
                if not isinstance(user_id, int):
                    try:
                        if hasattr(user_id, '__int__'):
                            user_id = int(user_id)
                        elif user_id is not None:
                            user_id = int(float(user_id))
                        else:
                            raise DatabaseException("Identity value is None - insert failed")
                    except (ValueError, TypeError) as e:
                        raise DatabaseException(f"Failed to convert identity value to integer: {str(e)}")
                
                conn.commit()
                return user_id
                
            except pyodbc.Error as e:
                conn.rollback()
                raise DatabaseException(f"Database error during user creation: {str(e)}")
            except Exception as e:
                conn.rollback()
                raise DatabaseException(f"Unexpected error during user creation: {str(e)}")
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT UserID, Username, PasswordHash, Email, CreatedAt
                FROM Users WHERE UserID = ?
            """, user_id)
            
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row[0],
                    username=row[1],
                    password_hash=row[2],
                    email=row[3],
                    created_at=row[4]
                )
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT UserID, Username, PasswordHash, Email, CreatedAt
                FROM Users WHERE Username = ?
            """, username)
            
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row[0],
                    username=row[1],
                    password_hash=row[2],
                    email=row[3],
                    created_at=row[4]
                )
            return None


class HabitDAO(BaseDAO):
    """Data Access Object for Habit operations"""
    #essential habit method (keep this)
    def create_habit(self, habit: Habit) -> int:
        """Create a new habit and return the habit ID"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # Use OUTPUT clause to get the identity value directly
                cursor.execute("""
                    INSERT INTO Habits (UserID, HabitName, Description, Period, CreatedDate, IsActive, CreatedAt)
                    OUTPUT INSERTED.HabitID
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, habit.user_id, habit.habit_name, habit.description, 
                   habit.period.value, habit.created_date, habit.is_active, habit.created_at)
                
                result = cursor.fetchone()
                
                if not result or result[0] is None:
                    raise DatabaseException("Failed to get identity value from OUTPUT clause - insert may have failed")
                
                # Extract the habit ID from the result to then send to habit service
                habit_id = result[0]
                
                # OUTPUT clause typically returns int directly, but handle edge cases
                if not isinstance(habit_id, int):
                    try:
                        if hasattr(habit_id, '__int__'):
                            habit_id = int(habit_id)
                        elif habit_id is not None:
                            habit_id = int(float(habit_id))
                        else:
                            raise DatabaseException("Identity value is None - insert failed")
                    except (ValueError, TypeError) as e:
                        raise DatabaseException(f"Failed to convert identity value to integer: {str(e)}")
                
                conn.commit()
                return habit_id
                
            except pyodbc.Error as e:
                conn.rollback()
                raise DatabaseException(f"Database error during habit creation: {str(e)}")
            except Exception as e:
                conn.rollback()
                raise DatabaseException(f"Unexpected error during habit creation: {str(e)}")
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Habit]:
        """Get habit by ID"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT HabitID, UserID, HabitName, Description, Period, CreatedDate, IsActive, CreatedAt
                FROM Habits WHERE HabitID = ?
            """, habit_id)
            
            row = cursor.fetchone()
            if row:
                return Habit(
                    habit_id=row[0],
                    user_id=row[1],
                    habit_name=row[2],
                    description=row[3],
                    period=HabitPeriod(row[4]),
                    created_date=row[5],
                    is_active=row[6],
                    created_at=row[7]
                )
            return None
    
    def get_habits_by_user_id(self, user_id: int, active_only: bool = True) -> List[Habit]:
        """Get all habits for a user"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT HabitID, UserID, HabitName, Description, Period, CreatedDate, IsActive, CreatedAt
                FROM Habits WHERE UserID = ?
            """
            params = [user_id]
            
            if active_only:
                query += " AND IsActive = 1"
            
            query += " ORDER BY CreatedAt DESC"
            
            cursor.execute(query, params)
            
            habits = []
            for row in cursor.fetchall():
                habits.append(Habit(
                    habit_id=row[0],
                    user_id=row[1],
                    habit_name=row[2],
                    description=row[3],
                    period=HabitPeriod(row[4]),
                    created_date=row[5],
                    is_active=row[6],
                    created_at=row[7]
                ))
            return habits
    
    def update_habit(self, habit: Habit) -> bool:
        """Update an existing habit"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Habits 
                SET HabitName = ?, Description = ?, Period = ?, IsActive = ?
                WHERE HabitID = ?
            """, habit.habit_name, habit.description, habit.period.value, 
               habit.is_active, habit.habit_id)
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_habit(self, habit_id: int) -> bool:
        """Soft delete a habit by setting IsActive to False"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Habits SET IsActive = 0 WHERE HabitID = ?
            """, habit_id)
            
            conn.commit()
            return cursor.rowcount > 0


class HabitCompletionDAO(BaseDAO):
    """Data Access Object for HabitCompletion operations"""
    
    def create_completion(self, completion: HabitCompletion) -> int:
        """Create a new habit completion and return the completion ID"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                # Use OUTPUT clause to get the identity value directly
                cursor.execute("""
                    INSERT INTO HabitCompletions (HabitID, CompletionDate, Notes, CreatedAt)
                    OUTPUT INSERTED.CompletionID
                    VALUES (?, ?, ?, ?)
                """, completion.habit_id, completion.completion_date, 
                   completion.notes, completion.created_at)
                
                result = cursor.fetchone()
                
                if not result or result[0] is None:
                    raise DatabaseException("Failed to get identity value from OUTPUT clause - insert may have failed")
                
                completion_id = result[0]
                
                # OUTPUT clause typically returns int directly, but handle edge cases
                if not isinstance(completion_id, int):
                    try:
                        if hasattr(completion_id, '__int__'):
                            completion_id = int(completion_id)
                        elif completion_id is not None:
                            completion_id = int(float(completion_id))
                        else:
                            raise DatabaseException("Identity value is None - insert failed")
                    except (ValueError, TypeError) as e:
                        raise DatabaseException(f"Failed to convert identity value to integer: {str(e)}")
                
                conn.commit()
                return completion_id
                
            except pyodbc.IntegrityError as e:
                conn.rollback()
                if "UK_HabitCompletions_HabitDate" in str(e):
                    raise DatabaseException(f"Habit already completed on {completion.completion_date}")
                raise DatabaseException(f"Database integrity error: {str(e)}")
            except pyodbc.Error as e:
                conn.rollback()
                raise DatabaseException(f"Database error during completion creation: {str(e)}")
            except Exception as e:
                conn.rollback()
                raise DatabaseException(f"Unexpected error during completion creation: {str(e)}")
    
    def get_completions_by_habit_id(self, habit_id: int, limit: Optional[int] = None) -> List[HabitCompletion]:
        """Get completions for a specific habit"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            
            if limit:
                query = """
                    SELECT TOP (?) CompletionID, HabitID, CompletionDate, Notes, CreatedAt
                    FROM HabitCompletions 
                    WHERE HabitID = ?
                    ORDER BY CompletionDate DESC
                """
                cursor.execute(query, (limit, habit_id))
            else:
                query = """
                    SELECT CompletionID, HabitID, CompletionDate, Notes, CreatedAt
                    FROM HabitCompletions 
                    WHERE HabitID = ?
                    ORDER BY CompletionDate DESC
                """
                cursor.execute(query, (habit_id,))
            
            completions = []
            for row in cursor.fetchall():
                completions.append(HabitCompletion(
                    completion_id=row[0],
                    habit_id=row[1],
                    completion_date=row[2],
                    notes=row[3],
                    created_at=row[4]
                ))
            return completions
    
    def get_completion_by_habit_and_date(self, habit_id: int, completion_date: date) -> Optional[HabitCompletion]:
        """Get completion for a specific habit and date"""
        with self.get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT CompletionID, HabitID, CompletionDate, Notes, CreatedAt
                FROM HabitCompletions 
                WHERE HabitID = ? AND CompletionDate = ?
            """, habit_id, completion_date)
            
            row = cursor.fetchone()
            if row:
                return HabitCompletion(
                    completion_id=row[0],
                    habit_id=row[1],
                    completion_date=row[2],
                    notes=row[3],
                    created_at=row[4]
                )
            return None
