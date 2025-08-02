"""
Analytics Module for Habit Tracker Application
Using functional programming paradigm as required by project specifications

This module provides the 4 essential pure functions for habit analysis:
1. Return list of currently tracked habits
2. Return list of habits with same periodicity
3. Return longest run streak of all habits
4. Return longest run streak for a given habit
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from backend.models import Habit, HabitCompletion, HabitPeriod


def get_currently_tracked_habits(habits: List[Habit]) -> List[Habit]:
    """
    Pure function: Return list of currently tracked (active) habits
    
    Args:
        habits: List of all habits
        
    Returns:
        List of active habits
    """
    return [habit for habit in habits if habit.is_active]


def get_habits_with_same_periodicity(habits: List[Habit], periodicity: HabitPeriod) -> List[Habit]:
    """
    Pure function: Return list of all habits with the same periodicity
    
    Args:
        habits: List of all habits
        periodicity: The periodicity to filter for (DAILY or WEEKLY)
        
    Returns:
        List of habits with matching periodicity
    """
    return [habit for habit in habits if habit.period == periodicity]


def get_longest_run_streak_all_habits(habits: List[Habit], completions_by_habit: Dict[int, List[HabitCompletion]]) -> Dict[str, Any]:
    """
    Pure function: Return longest run streak of all defined habits
    
    Args:
        habits: List of all habits
        completions_by_habit: Dictionary mapping habit_id to list of completions
        
    Returns:
        Dictionary containing habit info and longest streak length
    """
    longest_streak = 0
    best_habit = None
    
    for habit in habits:
        habit_completions = completions_by_habit.get(habit.habit_id, [])
        if habit_completions:
            streak = calculate_streak_length(habit_completions, habit.period)
            if streak > longest_streak:
                longest_streak = streak
                best_habit = habit
    
    return {
        'habit': best_habit,
        'streak_length': longest_streak,
        'habit_name': best_habit.habit_name if best_habit else None
    }


def get_longest_run_streak_for_habit(habit: Habit, completions: List[HabitCompletion]) -> int:
    """
    Pure function: Return longest run streak for a given habit
    
    Args:
        habit: The habit to analyze
        completions: List of completions for this habit
        
    Returns:
        Longest streak length for the given habit
    """
    return calculate_streak_length(completions, habit.period)


def calculate_streak_length(completions: List[HabitCompletion], period: HabitPeriod) -> int:
    """
    Pure function: Calculate the current streak length for a habit
    
    Args:
        completions: List of habit completions sorted by date
        period: The habit period (DAILY or WEEKLY)
        
    Returns:
        Current streak length
    """
    if not completions:
        return 0
    
    # Sort completions by date (most recent first)
    sorted_completions = sorted(completions, key=lambda x: x.completion_date, reverse=True)
    
    if period == HabitPeriod.DAILY:
        return _calculate_daily_streak(sorted_completions)
    else:  # WEEKLY
        return _calculate_weekly_streak(sorted_completions)


def _calculate_daily_streak(sorted_completions: List[HabitCompletion]) -> int:
    """
    Helper function: Calculate streak for daily habits
    """
    if not sorted_completions:
        return 0
    
    streak = 0
    expected_date = date.today()
    
    # Check if completed today, if not, check yesterday
    if sorted_completions[0].completion_date != expected_date:
        expected_date = expected_date - timedelta(days=1)
        if sorted_completions[0].completion_date != expected_date:
            return 0
    
    for completion in sorted_completions:
        if completion.completion_date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break
    
    return streak


def _calculate_weekly_streak(sorted_completions: List[HabitCompletion]) -> int:
    """
    Helper function: Calculate streak for weekly habits
    """
    if not sorted_completions:
        return 0
    
    streak = 0
    current_week_start = _get_week_start(date.today())
    
    completion_weeks = set()
    for completion in sorted_completions:
        week_start = _get_week_start(completion.completion_date)
        completion_weeks.add(week_start)
    
    # Check consecutive weeks backwards from current week
    check_week = current_week_start
    while check_week in completion_weeks:
        streak += 1
        check_week -= timedelta(weeks=1)
    
    return streak


def _get_week_start(date_obj: date) -> date:
    """
    Helper function: Get the start of the week (Monday) for a given date
    """
    days_since_monday = date_obj.weekday()
    return date_obj - timedelta(days=days_since_monday)
