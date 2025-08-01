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

def calculate_habit_persistence_probability(completion_dates: List[date], 
                                         habit_period: str,
                                         weeks_analyzed: int = 4) -> Dict[str, float]:
    """
    Calculate probability that a habit will stick based on completion patterns
    Uses statistical models based on habit formation research
    """
    if not completion_dates or weeks_analyzed < 2:
        return {'probability': 0.0, 'confidence': 'low', 'factors': {}}
    
    # Week-by-week completion rates
    weekly_rates = _calculate_weekly_completion_rates(completion_dates, habit_period, weeks_analyzed)
    
    if not weekly_rates:
        return {'probability': 0.0, 'confidence': 'low', 'factors': {}}
    
    # Trend analysis (improving, declining, stable)
    trend_score = _calculate_trend_score(weekly_rates)
    
    # Consistency score (less variance = higher probability)
    consistency_score = _calculate_consistency_score(weekly_rates)
    
    # Recent performance weight (last 2 weeks matter more)
    recent_performance = _calculate_recent_performance_weight(weekly_rates)
    
    # Combined probability model
    base_probability = sum(weekly_rates) / len(weekly_rates) / 100  # Base completion rate
    trend_modifier = trend_score * 0.3  # Positive trend increases probability
    consistency_modifier = consistency_score * 0.2  # Consistency increases probability  
    recency_modifier = recent_performance * 0.3  # Recent success increases probability
    
    final_probability = min(0.95, max(0.05, 
        base_probability + trend_modifier + consistency_modifier + recency_modifier
    ))
    
    return {
        'probability': final_probability,
        'confidence': _determine_confidence_level(len(completion_dates), weeks_analyzed),
        'factors': {
            'base_completion_rate': base_probability,
            'trend_impact': trend_modifier,
            'consistency_impact': consistency_modifier,
            'recent_performance_impact': recency_modifier
        },
        'weekly_rates': weekly_rates,
        'trend_direction': 'improving' if trend_score > 0.1 else 'declining' if trend_score < -0.1 else 'stable'
    }


def predict_habit_difficulty(habit: Habit, completion_history: List[HabitCompletion]) -> Dict[str, Any]:
    """
    Predict how difficult a habit will be based on early performance patterns
    """
    if len(completion_history) < 7:  # Need at least a week of data
        return {'prediction': 'insufficient_data', 'confidence': 'low'}
    
    completion_dates = [c.completion_date for c in completion_history]
    
    # Early performance indicators
    first_week_rate = _calculate_completion_rate_for_period(
        completion_dates[:7], habit.period.value, 7
    )
    dropout_risk = _calculate_dropout_risk_score(completion_dates)
    variability = _calculate_performance_variability(completion_dates)
    
    # Difficulty prediction model
    if first_week_rate >= 85 and dropout_risk < 0.3:
        difficulty = 'easy'
    elif first_week_rate >= 65 and dropout_risk < 0.5:
        difficulty = 'moderate'  
    elif first_week_rate >= 45:
        difficulty = 'challenging'
    else:
        difficulty = 'difficult'
    
    return {
        'predicted_difficulty': difficulty,
        'early_performance_rate': first_week_rate,
        'dropout_risk_score': dropout_risk,
        'performance_variability': variability,
        'recommendations': _generate_difficulty_recommendations(difficulty, dropout_risk),
        'confidence': 'high' if len(completion_history) >= 14 else 'medium'
    }


def predict_streak_continuation(completion_dates: List[date], 
                              habit_period: str,
                              current_streak: int) -> Dict[str, Any]:
    """
    Predict likelihood of continuing current streak
    """
    if current_streak == 0:
        return {'probability': 0.0, 'reason': 'no_active_streak'}
    
    if len(completion_dates) < 7:
        return {'probability': 0.5, 'reason': 'insufficient_data', 'confidence': 'low'}
    
    # Historical streak analysis
    historical_streaks = _find_all_historical_streaks(completion_dates, habit_period)
    
    # Streak length vs continuation probability (longer streaks more likely to continue)
    length_factor = min(0.9, current_streak / 21)  # 21-day habit formation
    
    # Historical performance at this streak length
    historical_factor = _calculate_historical_continuation_rate(
        historical_streaks, current_streak
    )
    
    # Recent completion consistency
    recent_dates = completion_dates[-14:] if len(completion_dates) >= 14 else completion_dates
    recent_consistency = _calculate_recent_consistency(recent_dates, habit_period)
    
    continuation_probability = (length_factor * 0.4 + historical_factor * 0.4 + recent_consistency * 0.2)
    
    return {
        'continuation_probability': continuation_probability,
        'current_streak_length': current_streak,
        'streak_momentum': 'strong' if continuation_probability > 0.7 else 'moderate' if continuation_probability > 0.4 else 'weak',
        'factors': {
            'length_advantage': length_factor,
            'historical_performance': historical_factor,
            'recent_consistency': recent_consistency
        },
        'milestone_predictions': _predict_milestone_achievements(current_streak, continuation_probability),
        'confidence': 'high' if len(completion_dates) >= 21 else 'medium'
    }


