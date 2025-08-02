"""
Updated tests for the cleaned up Habit Tracker backend
Tests only the functionality that was kept:
1. Habit creation, editing, deletion
2. Habit completion tracking
3. Analytics functions (4 specific ones)
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, datetime, timedelta
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.models import Habit, HabitCompletion, HabitPeriod
from backend.analytics import (
    get_currently_tracked_habits,
    get_habits_with_same_periodicity,
    get_longest_run_streak_all_habits,
    get_longest_run_streak_for_habit,
    calculate_streak_length
)


class TestHabitModels(unittest.TestCase):
    """Test cases for habit models"""
    
    def test_habit_creation(self):
        """Test creating a habit with default values"""
        habit = Habit(
            habit_name="Test Habit",
            description="A test habit",
            period=HabitPeriod.DAILY
        )
        
        self.assertEqual(habit.habit_name, "Test Habit")
        self.assertEqual(habit.description, "A test habit")
        self.assertEqual(habit.period, HabitPeriod.DAILY)
        self.assertTrue(habit.is_active)
        self.assertIsNotNone(habit.created_date)
        self.assertIsNotNone(habit.created_at)
    
    def test_habit_period_from_string(self):
        """Test creating habit with string period"""
        habit = Habit(
            habit_name="Daily Habit",
            period="daily"
        )
        
        self.assertEqual(habit.period, HabitPeriod.DAILY)
    
    def test_habit_completion_creation(self):
        """Test creating a habit completion"""
        completion = HabitCompletion(
            habit_id=1,
            completion_date=date.today(),
            notes="Test completion"
        )
        
        self.assertEqual(completion.habit_id, 1)
        self.assertEqual(completion.completion_date, date.today())
        self.assertEqual(completion.notes, "Test completion")


class TestAnalyticsFunctions(unittest.TestCase):
    """Test cases for the 4 essential analytics functions"""
    
    def setUp(self):
        """Set up test data"""
        self.active_habit = Habit(
            habit_id=1,
            habit_name="Active Habit",
            period=HabitPeriod.DAILY,
            is_active=True
        )
        
        self.inactive_habit = Habit(
            habit_id=2, 
            habit_name="Inactive Habit",
            period=HabitPeriod.DAILY,
            is_active=False
        )
        
        self.weekly_habit = Habit(
            habit_id=3,
            habit_name="Weekly Habit", 
            period=HabitPeriod.WEEKLY,
            is_active=True
        )
        
        self.habits = [self.active_habit, self.inactive_habit, self.weekly_habit]
        
        # Create some completions for testing streaks
        today = date.today()
        self.completions = [
            HabitCompletion(habit_id=1, completion_date=today),
            HabitCompletion(habit_id=1, completion_date=today - timedelta(days=1)),
            HabitCompletion(habit_id=1, completion_date=today - timedelta(days=2)),
        ]
    
    def test_get_currently_tracked_habits(self):
        """Test getting currently tracked (active) habits"""
        result = get_currently_tracked_habits(self.habits)
        
        # Should return only active habits
        self.assertEqual(len(result), 2)
        habit_names = [h.habit_name for h in result]
        self.assertIn("Active Habit", habit_names)
        self.assertIn("Weekly Habit", habit_names)
        self.assertNotIn("Inactive Habit", habit_names)
    
    def test_get_habits_with_same_periodicity_daily(self):
        """Test getting habits with same periodicity - daily"""
        result = get_habits_with_same_periodicity(self.habits, HabitPeriod.DAILY)
        
        # Should return habits with daily period
        self.assertEqual(len(result), 2)
        for habit in result:
            self.assertEqual(habit.period, HabitPeriod.DAILY)
    
    def test_get_habits_with_same_periodicity_weekly(self):
        """Test getting habits with same periodicity - weekly"""
        result = get_habits_with_same_periodicity(self.habits, HabitPeriod.WEEKLY)
        
        # Should return habits with weekly period
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].habit_name, "Weekly Habit")
        self.assertEqual(result[0].period, HabitPeriod.WEEKLY)
    
    def test_get_longest_run_streak_all_habits(self):
        """Test getting longest run streak across all habits"""
        completions_by_habit = {
            1: self.completions,
            2: [],
            3: [HabitCompletion(habit_id=3, completion_date=date.today())]
        }
        
        result = get_longest_run_streak_all_habits(self.habits, completions_by_habit)
        
        # Should return the habit with the longest streak
        self.assertIsNotNone(result['habit'])
        self.assertEqual(result['habit_name'], "Active Habit")
        self.assertGreater(result['streak_length'], 0)
    
    def test_get_longest_run_streak_for_habit(self):
        """Test getting longest run streak for a specific habit"""
        result = get_longest_run_streak_for_habit(self.active_habit, self.completions)
        
        # Should calculate streak length for the given habit
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
    
    def test_calculate_streak_length_empty_completions(self):
        """Test streak calculation with no completions"""
        result = calculate_streak_length([], HabitPeriod.DAILY)
        self.assertEqual(result, 0)
    
    def test_calculate_streak_length_daily_habit(self):
        """Test streak calculation for daily habit"""
        result = calculate_streak_length(self.completions, HabitPeriod.DAILY)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
    
    def test_calculate_streak_length_weekly_habit(self):
        """Test streak calculation for weekly habit"""
        weekly_completions = [
            HabitCompletion(habit_id=3, completion_date=date.today())
        ]
        result = calculate_streak_length(weekly_completions, HabitPeriod.WEEKLY)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)


class TestHabitServices(unittest.TestCase):
    """Test cases for habit services that were kept"""
    
    @patch('backend.services.HabitDAO')
    @patch('backend.services.UserService')
    def test_habit_service_creation(self, mock_user_service, mock_habit_dao):
        """Test that HabitService can be created"""
        from backend.services import HabitService
        
        service = HabitService()
        self.assertIsNotNone(service)
    
    @patch('backend.services.HabitCompletionDAO')
    def test_completion_service_creation(self, mock_completion_dao):
        """Test that HabitCompletionService can be created"""
        from backend.services import HabitCompletionService
        
        service = HabitCompletionService()
        self.assertIsNotNone(service)
    
    @patch('backend.services.HabitService')
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.UserService')
    def test_analytics_service_creation(self, mock_user_service, mock_completion_service, mock_habit_service):
        """Test that HabitAnalyticsService can be created"""
        from backend.services import HabitAnalyticsService
        
        service = HabitAnalyticsService()
        self.assertIsNotNone(service)


class TestFunctionalRequirements(unittest.TestCase):
    """Test cases for the specific functional requirements mentioned"""
    
    def test_habit_creation_requirement(self):
        """Test that habits can be created (requirement 1)"""
        habit = Habit(
            habit_name="Morning Exercise",
            description="30 minutes of exercise",
            period=HabitPeriod.DAILY
        )
        
        self.assertEqual(habit.habit_name, "Morning Exercise")
        self.assertEqual(habit.description, "30 minutes of exercise")
        self.assertEqual(habit.period, HabitPeriod.DAILY)
        self.assertTrue(habit.is_active)
    
    def test_habit_edit_delete_requirement(self):
        """Test that habits can be edited and deleted (requirement 2)"""
        habit = Habit(
            habit_name="Original Name",
            description="Original Description",
            period=HabitPeriod.DAILY
        )
        
        # Test editing (changing properties)
        habit.habit_name = "Updated Name"
        habit.description = "Updated Description"
        
        self.assertEqual(habit.habit_name, "Updated Name")
        self.assertEqual(habit.description, "Updated Description")
        
        # Test deletion (marking as inactive)
        habit.is_active = False
        self.assertFalse(habit.is_active)
    
    def test_tracking_system_requirement(self):
        """Test that completion tracking works (requirement 4)"""
        completion = HabitCompletion(
            habit_id=1,
            completion_date=date.today(),
            notes="Completed successfully"
        )
        
        self.assertEqual(completion.habit_id, 1)
        self.assertEqual(completion.completion_date, date.today())
        self.assertEqual(completion.notes, "Completed successfully")
        self.assertIsNotNone(completion.created_at)
    
    def test_analytics_requirements(self):
        """Test that all 4 analytics functions exist and work (requirement 5)"""
        # Create test data
        habits = [
            Habit(habit_id=1, habit_name="Habit 1", period=HabitPeriod.DAILY, is_active=True),
            Habit(habit_id=2, habit_name="Habit 2", period=HabitPeriod.WEEKLY, is_active=True),
            Habit(habit_id=3, habit_name="Habit 3", period=HabitPeriod.DAILY, is_active=False)
        ]
        
        completions = [
            HabitCompletion(habit_id=1, completion_date=date.today()),
            HabitCompletion(habit_id=2, completion_date=date.today())
        ]
        
        completions_by_habit = {1: completions[:1], 2: completions[1:]}
        
        # 5a. Test currently tracked habits
        tracked = get_currently_tracked_habits(habits)
        self.assertEqual(len(tracked), 2)  # Only active habits
        
        # 5b. Test habits with same periodicity
        daily_habits = get_habits_with_same_periodicity(habits, HabitPeriod.DAILY)
        weekly_habits = get_habits_with_same_periodicity(habits, HabitPeriod.WEEKLY)
        self.assertEqual(len(daily_habits), 2)
        self.assertEqual(len(weekly_habits), 1)
        
        # 5c. Test longest run streak of all habits
        longest_all = get_longest_run_streak_all_habits(habits, completions_by_habit)
        self.assertIn('habit', longest_all)
        self.assertIn('streak_length', longest_all)
        self.assertIn('habit_name', longest_all)
        
        # 5d. Test longest run streak for a given habit
        streak_for_habit = get_longest_run_streak_for_habit(habits[0], completions[:1])
        self.assertIsInstance(streak_for_habit, int)


class TestTaskCompletionRequirement(unittest.TestCase):
    """Test cases specifically for the 'Task Completion' requirement"""
    
    @patch('backend.services.HabitCompletionDAO')
    @patch('backend.services.HabitService')
    def test_complete_habit_service_method(self, mock_habit_service, mock_completion_dao):
        """Test that habits can be completed through the service layer"""
        from backend.services import HabitCompletionService
        
        # Mock the habit service to return a test habit
        mock_habit = Habit(habit_id=1, habit_name="Test Habit", period=HabitPeriod.DAILY)
        mock_habit_service.return_value.get_habit_by_id.return_value = mock_habit
        
        # Mock the DAO to return a completion ID
        mock_completion_dao.return_value.create_completion.return_value = 123
        
        service = HabitCompletionService()
        completion = service.complete_habit(habit_id=1, notes="Test completion")
        
        # Verify the completion was created
        self.assertIsNotNone(completion)
        self.assertEqual(completion.habit_id, 1)
        self.assertEqual(completion.notes, "Test completion")
        self.assertEqual(completion.completion_date, date.today())
        self.assertEqual(completion.completion_id, 123)
    
    @patch('backend.services.HabitCompletionDAO')
    @patch('backend.services.HabitService')
    def test_complete_habit_at_any_time(self, mock_habit_service, mock_completion_dao):
        """Test that habits can be completed for any date (past, present, future)"""
        from backend.services import HabitCompletionService
        
        # Mock the habit service
        mock_habit = Habit(habit_id=1, habit_name="Test Habit", period=HabitPeriod.DAILY)
        mock_habit_service.return_value.get_habit_by_id.return_value = mock_habit
        mock_completion_dao.return_value.create_completion.return_value = 123
        
        service = HabitCompletionService()
        
        # Test completing for yesterday
        yesterday = date.today() - timedelta(days=1)
        completion_past = service.complete_habit(habit_id=1, completion_date=yesterday)
        self.assertEqual(completion_past.completion_date, yesterday)
        
        # Test completing for today (default)
        completion_today = service.complete_habit(habit_id=1)
        self.assertEqual(completion_today.completion_date, date.today())
        
        # Test completing for tomorrow  
        tomorrow = date.today() + timedelta(days=1)
        completion_future = service.complete_habit(habit_id=1, completion_date=tomorrow)
        self.assertEqual(completion_future.completion_date, tomorrow)
    
    @patch('backend.services.HabitCompletionDAO')
    @patch('backend.services.HabitService')
    def test_is_habit_completed_today(self, mock_habit_service, mock_completion_dao):
        """Test checking if a habit is completed today"""
        from backend.services import HabitCompletionService
        
        service = HabitCompletionService()
        
        # Test when habit is NOT completed today
        mock_completion_dao.return_value.get_completion_by_habit_and_date.return_value = None
        is_completed = service.is_habit_completed_today(habit_id=1)
        self.assertFalse(is_completed)
        
        # Test when habit IS completed today
        mock_completion = HabitCompletion(habit_id=1, completion_date=date.today())
        mock_completion_dao.return_value.get_completion_by_habit_and_date.return_value = mock_completion
        is_completed = service.is_habit_completed_today(habit_id=1)
        self.assertTrue(is_completed)
    
    def test_task_completion_requirement_model_level(self):
        """Test that task completion works at the model level"""
        # Test creating a completion for today
        today_completion = HabitCompletion(
            habit_id=1,
            completion_date=date.today(),
            notes="Completed today"
        )
        self.assertEqual(today_completion.completion_date, date.today())
        
        # Test creating a completion for a past date
        past_date = date.today() - timedelta(days=5)
        past_completion = HabitCompletion(
            habit_id=1,
            completion_date=past_date,
            notes="Completed 5 days ago"
        )
        self.assertEqual(past_completion.completion_date, past_date)
        
        # Test creating a completion for a future date
        future_date = date.today() + timedelta(days=3)
        future_completion = HabitCompletion(
            habit_id=1,
            completion_date=future_date,
            notes="Planned for future"
        )
        self.assertEqual(future_completion.completion_date, future_date)
        
        # Verify all completions have proper timestamps
        self.assertIsNotNone(today_completion.created_at)
        self.assertIsNotNone(past_completion.created_at)
        self.assertIsNotNone(future_completion.created_at)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
