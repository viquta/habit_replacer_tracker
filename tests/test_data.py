"""
Test Data Module for Habit Tracker Application
Provides 4 weeks worth of predefined habit data for unit testing

This module contains time-series data for testing analytics functions,
especially streak calculations respecting habit periodicity.
"""
from datetime import date, timedelta
from backend.models import Habit, HabitCompletion, HabitPeriod


def get_test_habits():
    """
    Returns a list of predefined test habits with different periodicities
    
    Returns:
        List[Habit]: Test habits with IDs 1-5
    """
    return [
        # Daily habits
        Habit(
            habit_id=1,
            habit_name="Exercise",
            description="30 minutes of physical exercise",
            period=HabitPeriod.DAILY,
            is_active=True
        ),
        Habit(
            habit_id=2,
            habit_name="Read Books",
            description="Read for at least 20 minutes",
            period=HabitPeriod.DAILY,
            is_active=True
        ),
        Habit(
            habit_id=3,
            habit_name="Meditation",
            description="10 minutes of mindfulness meditation",
            period=HabitPeriod.DAILY,
            is_active=True
        ),
        
        # Weekly habits
        Habit(
            habit_id=4,
            habit_name="House Cleaning",
            description="Deep clean the house",
            period=HabitPeriod.WEEKLY,
            is_active=True
        ),
        Habit(
            habit_id=5,
            habit_name="Grocery Shopping",
            description="Weekly grocery shopping",
            period=HabitPeriod.WEEKLY,
            is_active=True
        )
    ]


def get_four_weeks_completion_data():
    """
    Returns 4 weeks worth of completion data for test habits
    
    This data includes:
    - Perfect streaks (every day/week completed)
    - Broken streaks (missed days/weeks)
    - Improving patterns (getting better over time)
    - Declining patterns (getting worse over time)
    
    Returns:
        Dict[int, List[HabitCompletion]]: Completions by habit_id
    """
    today = date.today()
    four_weeks_ago = today - timedelta(days=28)
    
    completions_by_habit = {}
    
    # Habit 1: Exercise (Daily) - Perfect consistency (28/28 days)
    exercise_completions = []
    for i in range(28):
        completion_date = four_weeks_ago + timedelta(days=i)
        exercise_completions.append(
            HabitCompletion(
                habit_id=1,
                completion_date=completion_date,
                notes=f"Day {i+1} - Feeling strong!"
            )
        )
    completions_by_habit[1] = exercise_completions
    
    # Habit 2: Read Books (Daily) - Good consistency with some gaps (22/28 days)
    reading_completions = []
    reading_dates = [
        # Week 1: 5/7 days
        0, 1, 2, 4, 6,
        # Week 2: 6/7 days  
        7, 8, 9, 10, 11, 13,
        # Week 3: 6/7 days
        14, 15, 16, 17, 19, 20,
        # Week 4: 5/7 days
        21, 22, 23, 25, 27
    ]
    for day_offset in reading_dates:
        completion_date = four_weeks_ago + timedelta(days=day_offset)
        reading_completions.append(
            HabitCompletion(
                habit_id=2,
                completion_date=completion_date,
                notes=f"Reading day {day_offset + 1}"
            )
        )
    completions_by_habit[2] = reading_completions
    
    # Habit 3: Meditation (Daily) - Improving pattern (8 -> 10 -> 12 -> 14 days per week trend)
    meditation_completions = []
    meditation_dates = [
        # Week 1: Poor (2/7 days)
        1, 4,
        # Week 2: Better (4/7 days)
        8, 10, 12, 13,
        # Week 3: Good (5/7 days)
        14, 16, 17, 19, 20,
        # Week 4: Excellent (6/7 days)
        21, 22, 24, 25, 26, 27
    ]
    for day_offset in meditation_dates:
        completion_date = four_weeks_ago + timedelta(days=day_offset)
        meditation_completions.append(
            HabitCompletion(
                habit_id=3,
                completion_date=completion_date,
                notes=f"Meditation session {day_offset + 1}"
            )
        )
    completions_by_habit[3] = meditation_completions
    
    # Habit 4: House Cleaning (Weekly) - Perfect consistency (4/4 weeks)
    cleaning_completions = []
    for week in range(4):
        # Complete on different days of each week to test weekly grouping
        completion_date = four_weeks_ago + timedelta(days=week * 7 + week)  # Day 0, 8, 16, 24
        cleaning_completions.append(
            HabitCompletion(
                habit_id=4,
                completion_date=completion_date,
                notes=f"Week {week + 1} deep clean"
            )
        )
    completions_by_habit[4] = cleaning_completions
    
    # Habit 5: Grocery Shopping (Weekly) - Missed one week (3/4 weeks)
    shopping_completions = []
    shopping_weeks = [0, 1, 3]  # Missed week 2
    for week in shopping_weeks:
        completion_date = four_weeks_ago + timedelta(days=week * 7 + 2)  # Always on "Tuesday"
        shopping_completions.append(
            HabitCompletion(
                habit_id=5,
                completion_date=completion_date,
                notes=f"Week {week + 1} grocery run"
            )
        )
    completions_by_habit[5] = shopping_completions
    
    return completions_by_habit