# Helper functions for analytics calculations

def _calculate_weekly_completion_rates(completion_dates: List[date], habit_period: str, weeks_back: int = 4) -> List[float]:
    """Calculate completion rates for each week going back from today"""
    if not completion_dates:
        return []
    
    today = date.today()
    weekly_rates = []
    
    for week_offset in range(weeks_back):
        week_start = today - timedelta(days=today.weekday() + (week_offset * 7))
        week_end = week_start + timedelta(days=6)
        
        # Count completions in this week
        week_completions = [d for d in completion_dates if week_start <= d <= week_end]
        
        if habit_period.lower() == 'daily':
            expected = 7
            completion_rate = (len(week_completions) / 7) * 100
        else:  # weekly
            expected = 1
            completion_rate = 100 if len(week_completions) >= 1 else 0
        
        weekly_rates.append(completion_rate)
    
    return list(reversed(weekly_rates))  # Most recent week last


def _calculate_trend_score(weekly_rates: List[float]) -> float:
    """Calculate if completion rates are trending up or down"""
    if len(weekly_rates) < 2:
        return 0.0
    
    # Simple linear trend calculation
    x_values = list(range(len(weekly_rates)))
    if len(set(weekly_rates)) == 1:  # All rates are the same
        return 0.0
    
    # Calculate correlation coefficient as trend indicator
    try:
        correlation = statistics.correlation(x_values, weekly_rates)
        return correlation  # Positive = improving trend, negative = declining
    except statistics.StatisticsError:
        return 0.0


def _calculate_consistency_score(weekly_rates: List[float]) -> float:
    """Calculate consistency score (lower variance = higher score)"""
    if len(weekly_rates) < 2:
        return 0.0
    
    try:
        variance = statistics.variance(weekly_rates)
        # Convert variance to consistency score (0-1, where 1 is most consistent)
        max_possible_variance = 50 * 50  # Assuming max rate difference of 50%
        consistency = max(0.0, 1.0 - (variance / max_possible_variance))
        return consistency
    except statistics.StatisticsError:
        return 0.0


def _calculate_recent_performance_weight(weekly_rates: List[float]) -> float:
    """Weight recent performance more heavily"""
    if len(weekly_rates) < 2:
        return 0.0
    
    # Take last 2 weeks and weight them more
    recent_weeks = weekly_rates[-2:]
    recent_average = sum(recent_weeks) / len(recent_weeks)
    
    # Normalize to 0-1 scale
    return recent_average / 100


def _determine_confidence_level(data_points: int, weeks_analyzed: int) -> str:
    """Determine confidence level based on amount of data"""
    if data_points >= 21 and weeks_analyzed >= 4:
        return 'high'
    elif data_points >= 14 and weeks_analyzed >= 3:
        return 'medium'
    else:
        return 'low'


