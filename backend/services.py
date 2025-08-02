"""
Business Logic Services for Habit Tracker Application
Implements the core business logic and follows the application philosophy:
"Assume user is performing the habit unless they log that they have not performed the routine"
"""
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date, timedelta
from backend.models import (
    User, Habit, HabitCompletion, HabitPeriod,
    HabitNotFoundException, UserNotFoundException, DatabaseException
)
from backend.database import UserDAO, HabitDAO, HabitCompletionDAO


class UserService:
    """Service class for user-related operations"""
    
    def __init__(self):
        self.user_dao = UserDAO()
    
    def create_demo_user(self) -> User:
        """Create or get the demo user for single-user application"""
        # Try to get existing demo user first
        existing_user = self.user_dao.get_user_by_username("demo_user")
        if existing_user:
            return existing_user
        
        # Create new demo user
        demo_user = User(
            username="demo_user",
            password_hash="demo_hash",  # In a real app, this would be properly hashed
            email="demo@habittracker.local"
        )
        
        user_id = self.user_dao.create_user(demo_user)
        demo_user.user_id = user_id
        return demo_user
    
    def get_current_user(self) -> User:
        """Get the current user (demo user for this single-user application)"""
        user = self.user_dao.get_user_by_username("demo_user")
        if not user:
            return self.create_demo_user()
        return user


class HabitService:
    """Service class for habit-related operations"""
    
    def __init__(self):
        self.habit_dao = HabitDAO()
        self.completion_dao = HabitCompletionDAO()
        self.user_service = UserService()
    #essential habit method (keep this)
    def create_habit(self, habit_name: str, description: str, period: str) -> Habit:
        """Create a new habit"""
        current_user = self.user_service.get_current_user()
        
        habit = Habit(
            user_id=current_user.user_id,
            habit_name=habit_name,
            description=description,
            period=HabitPeriod(period.lower())
        )
        
        habit_id = self.habit_dao.create_habit(habit)
        habit.habit_id = habit_id
        return habit #returns a habit object with id
    
    def get_all_habits(self, active_only: bool = True) -> List[Habit]:
        """Get all habits for the current user"""
        current_user = self.user_service.get_current_user()
        return self.habit_dao.get_habits_by_user_id(current_user.user_id, active_only)
    
    def get_habit_by_id(self, habit_id: int) -> Habit:
        """Get a specific habit by ID"""
        habit = self.habit_dao.get_habit_by_id(habit_id)
        if not habit:
            raise HabitNotFoundException(f"Habit with ID {habit_id} not found")
        return habit
    
    def update_habit(self, habit_id: int, habit_name: str = None, description: str = None, 
                    period: str = None) -> Habit:
        """Update an existing habit"""
        habit = self.get_habit_by_id(habit_id)
        
        if habit_name:
            habit.habit_name = habit_name
        if description:
            habit.description = description
        if period:
            habit.period = HabitPeriod(period.lower())
        
        success = self.habit_dao.update_habit(habit)
        if not success:
            raise DatabaseException("Failed to update habit")
        
        return habit
    
    def delete_habit(self, habit_id: int) -> bool:
        """Soft delete a habit"""
        habit = self.get_habit_by_id(habit_id)  # Verify habit exists
        return self.habit_dao.delete_habit(habit_id)


class HabitCompletionService:
    """Simplified service class for habit completion operations"""
    
    def __init__(self):
        self.completion_dao = HabitCompletionDAO()
        self.habit_service = HabitService()
    
    def complete_habit(self, habit_id: int, completion_date: date = None, notes: str = "") -> HabitCompletion:
        """Mark a habit as completed for a specific date"""
        habit = self.habit_service.get_habit_by_id(habit_id)  # Verify habit exists
        
        if completion_date is None:
            completion_date = date.today()
        
        completion = HabitCompletion(
            habit_id=habit_id,
            completion_date=completion_date,
            notes=notes
        )
        
        completion_id = self.completion_dao.create_completion(completion)
        completion.completion_id = completion_id
        return completion
    
    def get_habit_completions(self, habit_id: int, limit: int = None) -> List[HabitCompletion]:
        """Get completions for a specific habit"""
        return self.completion_dao.get_completions_by_habit_id(habit_id, limit)
    
    def is_habit_completed_today(self, habit_id: int) -> bool:
        """Check if a habit is completed today"""
        completion = self.completion_dao.get_completion_by_habit_and_date(
            habit_id, date.today()
        )
        return completion is not None


class HabitAnalyticsService:
    """Service class for habit analytics using the functional programming analytics module"""
    
    def __init__(self):
        self.habit_service = HabitService()
        self.completion_service = HabitCompletionService()
        self.user_service = UserService()
    
    def get_currently_tracked_habits(self) -> List[Habit]:
        """Get list of currently tracked habits"""
        from backend.analytics import get_currently_tracked_habits
        habits = self.habit_service.get_all_habits()
        return get_currently_tracked_habits(habits)
    
    def get_habits_with_same_periodicity(self, periodicity: HabitPeriod) -> List[Habit]:
        """Get list of habits with same periodicity"""
        from backend.analytics import get_habits_with_same_periodicity
        habits = self.habit_service.get_all_habits()
        return get_habits_with_same_periodicity(habits, periodicity)
    
    def get_longest_run_streak_all_habits(self) -> Dict[str, Any]:
        """Get longest run streak of all defined habits"""
        from backend.analytics import get_longest_run_streak_all_habits
        habits = self.habit_service.get_all_habits()
        
        # Get completions for all habits
        completions_by_habit = {}
        for habit in habits:
            completions_by_habit[habit.habit_id] = self.completion_service.get_habit_completions(habit.habit_id)
        
        return get_longest_run_streak_all_habits(habits, completions_by_habit)
    
    def get_longest_run_streak_for_habit(self, habit_id: int) -> int:
        """Get longest run streak for a given habit"""
        from backend.analytics import get_longest_run_streak_for_habit
        habit = self.habit_service.get_habit_by_id(habit_id)
        completions = self.completion_service.get_habit_completions(habit_id)
        return get_longest_run_streak_for_habit(habit, completions)
