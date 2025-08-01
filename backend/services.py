"""
Business Logic Services for Habit Tracker Application
Implements the core business logic and follows the application philosophy:
"Assume user is performing the habit unless they log that they have not performed the routine"
"""
from typing import List, Optional, Dict, Any, Tuple #why is optional and dataetime now used?
from datetime import datetime, date, timedelta
from backend.models import (
    User, Habit, HabitCompletion, HabitPeriod, HabitAnalytics,
    HabitNotFoundException, UserNotFoundException, DatabaseException
)
from backend.database import UserDAO, HabitDAO, HabitCompletionDAO, AnalyticsDAO, UserSettingDAO


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
        return habit
    
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
        return self.habit_dao.delete_habit(habit_id) #what does this do?
    
    def search_habits(self, search_term: str) -> List[Habit]:
        """Search habits by name or description"""
        current_user = self.user_service.get_current_user()
        return self.habit_dao.search_habits(current_user.user_id, search_term)
    
    def get_habits_due_today(self) -> List[Habit]:
        """
        Get habits that are due today based on the app philosophy:
        - Daily habits are due every day
        - Weekly habits are due if not completed this week
        """
        habits = self.get_all_habits()
        habits_due = []
        today = date.today()
        
        for habit in habits:
            if habit.period == HabitPeriod.DAILY:
                # Daily habits are always due unless completed today
                completion = self.completion_dao.get_completion_by_habit_and_date(
                    habit.habit_id, today
                )
                if not completion:
                    habits_due.append(habit)
            
            elif habit.period == HabitPeriod.WEEKLY:
                # Weekly habits are due if not completed this week
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                
                completions = self.completion_dao.get_completions_by_date_range(
                    habit.habit_id, start_of_week, end_of_week
                )
                if not completions:
                    habits_due.append(habit)
        
        return habits_due
    
    def get_missed_habits(self, days_back: int = 7) -> List[Tuple[Habit, int]]:
        """
        Get habits that have been missed in the last N days
        Returns list of tuples (habit, days_missed)
        """
        habits = self.get_all_habits()
        missed_habits = []
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        
        for habit in habits:
            completions = self.completion_dao.get_completions_by_date_range(
                habit.habit_id, start_date, end_date
            )
            
            if habit.period == HabitPeriod.DAILY:
                expected_completions = days_back
                actual_completions = len(completions)
                days_missed = expected_completions - actual_completions
            else:  # weekly
                expected_completions = days_back // 7
                actual_completions = len(completions)
                days_missed = (expected_completions - actual_completions) * 7  # Convert to days
            
            if days_missed > 0:
                missed_habits.append((habit, days_missed))
        
        # Sort by most missed first
        missed_habits.sort(key=lambda x: x[1], reverse=True)
        return missed_habits


class HabitCompletionService:
    """Service class for habit completion operations"""
    
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
    
    def uncomplete_habit(self, habit_id: int, completion_date: date = None) -> bool:
        """Remove a habit completion for a specific date"""
        if completion_date is None:
            completion_date = date.today()
        
        completion = self.completion_dao.get_completion_by_habit_and_date(
            habit_id, completion_date
        )
        
        if completion:
            return self.completion_dao.delete_completion(completion.completion_id)
        return False
    
    def get_habit_completions(self, habit_id: int, limit: int = None) -> List[HabitCompletion]:
        """Get completions for a specific habit"""
        return self.completion_dao.get_completions_by_habit_id(habit_id, limit)
    
    def get_completions_for_date_range(self, habit_id: int, start_date: date, 
                                     end_date: date) -> List[HabitCompletion]:
        """Get completions within a date range"""
        return self.completion_dao.get_completions_by_date_range(habit_id, start_date, end_date)
    
    def is_habit_completed_today(self, habit_id: int) -> bool:
        """Check if a habit is completed today"""
        completion = self.completion_dao.get_completion_by_habit_and_date(
            habit_id, date.today()
        )
        return completion is not None
    
    def get_completion_calendar(self, habit_id: int, year: int, month: int) -> Dict[int, bool]:
        """Get completion status for each day of a specific month"""
        from calendar import monthrange
        
        # Get first and last day of the month
        first_day = date(year, month, 1)
        last_day_num = monthrange(year, month)[1]
        last_day = date(year, month, last_day_num)
        
        # Get all completions for the month
        completions = self.completion_dao.get_completions_by_date_range(
            habit_id, first_day, last_day
        )
        
        # Create a dictionary mapping day -> completion status
        completion_calendar = {}
        completed_days = {comp.completion_date.day for comp in completions}
        
        for day in range(1, last_day_num + 1):
            completion_calendar[day] = day in completed_days
        
        return completion_calendar


