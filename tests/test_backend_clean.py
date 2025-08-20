"""
Updated tests for the cleaned up Habit Tracker backend
Tests only the functionality that was kept:
1. Habit creation, editing, deletion
2. Habit completion tracking
3. Analytics functions (4 specific LOW-LEVEL functions from backend.analytics)

NOTE: These tests focus on the pure analytics functions (backend.analytics), 
NOT the service layer methods used by the CLI. For service layer testing, 
see test_services.py

This test suite includes:
- 4 weeks worth of predefined habit data for testing
- Comprehensive coverage of all analytics functions
- Tests for streak calculations respecting habit periodicity
- Edge cases and error scenarios
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, datetime, timedelta #timedelta is pretty awesome btw see here: https://www.geeksforgeeks.org/python/python-datetime-timedelta-function/
import sys
import os

# Add backend to path
#adds parent directory to path 
#gotcha's: earlier entries take precedence... probably should use insert(0, path) instead
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.models import Habit, HabitCompletion, HabitPeriod
from backend.analytics import (
    get_currently_tracked_habits,
    get_habits_with_same_periodicity,
    get_longest_run_streak_all_habits,
    get_longest_run_streak_for_habit,
    get_current_streak_for_habit,  # Added this missing function
    calculate_streak_length
)
from tests.test_data import (
    get_test_habits,
    get_four_weeks_completion_data,
    get_broken_streak_data,
    get_edge_case_data,
    get_all_test_data,
    PERFECT_DAILY_STREAK,
    PERFECT_WEEKLY_STREAK
)


class TestHabitModels(unittest.TestCase):
    """Test cases for habit models"""
    
    def test_habit_creation(self):
        """Test creating a habit with default values"""
        # Test daily habit creation
        daily_habit = Habit(
            habit_name="Test Daily Habit",
            description="A test daily habit",
            period=HabitPeriod.DAILY
        )
        
        self.assertEqual(daily_habit.habit_name, "Test Daily Habit")
        self.assertEqual(daily_habit.description, "A test daily habit")
        self.assertEqual(daily_habit.period, HabitPeriod.DAILY)
        self.assertTrue(daily_habit.is_active)
        self.assertIsNotNone(daily_habit.created_date)
        self.assertIsNotNone(daily_habit.created_at)
        
        # Test weekly habit creation
        weekly_habit = Habit(
            habit_name="Test Weekly Habit",
            description="A test weekly habit",
            period=HabitPeriod.WEEKLY
        )
        
        self.assertEqual(weekly_habit.habit_name, "Test Weekly Habit")
        self.assertEqual(weekly_habit.description, "A test weekly habit")
        self.assertEqual(weekly_habit.period, HabitPeriod.WEEKLY)
        self.assertTrue(weekly_habit.is_active)
        self.assertIsNotNone(weekly_habit.created_date)
        self.assertIsNotNone(weekly_habit.created_at)
    
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
    """Test cases for the 4 essential LOW-LEVEL analytics functions from backend.analytics
    
    These are the pure functions that take data as parameters, NOT the service layer methods.
    The CLI uses service layer methods which wrap these functions.
    """
    
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
    
    def test_get_current_streak_for_habit(self):
        """Test getting current streak for a specific habit (used by CLI)"""
        result = get_current_streak_for_habit(self.active_habit, self.completions)
        
        # Should calculate current streak length for the given habit
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
    
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


class TestFourWeeksData(unittest.TestCase):
    """Test cases using 4 weeks worth of predefined habit data"""
    
    def setUp(self):
        """Set up 4 weeks test data"""
        self.test_habits = get_test_habits()
        self.four_weeks_completions = get_four_weeks_completion_data()
    
    def test_perfect_daily_habit_streak(self):
        """Test analytics with perfect daily habit (28/28 days)"""
        exercise_habit = self.test_habits[0]  # Exercise habit
        exercise_completions = self.four_weeks_completions[1]
        
        # Should have perfect completion
        self.assertEqual(len(exercise_completions), PERFECT_DAILY_STREAK)
        
        # Test longest run streak calculation
        longest_streak = get_longest_run_streak_for_habit(exercise_habit, exercise_completions)
        self.assertEqual(longest_streak, PERFECT_DAILY_STREAK)
        
        # Test current streak calculation
        current_streak = calculate_streak_length(exercise_completions, HabitPeriod.DAILY)
        self.assertEqual(current_streak, PERFECT_DAILY_STREAK)
    
    def test_perfect_weekly_habit_streak(self):
        """Test analytics with perfect weekly habit (4/4 weeks)"""
        cleaning_habit = self.test_habits[3]  # House cleaning habit
        cleaning_completions = self.four_weeks_completions[4]
        
        # Should have perfect weekly completion
        self.assertEqual(len(cleaning_completions), PERFECT_WEEKLY_STREAK)
        
        # Test longest run streak calculation
        longest_streak = get_longest_run_streak_for_habit(cleaning_habit, cleaning_completions)
        self.assertEqual(longest_streak, PERFECT_WEEKLY_STREAK)
        
        # Test current streak calculation
        current_streak = calculate_streak_length(cleaning_completions, HabitPeriod.WEEKLY)
        self.assertEqual(current_streak, PERFECT_WEEKLY_STREAK)
    
    def test_good_consistency_daily_habit(self):
        """Test analytics with good but not perfect daily habit (22/28 days)"""
        reading_habit = self.test_habits[1]  # Reading habit
        reading_completions = self.four_weeks_completions[2]
        
        # Should have 22 completions
        self.assertEqual(len(reading_completions), 22)
        
        # Test streak calculation (should handle gaps properly)
        longest_streak = get_longest_run_streak_for_habit(reading_habit, reading_completions)
        self.assertGreater(longest_streak, 0)
        self.assertLessEqual(longest_streak, 22)
    
    def test_improving_pattern_habit(self):
        """Test analytics with improving habit pattern"""
        meditation_habit = self.test_habits[2]  # Meditation habit
        meditation_completions = self.four_weeks_completions[3]
        
        # Should show improvement over time (total 17 days)
        self.assertEqual(len(meditation_completions), 17)
        
        # Verify the pattern improves over weeks
        today = date.today()
        four_weeks_ago = today - timedelta(days=28)
        
        week_counts = [0, 0, 0, 0]
        for completion in meditation_completions:
            days_since_start = (completion.completion_date - four_weeks_ago).days
            week = min(days_since_start // 7, 3)  # Ensure week is 0-3
            week_counts[week] += 1
        
        # Should show improving trend (generally increasing)
        self.assertEqual(week_counts[0], 2)  # Week 1: 2 days
        self.assertEqual(week_counts[1], 4)  # Week 2: 4 days
        self.assertEqual(week_counts[2], 5)  # Week 3: 5 days
        self.assertEqual(week_counts[3], 6)  # Week 4: 6 days
    
    def test_missed_week_weekly_habit(self):
        """Test analytics with weekly habit that missed one week"""
        shopping_habit = self.test_habits[4]  # Grocery shopping habit
        shopping_completions = self.four_weeks_completions[5]
        
        # Should have 3 completions (missed week 2)
        self.assertEqual(len(shopping_completions), 3)
        
        # Test streak calculation
        longest_streak = get_longest_run_streak_for_habit(shopping_habit, shopping_completions)
        self.assertGreater(longest_streak, 0)
        self.assertLessEqual(longest_streak, 3)
    
    def test_analytics_function_1_currently_tracked(self):
        """Test Analytics Function 1: Get currently tracked habits"""
        result = get_currently_tracked_habits(self.test_habits)
        
        # All test habits should be active
        self.assertEqual(len(result), len(self.test_habits))
        for habit in result:
            self.assertTrue(habit.is_active)
    
    def test_analytics_function_2_same_periodicity(self):
        """Test Analytics Function 2: Get habits with same periodicity"""
        daily_habits = get_habits_with_same_periodicity(self.test_habits, HabitPeriod.DAILY)
        weekly_habits = get_habits_with_same_periodicity(self.test_habits, HabitPeriod.WEEKLY)
        
        # Should have 3 daily and 2 weekly habits
        self.assertEqual(len(daily_habits), 3)
        self.assertEqual(len(weekly_habits), 2)
        
        # Verify all are correct periodicity
        for habit in daily_habits:
            self.assertEqual(habit.period, HabitPeriod.DAILY)
        for habit in weekly_habits:
            self.assertEqual(habit.period, HabitPeriod.WEEKLY)
    
    def test_analytics_function_3_longest_streak_all(self):
        """Test Analytics Function 3: Get longest run streak of all habits"""
        result = get_longest_run_streak_all_habits(self.test_habits, self.four_weeks_completions)
        
        # Should return the exercise habit with perfect streak
        self.assertIsNotNone(result['habit'])
        self.assertEqual(result['habit_name'], "Exercise")
        self.assertEqual(result['streak_length'], PERFECT_DAILY_STREAK)
    
    def test_analytics_function_4_longest_streak_specific(self):
        """Test Analytics Function 4: Get longest run streak for given habit"""
        # Test perfect daily habit
        exercise_habit = self.test_habits[0]
        exercise_streak = get_longest_run_streak_for_habit(
            exercise_habit, 
            self.four_weeks_completions[1]
        )
        self.assertEqual(exercise_streak, PERFECT_DAILY_STREAK)
        
        # Test perfect weekly habit
        cleaning_habit = self.test_habits[3]
        cleaning_streak = get_longest_run_streak_for_habit(
            cleaning_habit, 
            self.four_weeks_completions[4]
        )
        self.assertEqual(cleaning_streak, PERFECT_WEEKLY_STREAK)


class TestStreakCalculationEdgeCases(unittest.TestCase):
    """Test edge cases for streak calculations with periodicity respect"""
    
    def setUp(self):
        """Set up edge case test data"""
        self.edge_case_data = get_edge_case_data()
        self.broken_streak_data = get_broken_streak_data()
    
    def test_single_completion_streak(self):
        """Test streak calculation with only one completion"""
        single_completion = self.edge_case_data[201]
        habit = Habit(habit_id=201, period=HabitPeriod.DAILY)
        
        streak = get_longest_run_streak_for_habit(habit, single_completion)
        self.assertEqual(streak, 1)
    
    def test_no_completions_streak(self):
        """Test streak calculation with no completions"""
        no_completions = self.edge_case_data[202]
        habit = Habit(habit_id=202, period=HabitPeriod.DAILY)
        
        streak = get_longest_run_streak_for_habit(habit, no_completions)
        self.assertEqual(streak, 0)
    
    def test_broken_streak_calculation(self):
        """Test that broken streaks are calculated correctly"""
        broken_completions = self.broken_streak_data[101]
        habit = Habit(habit_id=101, period=HabitPeriod.DAILY)
        
        # Should calculate current streak (3 days) not the previous longer streak
        current_streak = calculate_streak_length(broken_completions, HabitPeriod.DAILY)
        self.assertEqual(current_streak, 3)
        
        # Longest streak should be the previous 10-day streak
        longest_streak = get_longest_run_streak_for_habit(habit, broken_completions)
        self.assertEqual(longest_streak, 10)
    
    def test_weekly_multiple_completions_same_week(self):
        """Test weekly habit with multiple completions in same week"""
        same_week_completions = self.edge_case_data[205]
        habit = Habit(habit_id=205, period=HabitPeriod.WEEKLY)
        
        # Should count as one week even with multiple completions
        streak = calculate_streak_length(same_week_completions, HabitPeriod.WEEKLY)
        self.assertEqual(streak, 1)
    
    def test_periodicity_respect_daily(self):
        """Test that daily habits respect daily periodicity in streak calculation"""
        today = date.today()
        daily_completions = [
            HabitCompletion(habit_id=301, completion_date=today),
            HabitCompletion(habit_id=301, completion_date=today - timedelta(days=1)),
            HabitCompletion(habit_id=301, completion_date=today - timedelta(days=2)),
            # Gap of one day
            HabitCompletion(habit_id=301, completion_date=today - timedelta(days=4)),
        ]
        
        habit = Habit(habit_id=301, period=HabitPeriod.DAILY)
        
        # Current streak should be 3 (today, yesterday, day before)
        current_streak = calculate_streak_length(daily_completions, HabitPeriod.DAILY)
        self.assertEqual(current_streak, 3)
    
    def test_periodicity_respect_weekly(self):
        """Test that weekly habits respect weekly periodicity in streak calculation"""
        today = date.today()
        
        # Get start of current week (Monday)
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)
        
        weekly_completions = [
            # This week
            HabitCompletion(habit_id=302, completion_date=today),
            # Last week
            HabitCompletion(habit_id=302, completion_date=current_week_start - timedelta(days=3)),
            # Two weeks ago
            HabitCompletion(habit_id=302, completion_date=current_week_start - timedelta(days=10)),
            # Skip three weeks ago
            # Four weeks ago
            HabitCompletion(habit_id=302, completion_date=current_week_start - timedelta(days=24)),
        ]
        
        habit = Habit(habit_id=302, period=HabitPeriod.WEEKLY)
        
        # Current streak should be 3 consecutive weeks
        current_streak = calculate_streak_length(weekly_completions, HabitPeriod.WEEKLY)
        self.assertEqual(current_streak, 3)


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
        
        # Test completing for tomorrow  --> should show error
        tomorrow = date.today() + timedelta(days=1)
        with self.assertRaises(ValueError) as context:
            service.complete_habit(habit_id=1, completion_date=tomorrow)
        self.assertEqual(str(context.exception), "Completion date cannot be in the future")
    
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