def get_broken_streak_data():
    """
    Returns data specifically designed to test broken streak scenarios
    
    Returns:
        Dict[int, List[HabitCompletion]]: Completions with intentional gaps
    """
    today = date.today()
    
    # Daily habit with a recent break in streak
    daily_completions = []
    # 10 day streak, then 2 day gap, then current 3 day streak
    for i in range(10):
        completion_date = today - timedelta(days=15 - i)
        daily_completions.append(
            HabitCompletion(
                habit_id=101,
                completion_date=completion_date,
                notes=f"Streak day {i+1}"
            )
        )
    
    # Gap of 2 days (days -4 and -3 missing)
    
    # Current streak
    for i in range(3):
        completion_date = today - timedelta(days=2 - i)
        daily_completions.append(
            HabitCompletion(
                habit_id=101,
                completion_date=completion_date,
                notes=f"New streak day {i+1}"
            )
        )
    
    return {101: daily_completions}


def get_edge_case_data():
    """
    Returns data for testing edge cases in streak calculations
    
    Returns:
        Dict[int, List[HabitCompletion]]: Edge case scenarios
    """
    today = date.today()
    
    return {
        # Habit with only one completion
        201: [HabitCompletion(habit_id=201, completion_date=today, notes="Single completion")],
        
        # Habit with no completions
        202: [],
        
        # Habit completed only today
        203: [HabitCompletion(habit_id=203, completion_date=today, notes="Just started")],
        
        # Habit last completed yesterday (current streak = 0)
        204: [HabitCompletion(habit_id=204, completion_date=today - timedelta(days=1), notes="Yesterday only")],
        
        # Weekly habit completed multiple times in same week (should count as one week)
        205: [
            HabitCompletion(habit_id=205, completion_date=today, notes="Today"),
            HabitCompletion(habit_id=205, completion_date=today - timedelta(days=1), notes="Yesterday"),
            HabitCompletion(habit_id=205, completion_date=today - timedelta(days=2), notes="Two days ago")
        ]
    }


def get_all_test_data():
    """
    Returns all test data combined for comprehensive testing
    
    Returns:
        Tuple[List[Habit], Dict[int, List[HabitCompletion]]]: All habits and completions
    """
    habits = get_test_habits()
    completions = get_four_weeks_completion_data()
    
    # Add broken streak and edge case data
    completions.update(get_broken_streak_data())
    completions.update(get_edge_case_data())
    
    # Add corresponding habits for edge cases
    edge_case_habits = [
        Habit(habit_id=101, habit_name="Broken Streak Test", period=HabitPeriod.DAILY),
        Habit(habit_id=201, habit_name="Single Completion", period=HabitPeriod.DAILY),
        Habit(habit_id=202, habit_name="No Completions", period=HabitPeriod.DAILY),
        Habit(habit_id=203, habit_name="Just Started", period=HabitPeriod.DAILY),
        Habit(habit_id=204, habit_name="Yesterday Only", period=HabitPeriod.DAILY),
        Habit(habit_id=205, habit_name="Multiple Same Week", period=HabitPeriod.WEEKLY),
    ]
    
    all_habits = habits + edge_case_habits
    
    return all_habits, completions


# Constants for testing
FOUR_WEEKS_DAYS = 28
PERFECT_DAILY_STREAK = 28
PERFECT_WEEKLY_STREAK = 4
GOOD_DAILY_STREAK = 22
IMPROVING_DAILY_PATTERN = [2, 4, 5, 6]  # Completions per week
MISSED_ONE_WEEKLY = 3