class HabitAnalyticsService:
    """Service class for habit analytics and statistics using functional programming"""
    
    def __init__(self):
        self.analytics_dao = AnalyticsDAO()
        self.habit_service = HabitService()
        self.user_service = UserService()
    
    def get_comprehensive_analytics(self, habit_id: int) -> HabitAnalytics:
        """Get comprehensive analytics for a specific habit"""
        habit = self.habit_service.get_habit_by_id(habit_id)
        
        # Get current streak
        current_user = self.user_service.get_current_user()
        current_streaks = self.analytics_dao.get_current_streaks(current_user.user_id)
        current_streak = next(
            (s['current_streak'] for s in current_streaks if s['habit_id'] == habit_id), 0
        )
        
        # Get longest streak
        longest_streaks = self.analytics_dao.get_longest_streaks(current_user.user_id)
        longest_streak_data = next(
            (s for s in longest_streaks if s['habit_id'] == habit_id), 
            {'longest_streak': 0, 'longest_streak_start': None, 'longest_streak_end': None}
        )
        
        # Get completion statistics
        stats = self.analytics_dao.get_completion_statistics(habit_id)
        
        return HabitAnalytics(
            habit_id=habit_id,
            habit_name=habit.habit_name,
            period=habit.period.value,
            current_streak=current_streak,
            longest_streak=longest_streak_data['longest_streak'],
            total_completions=stats['total_completions'],
            completion_rate=stats['completion_rate'],
            longest_streak_start=longest_streak_data['longest_streak_start'],
            longest_streak_end=longest_streak_data['longest_streak_end']
        )
    
    def get_all_habits_analytics(self) -> List[HabitAnalytics]:
        """Get analytics for all active habits"""
        habits = self.habit_service.get_all_habits()
        return [self.get_comprehensive_analytics(habit.habit_id) for habit in habits]
    
    def get_easiest_habits(self, limit: int = 3) -> List[HabitAnalytics]:
        """Get the easiest habits based on completion rate"""
        all_analytics = self.get_all_habits_analytics()
        return sorted(all_analytics, key=lambda x: x.completion_rate, reverse=True)[:limit]
    
    def get_most_difficult_habits(self, limit: int = 3) -> List[HabitAnalytics]:
        """Get the most difficult habits based on completion rate"""
        all_analytics = self.get_all_habits_analytics()
        return sorted(all_analytics, key=lambda x: x.completion_rate)[:limit]
    
    def get_best_streaks(self, limit: int = 5) -> List[HabitAnalytics]:
        """Get habits with the best current streaks"""
        all_analytics = self.get_all_habits_analytics()
        return sorted(all_analytics, key=lambda x: x.current_streak, reverse=True)[:limit]
    
    def get_longest_all_time_streaks(self, limit: int = 5) -> List[HabitAnalytics]:
        """Get habits with the longest all-time streaks"""
        all_analytics = self.get_all_habits_analytics()
        return sorted(all_analytics, key=lambda x: x.longest_streak, reverse=True)[:limit]
    
    def get_weekly_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of this week's progress across all habits"""
        habits = self.habit_service.get_all_habits()
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        
        total_habits = len(habits)
        completed_today = 0
        weekly_completions = 0
        
        for habit in habits:
            # Check if completed today
            completion_service = HabitCompletionService()
            if completion_service.is_habit_completed_today(habit.habit_id):
                completed_today += 1
            
            # Count weekly completions
            completions = completion_service.get_completions_for_date_range(
                habit.habit_id, start_of_week, today
            )
            weekly_completions += len(completions)
        
        return {
            'total_habits': total_habits,
            'completed_today': completed_today,
            'completion_rate_today': (completed_today / total_habits * 100) if total_habits > 0 else 0,
            'weekly_completions': weekly_completions,
            'week_start': start_of_week,
            'days_into_week': (today - start_of_week).days + 1
        }
    
    def get_habit_trends(self, habit_id: int, weeks_back: int = 4) -> List[Dict[str, Any]]:
        """Get weekly completion trends for a habit"""
        habit = self.habit_service.get_habit_by_id(habit_id)
        completion_service = HabitCompletionService()
        
        trends = []
        today = date.today()
        
        for week_offset in range(weeks_back):
            week_start = today - timedelta(days=today.weekday() + (week_offset * 7))
            week_end = week_start + timedelta(days=6)
            
            completions = completion_service.get_completions_for_date_range(
                habit_id, week_start, week_end
            )
            
            if habit.period == HabitPeriod.DAILY:
                expected = 7
                completion_rate = (len(completions) / 7) * 100
            else:  # weekly
                expected = 1
                completion_rate = 100 if len(completions) >= 1 else 0
            
            trends.append({
                'week_start': week_start,
                'week_end': week_end,
                'completions': len(completions),
                'expected': expected,
                'completion_rate': round(completion_rate, 1),
                'week_number': week_offset + 1
            })
        
        return list(reversed(trends))  # Most recent week first

    def calculate_habit_persistence_probability(self, habit_id: int) -> Dict[str, Any]:
        """Calculate the probability that a habit will be maintained based on historical patterns"""
        from .analytics import calculate_habit_persistence_probability
        
        # Get habit data
        habit = self.habit_service.get_habit_by_id(habit_id)
        completion_service = HabitCompletionService()
        
        # Get all completions for this habit
        completions = completion_service.get_habit_completions(habit_id)
        completion_dates = [c.completion_date for c in completions]
        
        return calculate_habit_persistence_probability(completion_dates, habit.period.value, 4)
    
    def predict_habit_difficulty(self, habit_id: int) -> Dict[str, Any]:
        """Predict difficulty level and provide insights for a habit"""
        from .analytics import predict_habit_difficulty
        
        # Get habit data
        habit = self.habit_service.get_habit_by_id(habit_id)
        completion_service = HabitCompletionService()
        
        # Get all completions for this habit
        completions = completion_service.get_habit_completions(habit_id)
        
        result = predict_habit_difficulty(habit, completions)
        result['habit_name'] = habit.habit_name
        return result
    
    def predict_streak_continuation(self, habit_id: int) -> Dict[str, Any]:
        """Predict likelihood of continuing current streak"""
        from .analytics import predict_streak_continuation
        
        # Get habit data
        habit = self.habit_service.get_habit_by_id(habit_id)
        completion_service = HabitCompletionService()
        
        # Get all completions for this habit
        completions = completion_service.get_habit_completions(habit_id)
        completion_dates = [c.completion_date for c in completions]
        
        # Get current streak
        current_streaks = self.analytics_dao.get_current_streaks(self.user_service.get_current_user().user_id)
        current_streak = next(
            (s['current_streak'] for s in current_streaks if s['habit_id'] == habit_id), 0
        )
        
        result = predict_streak_continuation(completion_dates, habit.period.value, current_streak)
        result['habit_name'] = habit.habit_name
        return result


