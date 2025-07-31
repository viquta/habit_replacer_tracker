"""
Analytics Module for Habit Tracker Application
Using functional programming paradigm as required by project specifications

This module provides pure functions for habit analysis and statistics
without side effects, following functional programming principles.
"""
from typing import List, Dict, Any, Callable, Optional, Tuple
from datetime import datetime, date, timedelta
from functools import reduce, partial
from itertools import groupby
from collections import defaultdict
import statistics
from backend.models import Habit, HabitCompletion, HabitAnalytics, HabitPeriod


# Type aliases for better code readability
HabitData = Dict[str, Any]
CompletionList = List[HabitCompletion]
AnalyticsResult = Dict[str, Any]


# Pure functions for data transformation and analysis

def map_habits_to_data(habits: List[Habit]) -> List[HabitData]:
    """
    Transform habit objects to dictionaries for functional processing
    Pure function with no side effects
    """
    return [
        {
            'habit_id': habit.habit_id,
            'name': habit.habit_name,
            'description': habit.description,
            'period': habit.period.value,
            'created_date': habit.created_date,
            'is_active': habit.is_active
        }
        for habit in habits
    ]


def filter_active_habits(habit_data_list: List[HabitData]) -> List[HabitData]:
    """Filter only active habits - pure function"""
    return list(filter(lambda h: h['is_active'], habit_data_list))


def filter_habits_by_period(period: str) -> Callable[[List[HabitData]], List[HabitData]]:
    """Higher-order function that returns a filter function for habit periods"""
    return lambda habits: list(filter(lambda h: h['period'] == period, habits))


def group_completions_by_habit(completions: CompletionList) -> Dict[int, CompletionList]:
    """
    Group completions by habit_id using functional approach
    Pure function with no side effects
    """
    completion_groups = defaultdict(list)
    for completion in completions:
        completion_groups[completion.habit_id].append(completion)
    return dict(completion_groups)


def calculate_completion_dates(completions: CompletionList) -> List[date]:
    """Extract completion dates from completion objects - pure function"""
    return [comp.completion_date for comp in completions]


def count_completions_in_range(completions: CompletionList, start_date: date, end_date: date) -> int:
    """
    Count completions within a date range - pure function
    """
    in_range = filter(
        lambda comp: start_date <= comp.completion_date <= end_date,
        completions
    )
    return len(list(in_range))


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


def calculate_average_completions_per_week(completions: CompletionList, weeks_analyzed: int) -> float:
    """Calculate average completions per week - pure function"""
    if weeks_analyzed <= 0:
        return 0.0
    
    return len(completions) / weeks_analyzed


def categorize_habit_difficulty(completion_rate: float) -> str:
    """
    Categorize habit difficulty based on completion rate - pure function
    Follows app philosophy: higher completion rate = easier habit
    """
    if completion_rate >= 90:
        return "Very Easy"
    elif completion_rate >= 75:
        return "Easy"
    elif completion_rate >= 60:
        return "Moderate"
    elif completion_rate >= 40:
        return "Challenging"
    elif completion_rate >= 20:
        return "Difficult"
    else:
        return "Very Difficult"


def rank_habits_by_metric(habits_analytics: List[HabitAnalytics], 
                         metric_func: Callable[[HabitAnalytics], float],
                         descending: bool = True) -> List[HabitAnalytics]:
    """
    Higher-order function to rank habits by any metric - pure function
    """
    return sorted(habits_analytics, key=metric_func, reverse=descending)


# Specific ranking functions using partial application
rank_by_completion_rate = partial(rank_habits_by_metric, 
                                 metric_func=lambda h: h.completion_rate)
rank_by_current_streak = partial(rank_habits_by_metric, 
                                metric_func=lambda h: h.current_streak)
rank_by_longest_streak = partial(rank_habits_by_metric, 
                                metric_func=lambda h: h.longest_streak)


