"""
Basic tests for the Habit Tracker backend
Demonstrates unit testing as required by project specifications
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import date, datetime, timedelta
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.models import Habit, HabitCompletion, HabitPeriod, HabitAnalytics
from backend.analytics import (
    calculate_streak_length, 
    calculate_completion_rate,
    categorize_habit_difficulty,
    analyze_habit_trends
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
            notes="Completed successfully"
        )
        
        self.assertEqual(completion.habit_id, 1)
        self.assertEqual(completion.notes, "Completed successfully")
        self.assertIsNotNone(completion.completion_date)
        self.assertIsNotNone(completion.created_at)


class TestAnalyticsFunctions(unittest.TestCase):
    """Test cases for analytics functions (functional programming)"""
    
    def test_calculate_daily_streak(self):
        """Test calculating streak for daily habits"""
        # Create consecutive completion dates
        today = date.today()
        completion_dates = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3)
        ]
        
        streak = calculate_streak_length(completion_dates, "daily")
        self.assertEqual(streak, 4)
    
    def test_calculate_daily_streak_with_gap(self):
        """Test calculating streak with gaps"""
        today = date.today()
        completion_dates = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=3),  # Gap here
            today - timedelta(days=4)
        ]
        
        streak = calculate_streak_length(completion_dates, "daily")
        self.assertEqual(streak, 2)  # Only current streak
    
    def test_calculate_completion_rate(self):
        """Test completion rate calculation"""
        # Mock completions for testing
        mock_completions = [MagicMock() for _ in range(7)]  # 7 completions
        
        # Test daily habit over 10 days
        rate = calculate_completion_rate(mock_completions, "daily", 10)
        self.assertEqual(rate, 70.0)  # 7/10 * 100
        
        # Test weekly habit over 14 days (2 weeks)
        rate = calculate_completion_rate(mock_completions, "weekly", 14)
        self.assertEqual(rate, 350.0)  # 7/2 * 100 (capped in real implementation)
    
    def test_categorize_habit_difficulty(self):
        """Test habit difficulty categorization"""
        self.assertEqual(categorize_habit_difficulty(95.0), "Very Easy")
        self.assertEqual(categorize_habit_difficulty(80.0), "Easy")
        self.assertEqual(categorize_habit_difficulty(65.0), "Moderate")
        self.assertEqual(categorize_habit_difficulty(45.0), "Challenging")
        self.assertEqual(categorize_habit_difficulty(25.0), "Difficult")
        self.assertEqual(categorize_habit_difficulty(15.0), "Very Difficult")
    
    def test_analyze_habit_trends(self):
        """Test trend analysis function"""
        # Improving trend
        improving_data = [2, 3, 4, 5, 6]
        result = analyze_habit_trends(improving_data)
        self.assertEqual(result['trend'], 'improving')
        self.assertGreater(result['slope'], 0)
        
        # Declining trend
        declining_data = [6, 5, 4, 3, 2]
        result = analyze_habit_trends(declining_data)
        self.assertEqual(result['trend'], 'declining')
        self.assertLess(result['slope'], 0)
        
        # Stable trend
        stable_data = [5, 5, 5, 5, 5]
        result = analyze_habit_trends(stable_data)
        self.assertEqual(result['trend'], 'stable')


class TestHabitAnalytics(unittest.TestCase):
    """Test cases for HabitAnalytics model"""
    
    def test_analytics_difficulty_level(self):
        """Test difficulty level calculation"""
        analytics = HabitAnalytics(
            habit_id=1,
            habit_name="Test Habit",
            period="daily",
            completion_rate=85.0
        )
        
        self.assertEqual(analytics.get_difficulty_level(), "Easy")
    
    def test_analytics_consistency_score(self):
        """Test consistency score calculation"""
        analytics = HabitAnalytics(
            habit_id=1,
            habit_name="Test Habit", 
            period="daily",
            completion_rate=92.0,
            current_streak=10
        )
        
        self.assertEqual(analytics.get_consistency_score(), "Excellent")


class TestServiceIntegration(unittest.TestCase):
    """Integration tests for services (if backend is available)"""
    
    def setUp(self):
        """Set up test environment"""
        try:
            from backend.services import SystemService
            self.system_service = SystemService()
            self.backend_available = True
        except ImportError:
            self.backend_available = False
            self.skipTest("Backend services not available")
    
    def test_system_status(self):
        """Test system status check"""
        if not self.backend_available:
            self.skipTest("Backend not available")
        
        status = self.system_service.get_system_status()
        self.assertIn('status', status)
        self.assertIn('system_initialized', status)




if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestHabitModels))
    test_suite.addTest(unittest.makeSuite(TestAnalyticsFunctions))
    test_suite.addTest(unittest.makeSuite(TestHabitAnalytics))
    
    # Add integration tests if backend is available
    try:
        from backend.services import SystemService
        test_suite.addTest(unittest.makeSuite(TestServiceIntegration))
    except ImportError:
        print("⚠️  Backend services not available - skipping integration tests")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")
        sys.exit(1)