class SystemService:
    """Service for system-wide operations and initialization"""
    
    def __init__(self):
        self.user_service = UserService()
        self.habit_service = HabitService()
    
    def initialize_system(self) -> bool:
        """Initialize the system with demo user and check database connectivity"""
        try:
            # Ensure demo user exists
            user = self.user_service.create_demo_user()
            
            # Check if we have any habits, if not, create some demo habits
            habits = self.habit_service.get_all_habits()
            if not habits:
                self._create_demo_habits()
            
            return True
        except Exception as e:
            print(f"System initialization failed: {e}")
            return False
    
    def _create_demo_habits(self):
        """Create demo habits if none exist"""
        demo_habits = [
            ("💧 Drink 8 glasses of water", "Stay hydrated throughout the day", "daily"),
            ("📖 Read for 30 minutes", "Read books or articles for personal growth", "daily"),
            ("🏃‍♂️ Exercise", "Physical activity for health", "daily"),
            ("🧘 Meditation", "10 minutes of mindfulness", "daily"),
            ("🏠 Clean house", "Weekly house cleaning routine", "weekly")
        ]
        
        for name, description, period in demo_habits:
            try:
                self.habit_service.create_habit(name, description, period)
            except Exception as e:
                print(f"Warning: Could not create demo habit '{name}': {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and health check"""
        try:
            user = self.user_service.get_current_user()
            habits = self.habit_service.get_all_habits()
            
            return {
                'status': 'healthy',
                'user_id': user.user_id,
                'username': user.username,
                'total_habits': len(habits),
                'active_habits': len([h for h in habits if h.is_active]),
                'system_initialized': True
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'system_initialized': False
            }
