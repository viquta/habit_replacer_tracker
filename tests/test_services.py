"""
Test Suite for Service Layer Functions Used by CLI
Tests the actual service methods that the CLI calls, not the low-level analytics functions.

This test suite covers:
1. HabitAnalyticsService methods used by CLI
2. Integration with the service layer
3. Real-world usage patterns from CLI

The CLI actually calls these service methods:
- analytics_service.get_currently_tracked_habits()
- analytics_service.get_habits_with_same_periodicity()
- analytics_service.get_longest_run_streak_for_habit()
- analytics_service.get_current_streak_for_habit()
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.models import Habit, HabitCompletion, HabitPeriod
from backend.services import HabitAnalyticsService
from tests.test_data import (
    get_test_habits,
    get_four_weeks_completion_data,
    PERFECT_DAILY_STREAK,
    PERFECT_WEEKLY_STREAK
)


class TestHabitAnalyticsService(unittest.TestCase):
    """Test cases for HabitAnalyticsService - the actual service used by CLI"""
    
    def setUp(self):
        """Set up test data and service"""
        self.test_habits = get_test_habits()
        self.four_weeks_completions = get_four_weeks_completion_data()
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_get_currently_tracked_habits_service(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test the service method that CLI calls for getting active habits"""
        # Mock the HabitService to return our test habits
        mock_habit_service.return_value.get_all_habits.return_value = self.test_habits
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Call the service method (same as CLI does)
        result = analytics_service.get_currently_tracked_habits()
        
        # Should return all active habits (all test habits are active)
        self.assertEqual(len(result), 5)
        for habit in result:
            self.assertTrue(habit.is_active)
        
        # Verify it called the habit service
        mock_habit_service.return_value.get_all_habits.assert_called_once()
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_get_habits_with_same_periodicity_daily_service(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test the service method for getting daily habits (as CLI does)"""
        mock_habit_service.return_value.get_all_habits.return_value = self.test_habits
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Call the service method for daily habits
        result = analytics_service.get_habits_with_same_periodicity(HabitPeriod.DAILY)
        
        # Should return 3 daily habits (Exercise, Reading, Meditation)
        self.assertEqual(len(result), 3)
        for habit in result:
            self.assertEqual(habit.period, HabitPeriod.DAILY)
        
        habit_names = [h.habit_name for h in result]
        self.assertIn("Exercise", habit_names)
        self.assertIn("Read Books", habit_names)
        self.assertIn("Meditation", habit_names)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_get_habits_with_same_periodicity_weekly_service(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test the service method for getting weekly habits (as CLI does)"""
        mock_habit_service.return_value.get_all_habits.return_value = self.test_habits
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Call the service method for weekly habits
        result = analytics_service.get_habits_with_same_periodicity(HabitPeriod.WEEKLY)
        
        # Should return 2 weekly habits (House Cleaning, Grocery Shopping)
        self.assertEqual(len(result), 2)
        for habit in result:
            self.assertEqual(habit.period, HabitPeriod.WEEKLY)
        
        habit_names = [h.habit_name for h in result]
        self.assertIn("House Cleaning", habit_names)
        self.assertIn("Grocery Shopping", habit_names)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_get_longest_run_streak_for_habit_service(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test the service method for getting longest streak for a specific habit (as CLI does)"""
        # Mock the services
        exercise_habit = self.test_habits[0]  # Exercise habit (ID=1)
        mock_habit_service.return_value.get_habit_by_id.return_value = exercise_habit
        mock_completion_service.return_value.get_habit_completions.return_value = self.four_weeks_completions[1]
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Call the service method (same as CLI does)
        result = analytics_service.get_longest_run_streak_for_habit(habit_id=1)
        
        # Should return the perfect daily streak (28 days)
        self.assertEqual(result, PERFECT_DAILY_STREAK)
        
        # Verify service calls
        mock_habit_service.return_value.get_habit_by_id.assert_called_once_with(1)
        mock_completion_service.return_value.get_habit_completions.assert_called_once_with(1)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_get_current_streak_for_habit_service(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test the service method for getting current streak (as CLI does)"""
        # This is the function the CLI actually calls but wasn't tested before!
        exercise_habit = self.test_habits[0]  # Exercise habit (ID=1)
        mock_habit_service.return_value.get_habit_by_id.return_value = exercise_habit
        mock_completion_service.return_value.get_habit_completions.return_value = self.four_weeks_completions[1]
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Call the service method (same as CLI does)
        result = analytics_service.get_current_streak_for_habit(habit_id=1)
        
        # Should return the current streak (should be 28 for perfect completion)
        self.assertEqual(result, PERFECT_DAILY_STREAK)
        
        # Verify service calls
        mock_habit_service.return_value.get_habit_by_id.assert_called_once_with(1)
        mock_completion_service.return_value.get_habit_completions.assert_called_once_with(1)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_get_longest_run_streak_all_habits_service(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test the service method for getting the longest streak across all habits"""
        # Mock the services
        mock_habit_service.return_value.get_all_habits.return_value = self.test_habits
        
        # Mock completion service to return different completions for each habit
        def mock_get_completions(habit_id):
            return self.four_weeks_completions.get(habit_id, [])
        
        mock_completion_service.return_value.get_habit_completions.side_effect = mock_get_completions
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Call the service method
        result = analytics_service.get_longest_run_streak_all_habits()
        
        # Should return a dict with habit info and streak length
        self.assertIsInstance(result, dict)
        self.assertIn('habit', result)
        self.assertIn('habit_name', result)
        self.assertIn('streak_length', result)
        
        # Should return the Exercise habit with perfect streak
        self.assertEqual(result['habit_name'], "Exercise")
        self.assertEqual(result['streak_length'], PERFECT_DAILY_STREAK)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_service_handles_no_habits(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test service methods handle empty habit lists gracefully"""
        mock_habit_service.return_value.get_all_habits.return_value = []
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Test currently tracked habits with no habits
        result = analytics_service.get_currently_tracked_habits()
        self.assertEqual(len(result), 0)
        
        # Test habits by periodicity with no habits
        daily_result = analytics_service.get_habits_with_same_periodicity(HabitPeriod.DAILY)
        weekly_result = analytics_service.get_habits_with_same_periodicity(HabitPeriod.WEEKLY)
        self.assertEqual(len(daily_result), 0)
        self.assertEqual(len(weekly_result), 0)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_service_handles_habit_not_found(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test service methods handle non-existent habit IDs"""
        from backend.models import HabitNotFoundException
        
        # Mock habit service to raise exception for non-existent habit
        mock_habit_service.return_value.get_habit_by_id.side_effect = HabitNotFoundException("Habit not found")
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Should handle the exception gracefully
        with self.assertRaises(HabitNotFoundException):
            analytics_service.get_longest_run_streak_for_habit(habit_id=999)
        
        with self.assertRaises(HabitNotFoundException):
            analytics_service.get_current_streak_for_habit(habit_id=999)
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_service_handles_no_completions(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Test service methods handle habits with no completions"""
        # Mock habit exists but has no completions
        habit = self.test_habits[0]
        mock_habit_service.return_value.get_habit_by_id.return_value = habit
        mock_completion_service.return_value.get_habit_completions.return_value = []
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Should return 0 for both streak methods
        longest_streak = analytics_service.get_longest_run_streak_for_habit(habit_id=1)
        current_streak = analytics_service.get_current_streak_for_habit(habit_id=1)
        
        self.assertEqual(longest_streak, 0)
        self.assertEqual(current_streak, 0)


class TestCLIAnalyticsIntegration(unittest.TestCase):
    """Test cases that simulate actual CLI usage patterns"""
    
    def setUp(self):
        """Set up test data"""
        self.test_habits = get_test_habits()
        self.four_weeks_completions = get_four_weeks_completion_data()
    
    @patch('backend.services.HabitCompletionService')
    @patch('backend.services.HabitService')
    @patch('backend.services.UserService')
    def test_cli_analytics_dashboard_simulation(self, mock_user_service, mock_habit_service, mock_completion_service):
        """Simulate the exact sequence of calls the CLI makes in view_analytics()"""
        # Mock the services as they would be called by CLI
        mock_habit_service.return_value.get_all_habits.return_value = self.test_habits
        
        def mock_get_completions(habit_id):
            return self.four_weeks_completions.get(habit_id, [])
        
        mock_completion_service.return_value.get_habit_completions.side_effect = mock_get_completions
        
        # Create analytics service after mocking
        analytics_service = HabitAnalyticsService()
        
        # Simulate CLI analytics dashboard calls:
        
        # 1. Get currently tracked habits overview
        tracked_habits = analytics_service.get_currently_tracked_habits()
        self.assertEqual(len(tracked_habits), 5)
        
        # 2. Get habits by periodicity
        daily_habits = analytics_service.get_habits_with_same_periodicity(HabitPeriod.DAILY)
        weekly_habits = analytics_service.get_habits_with_same_periodicity(HabitPeriod.WEEKLY)
        self.assertEqual(len(daily_habits), 3)
        self.assertEqual(len(weekly_habits), 2)
        
        # 3. Get longest streaks for each habit (CLI loops through habits)
        for habit in daily_habits:
            streak = analytics_service.get_longest_run_streak_for_habit(habit.habit_id)
            self.assertIsInstance(streak, int)
            self.assertGreaterEqual(streak, 0)
        
        for habit in weekly_habits:
            streak = analytics_service.get_longest_run_streak_for_habit(habit.habit_id)
            self.assertIsInstance(streak, int)
            self.assertGreaterEqual(streak, 0)
        
        # 4. Get current streaks for individual habit table (CLI loops through all habits)
        for habit in tracked_habits:
            current_streak = analytics_service.get_current_streak_for_habit(habit.habit_id)
            self.assertIsInstance(current_streak, int)
            self.assertGreaterEqual(current_streak, 0)
        
        # All calls should complete without errors
        # This simulates the full analytics dashboard workflow


if __name__ == '__main__':
    # Run the service layer tests
    unittest.main(verbosity=2)