def aggregate_analytics_summary(habits_analytics: List[HabitAnalytics]) -> AnalyticsResult:
    """
    Aggregate analytics across all habits using functional programming - pure function
    """
    if not habits_analytics:
        return {
            'total_habits': 0,
            'average_completion_rate': 0.0,
            'total_active_streaks': 0,
            'highest_streak': 0,
            'total_completions': 0
        }
    
    # Use functional approach to calculate aggregates
    completion_rates = [h.completion_rate for h in habits_analytics]
    current_streaks = [h.current_streak for h in habits_analytics]
    longest_streaks = [h.longest_streak for h in habits_analytics]
    total_completions = [h.total_completions for h in habits_analytics]
    
    return {
        'total_habits': len(habits_analytics),
        'average_completion_rate': statistics.mean(completion_rates),
        'median_completion_rate': statistics.median(completion_rates),
        'total_active_streaks': sum(filter(lambda x: x > 0, current_streaks)),
        'highest_current_streak': max(current_streaks, default=0),
        'highest_all_time_streak': max(longest_streaks, default=0),
        'total_completions': sum(total_completions),
        'habits_with_active_streaks': len(list(filter(lambda x: x > 0, current_streaks)))
    }


def analyze_habit_trends(completions_by_week: List[int]) -> AnalyticsResult:
    """
    Analyze trends in habit completion over time - pure function
    """
    if len(completions_by_week) < 2:
        return {'trend': 'insufficient_data', 'change': 0.0}
    
    # Calculate trend using linear regression approach
    n = len(completions_by_week)
    x_values = list(range(n))
    y_values = completions_by_week
    
    # Simple linear regression calculation
    x_mean = statistics.mean(x_values)
    y_mean = statistics.mean(y_values)
    
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
    denominator = sum((x - x_mean) ** 2 for x in x_values)
    
    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator
    
    # Determine trend direction
    if slope > 0.1:
        trend = 'improving'
    elif slope < -0.1:
        trend = 'declining'
    else:
        trend = 'stable'
    
    # Calculate percentage change from first to last period
    if completions_by_week[0] > 0:
        change = ((completions_by_week[-1] - completions_by_week[0]) / completions_by_week[0]) * 100
    else:
        change = 0.0
    
    return {
        'trend': trend,
        'slope': slope,
        'change_percentage': change,
        'recent_average': statistics.mean(completions_by_week[-3:]) if len(completions_by_week) >= 3 else y_mean
    }


def identify_pattern_insights(habits_analytics: List[HabitAnalytics]) -> List[str]:
    """
    Generate insights about habit patterns using functional analysis - pure function
    """
    insights = []
    
    if not habits_analytics:
        return ["No habits to analyze"]
    
    # Group habits by period
    daily_habits = list(filter(lambda h: h.period == 'daily', habits_analytics))
    weekly_habits = list(filter(lambda h: h.period == 'weekly', habits_analytics))
    
    if daily_habits:
        daily_avg_rate = statistics.mean([h.completion_rate for h in daily_habits])
        insights.append(f"Daily habits average completion rate: {daily_avg_rate:.1f}%")
        
        if daily_avg_rate > 75:
            insights.append("🎉 You're doing great with daily habits!")
        elif daily_avg_rate < 50:
            insights.append("💪 Daily habits need more attention - consider starting smaller")
    
    if weekly_habits:
        weekly_avg_rate = statistics.mean([h.completion_rate for h in weekly_habits])
        insights.append(f"Weekly habits average completion rate: {weekly_avg_rate:.1f}%")
        
        if weekly_avg_rate > daily_avg_rate if daily_habits else 0:
            insights.append("📅 You seem to handle weekly habits better than daily ones")
    
    # Find patterns in difficulty
    difficult_habits = list(filter(lambda h: h.completion_rate < 40, habits_analytics))
    if len(difficult_habits) > len(habits_analytics) / 2:
        insights.append("🔍 Consider reviewing your habit difficulty - many seem challenging")
    
    # Streak insights
    habits_with_streaks = list(filter(lambda h: h.current_streak > 0, habits_analytics))
    if habits_with_streaks:
        avg_streak = statistics.mean([h.current_streak for h in habits_with_streaks])
        insights.append(f"🔥 Average active streak length: {avg_streak:.1f}")
    
    return insights