def _calculate_completion_rate_for_period(completion_dates: List[date], habit_period: str, days: int) -> float:
    """Calculate completion rate for a specific period"""
    if not completion_dates or days == 0:
        return 0.0
    
    if habit_period.lower() == 'daily':
        expected = days
        actual = len(completion_dates)
        return (actual / expected) * 100
    else:  # weekly
        expected_weeks = max(1, days // 7)
        actual_weeks = len(set(d.isocalendar()[1] for d in completion_dates))
        return (actual_weeks / expected_weeks) * 100


def _calculate_dropout_risk_score(completion_dates: List[date]) -> float:
    """Calculate risk of dropping the habit based on completion patterns"""
    if len(completion_dates) < 7:
        return 0.5  # Medium risk with insufficient data
    
    # Look for gaps in completion
    sorted_dates = sorted(completion_dates)
    gaps = []
    
    for i in range(1, len(sorted_dates)):
        gap = (sorted_dates[i] - sorted_dates[i-1]).days
        if gap > 1:  # More than 1 day gap
            gaps.append(gap)
    
    if not gaps:
        return 0.1  # Low risk if no gaps
    
    # Calculate average gap and convert to risk score
    average_gap = sum(gaps) / len(gaps)
    risk_score = min(0.9, average_gap / 10)  # Scale to 0-0.9
    
    return risk_score


def _calculate_performance_variability(completion_dates: List[date]) -> float:
    """Calculate how variable the performance is"""
    if len(completion_dates) < 7:
        return 0.5
    
    # Group by weeks and calculate weekly completion counts
    weekly_counts = {}
    for date_obj in completion_dates:
        week_key = date_obj.isocalendar()[:2]  # (year, week)
        weekly_counts[week_key] = weekly_counts.get(week_key, 0) + 1
    
    if len(weekly_counts) < 2:
        return 0.0
    
    try:
        counts = list(weekly_counts.values())
        variance = statistics.variance(counts)
        # Normalize variance to 0-1 scale
        return min(1.0, variance / 10)
    except statistics.StatisticsError:
        return 0.5


def _generate_difficulty_recommendations(difficulty: str, dropout_risk: float) -> List[str]:
    """Generate recommendations based on predicted difficulty"""
    recommendations = []
    
    if difficulty == 'difficult':
        recommendations.append("Consider breaking this habit into smaller, easier steps")
        recommendations.append("Try habit stacking - attach this to an existing habit")
        if dropout_risk > 0.6:
            recommendations.append("High dropout risk detected - consider reducing frequency initially")
    
    elif difficulty == 'challenging':
        recommendations.append("Focus on consistency over perfection")
        recommendations.append("Set up environmental cues to make the habit easier")
    
    elif difficulty == 'moderate':
        recommendations.append("You're on a good track - maintain your current approach")
        if dropout_risk > 0.4:
            recommendations.append("Watch for consistency gaps - they're your main risk factor")
    
    else:  # easy
        recommendations.append("Great job! Consider adding complementary habits")
        recommendations.append("You might be ready to increase the challenge level")
    
    return recommendations


def _find_all_historical_streaks(completion_dates: List[date], habit_period: str) -> List[int]:
    """Find all historical streaks in the completion data"""
    if not completion_dates:
        return []
    
    sorted_dates = sorted(completion_dates)
    streaks = []
    current_streak = 1
    
    for i in range(1, len(sorted_dates)):
        expected_gap = 1 if habit_period.lower() == 'daily' else 7
        actual_gap = (sorted_dates[i] - sorted_dates[i-1]).days
        
        if actual_gap <= expected_gap + 1:  # Allow 1 day tolerance
            current_streak += 1
        else:
            if current_streak > 1:
                streaks.append(current_streak)
            current_streak = 1
    
    # Don't forget the last streak
    if current_streak > 1:
        streaks.append(current_streak)
    
    return streaks


def _calculate_historical_continuation_rate(historical_streaks: List[int], current_streak: int) -> float:
    """Calculate how often streaks of this length have continued historically"""
    if not historical_streaks or current_streak == 0:
        return 0.5  # Default probability
    
    # Find streaks that reached this length
    relevant_streaks = [s for s in historical_streaks if s >= current_streak]
    
    if not relevant_streaks:
        return 0.3  # Lower probability if never reached this length before
    
    # Find streaks that exceeded this length
    exceeded_streaks = [s for s in relevant_streaks if s > current_streak]
    
    if not relevant_streaks:
        return 0.5
    
    continuation_rate = len(exceeded_streaks) / len(relevant_streaks)
    return continuation_rate


def _calculate_recent_consistency(completion_dates: List[date], habit_period: str) -> float:
    """Calculate consistency in recent completions"""
    if not completion_dates:
        return 0.0
    
    # Look at last 2 weeks of data
    two_weeks_ago = date.today() - timedelta(days=14)
    recent_dates = [d for d in completion_dates if d >= two_weeks_ago]
    
    if not recent_dates:
        return 0.0
    
    if habit_period.lower() == 'daily':
        expected = 14
        actual = len(recent_dates)
        return min(1.0, actual / expected)
    else:  # weekly
        expected = 2
        weeks_with_completion = len(set(d.isocalendar()[1] for d in recent_dates))
        return min(1.0, weeks_with_completion / expected)


def _predict_milestone_achievements(current_streak: int, continuation_probability: float) -> Dict[str, float]:
    """Predict probability of reaching habit formation milestones"""
    milestones = {
        '7_days': 7,
        '21_days': 21,
        '66_days': 66,
        '100_days': 100
    }
    
    predictions = {}
    
    for milestone_name, milestone_days in milestones.items():
        if current_streak >= milestone_days:
            predictions[milestone_name] = 1.0  # Already achieved
        else:
            days_needed = milestone_days - current_streak
            # Probability decreases with distance and depends on continuation probability
            probability = continuation_probability ** (days_needed / 7)  # Weekly decay
            predictions[milestone_name] = probability
    
    return predictions

