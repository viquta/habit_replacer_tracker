"""
Analytics Module for Habit Tracker Application
Using functional programming paradigm as required by project specifications

This module provides essential pure functions for habit analysis and statistics
without side effects, following functional programming principles.
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date, timedelta
import statistics
from backend.models import Habit, HabitCompletion, HabitAnalytics


# Type aliases for better code readability
HabitData = Dict[str, Any]
CompletionList = List[HabitCompletion]
AnalyticsResult = Dict[str, Any]


# Essential pure functions for analytics

def calculate_streak_length(completion_dates: List[date], habit_period: str) -> int:
    """
    Calculate current streak length from completion dates - pure function
    Uses functional approach to find consecutive dates
    """
    if not completion_dates:
        return 0
    
    # Sort dates in descending order (most recent first)
    sorted_dates = sorted(completion_dates, reverse=True)
    
    today = date.today()
    streak = 0
    
    if habit_period == 'daily':
        expected_date = today
        for completion_date in sorted_dates:
            if completion_date == expected_date:
                streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
    else:  # weekly
        # For weekly habits, check if completed in current week and previous weeks
        current_week_start = today - timedelta(days=today.weekday())
        week_start = current_week_start
        
        for completion_date in sorted_dates:
            week_end = week_start + timedelta(days=6)
            if week_start <= completion_date <= week_end:
                streak += 1
                week_start -= timedelta(days=7)  # Move to previous week
            else:
                break
    
    return streak


def find_longest_streak(completion_dates: List[date], habit_period: str) -> Tuple[int, Optional[date], Optional[date]]:
    """
    Find the longest streak in the completion history - pure function
    Returns (streak_length, start_date, end_date)
    """
    if not completion_dates:
        return 0, None, None
    
    sorted_dates = sorted(completion_dates)
    
    if habit_period == 'daily':
        return _find_longest_daily_streak(sorted_dates)
    else:  # weekly
        return _find_longest_weekly_streak(sorted_dates)


def _find_longest_daily_streak(sorted_dates: List[date]) -> Tuple[int, Optional[date], Optional[date]]:
    """Find longest consecutive daily streak - pure function"""
    if not sorted_dates:
        return 0, None, None
    
    max_streak = 1
    current_streak = 1
    max_start = sorted_dates[0]
    max_end = sorted_dates[0]
    current_start = sorted_dates[0]
    
    for i in range(1, len(sorted_dates)):
        expected_date = sorted_dates[i-1] + timedelta(days=1)
        
        if sorted_dates[i] == expected_date:
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
                max_start = current_start
                max_end = sorted_dates[i-1]
            current_streak = 1
            current_start = sorted_dates[i]
    
    # Check final streak
    if current_streak > max_streak:
        max_streak = current_streak
        max_start = current_start
        max_end = sorted_dates[-1]
    
    return max_streak, max_start, max_end


def _find_longest_weekly_streak(sorted_dates: List[date]) -> Tuple[int, Optional[date], Optional[date]]:
    """Find longest consecutive weekly streak - pure function"""
    if not sorted_dates:
        return 0, None, None
    
    # Group dates by week
    weeks = {}
    for d in sorted_dates:
        week_start = d - timedelta(days=d.weekday())
        weeks[week_start] = d
    
    week_starts = sorted(weeks.keys())
    
    if len(week_starts) <= 1:
        return len(week_starts), sorted_dates[0] if sorted_dates else None, sorted_dates[-1] if sorted_dates else None
    
    max_streak = 1
    current_streak = 1
    max_start_week = week_starts[0]
    max_end_week = week_starts[0]
    current_start_week = week_starts[0]
    
    for i in range(1, len(week_starts)):
        expected_week = week_starts[i-1] + timedelta(days=7)
        
        if week_starts[i] == expected_week:
            current_streak += 1
        else:
            if current_streak > max_streak:
                max_streak = current_streak
                max_start_week = current_start_week
                max_end_week = week_starts[i-1]
            current_streak = 1
            current_start_week = week_starts[i]
    
    # Check final streak
    if current_streak > max_streak:
        max_streak = current_streak
        max_start_week = current_start_week
        max_end_week = week_starts[-1]
    
    return max_streak, weeks[max_start_week], weeks[max_end_week]


def calculate_completion_rate(completions: CompletionList, habit_period: str, days_analyzed: int) -> float:
    """
    Calculate completion rate as a percentage - pure function
    """
    if days_analyzed <= 0:
        return 0.0
    
    actual_completions = len(completions)
    
    if habit_period == 'daily':
        expected_completions = days_analyzed
    else:  # weekly
        expected_completions = max(1, days_analyzed // 7)
    
    return (actual_completions / expected_completions) * 100 if expected_completions > 0 else 0.0


# Main analytics pipeline function (used by CLI)
def analyze_habits_comprehensive(habits: List[Habit], 
                               all_completions: List[HabitCompletion],
                               analysis_period_days: int = 28) -> AnalyticsResult:
    """
    Comprehensive habit analysis using functional programming pipeline
    Pure function that processes all data without side effects
    """
    # Group completions by habit
    completions_by_habit = {}
    for completion in all_completions:
        if completion.habit_id not in completions_by_habit:
            completions_by_habit[completion.habit_id] = []
        completions_by_habit[completion.habit_id].append(completion)
    
    # Calculate analytics for each active habit
    habits_analytics = []
    
    for habit in habits:
        if not habit.is_active:
            continue
            
        habit_completions = completions_by_habit.get(habit.habit_id, [])
        
        # Filter completions to analysis period
        end_date = date.today()
        start_date = end_date - timedelta(days=analysis_period_days)
        period_completions = [
            c for c in habit_completions 
            if start_date <= c.completion_date <= end_date
        ]
        
        # Extract completion dates
        all_completion_dates = [comp.completion_date for comp in habit_completions]
        
        current_streak = calculate_streak_length(all_completion_dates, habit.period.value)
        longest_streak, streak_start, streak_end = find_longest_streak(
            all_completion_dates, habit.period.value
        )
        completion_rate = calculate_completion_rate(
            period_completions, habit.period.value, analysis_period_days
        )
        
        analytics = HabitAnalytics(
            habit_id=habit.habit_id,
            habit_name=habit.habit_name,
            period=habit.period.value,
            current_streak=current_streak,
            longest_streak=longest_streak,
            total_completions=len(period_completions),
            completion_rate=completion_rate,
            longest_streak_start=streak_start,
            longest_streak_end=streak_end
        )
        
        habits_analytics.append(analytics)
    
    # Basic summary statistics
    if habits_analytics:
        avg_completion_rate = statistics.mean([h.completion_rate for h in habits_analytics])
        max_current_streak = max([h.current_streak for h in habits_analytics])
        max_longest_streak = max([h.longest_streak for h in habits_analytics])
        total_completions = sum([h.total_completions for h in habits_analytics])
    else:
        avg_completion_rate = 0.0
        max_current_streak = 0
        max_longest_streak = 0
        total_completions = 0
    
    return {
        'summary': {
            'total_habits': len(habits_analytics),
            'average_completion_rate': avg_completion_rate,
            'highest_current_streak': max_current_streak,
            'highest_all_time_streak': max_longest_streak,
            'total_completions': total_completions
        },
        'individual_analytics': habits_analytics,
        'analysis_period_days': analysis_period_days,
        'generated_at': datetime.now().isoformat()
    }