def generate_recommendations(habits_analytics: List[HabitAnalytics]) -> List[str]:
    """
    Generate recommendations based on habit analytics - pure function
    """
    recommendations = []
    
    if not habits_analytics:
        return ["Start by creating your first habit!"]
    
    # Find habits that need attention
    struggling_habits = list(filter(lambda h: h.completion_rate < 30, habits_analytics))
    if struggling_habits:
        habit_names = [h.habit_name for h in struggling_habits[:2]]  # Top 2 most difficult
        recommendations.append(f"Focus on: {', '.join(habit_names)} - they need the most attention")
    
    # Find habits doing well
    successful_habits = list(filter(lambda h: h.completion_rate > 80, habits_analytics))
    if successful_habits:
        recommendations.append(f"Keep up the great work with {len(successful_habits)} successful habits!")
    
    # Streak recommendations
    no_streak_habits = list(filter(lambda h: h.current_streak == 0, habits_analytics))
    if no_streak_habits:
        recommendations.append("Start building momentum - pick one habit to focus on this week")
    
    # Balance recommendations
    daily_count = len(list(filter(lambda h: h.period == 'daily', habits_analytics)))
    weekly_count = len(list(filter(lambda h: h.period == 'weekly', habits_analytics)))
    
    if daily_count > weekly_count * 3:
        recommendations.append("Consider adding some weekly habits for variety")
    elif weekly_count > daily_count * 2:
        recommendations.append("Daily habits can help build consistent routines")
    
    return recommendations[:5]  # Limit to top 5 recommendations


# Main analytics pipeline function
def analyze_habits_comprehensive(habits: List[Habit], 
                               all_completions: List[HabitCompletion],
                               analysis_period_days: int = 28) -> AnalyticsResult:
    """
    Comprehensive habit analysis using functional programming pipeline
    Pure function that processes all data without side effects
    """
    # Transform data using functional approach
    habit_data = map_habits_to_data(habits)
    active_habits = filter_active_habits(habit_data)
    
    # Group completions by habit
    completions_by_habit = group_completions_by_habit(all_completions)
    
    # Calculate analytics for each habit
    habits_analytics = []
    
    for habit_info in active_habits:
        habit_id = habit_info['habit_id']
        habit_completions = completions_by_habit.get(habit_id, [])
        
        # Filter completions to analysis period
        end_date = date.today()
        start_date = end_date - timedelta(days=analysis_period_days)
        period_completions = list(filter(
            lambda c: start_date <= c.completion_date <= end_date,
            habit_completions
        ))
        
        completion_dates = calculate_completion_dates(period_completions)
        current_streak = calculate_streak_length(
            calculate_completion_dates(habit_completions), 
            habit_info['period']
        )
        longest_streak, streak_start, streak_end = find_longest_streak(
            calculate_completion_dates(habit_completions),
            habit_info['period']
        )
        completion_rate = calculate_completion_rate(
            period_completions, 
            habit_info['period'], 
            analysis_period_days
        )
        
        analytics = HabitAnalytics(
            habit_id=habit_id,
            habit_name=habit_info['name'],
            period=habit_info['period'],
            current_streak=current_streak,
            longest_streak=longest_streak,
            total_completions=len(period_completions),
            completion_rate=completion_rate,
            longest_streak_start=streak_start,
            longest_streak_end=streak_end
        )
        
        habits_analytics.append(analytics)
    
    # Generate comprehensive analysis
    summary = aggregate_analytics_summary(habits_analytics)
    insights = identify_pattern_insights(habits_analytics)
    recommendations = generate_recommendations(habits_analytics)
    
    # Rankings
    by_completion_rate = rank_by_completion_rate(habits_analytics)
    by_current_streak = rank_by_current_streak(habits_analytics)
    by_longest_streak = rank_by_longest_streak(habits_analytics)
    
    return {
        'summary': summary,
        'individual_analytics': habits_analytics,
        'insights': insights,
        'recommendations': recommendations,
        'rankings': {
            'by_completion_rate': by_completion_rate[:5],
            'by_current_streak': by_current_streak[:5],
            'by_longest_streak': by_longest_streak[:5]
        },
        'analysis_period_days': analysis_period_days,
        'generated_at': datetime.now().isoformat()
    }
