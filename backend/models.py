"""
Models module for Habit Tracker Application
Following Object-Oriented programming paradigm as required
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any #why is list dict and any not used?
from dataclasses import dataclass
from enum import Enum


class HabitPeriod(Enum):
    """Enumeration for habit periods"""
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class User:
    """User model representing a user in the system"""
    user_id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    email: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Habit: #does it matter if the variables are a bit different than in database?
    """Habit model representing a habit in the system"""
    habit_id: Optional[int] = None
    user_id: Optional[int] = None
    habit_name: str = ""
    description: str = ""
    period: HabitPeriod = HabitPeriod.DAILY 
    created_date: Optional[date] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = date.today()
        if self.created_at is None:
            self.created_at = datetime.now()
        if isinstance(self.period, str):
            self.period = HabitPeriod(self.period)

    def __str__(self) -> str:
        return f"{self.habit_name} ({self.period.value})"


@dataclass
class HabitCompletion:
    """HabitCompletion model representing a completed habit instance"""
    completion_id: Optional[int] = None
    habit_id: Optional[int] = None
    completion_date: Optional[date] = None
    notes: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.completion_date is None:
            self.completion_date = date.today()
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class UserSetting:
    """UserSetting model for user preferences"""
    setting_id: Optional[int] = None
    user_id: Optional[int] = None
    setting_key: str = ""
    setting_value: str = ""
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class HabitAnalytics:
    """Data class for habit analytics results"""
    habit_id: int
    habit_name: str
    period: str
    current_streak: int = 0
    longest_streak: int = 0
    total_completions: int = 0
    completion_rate: float = 0.0
    average_weekly_completions: float = 0.0
    longest_streak_start: Optional[date] = None
    longest_streak_end: Optional[date] = None
    
    def get_difficulty_level(self) -> str:
        """
        Determine habit difficulty based on completion rate
        Following the app philosophy: assume user is performing unless logged otherwise
        """
        if self.completion_rate >= 80:
            return "Easy"
        elif self.completion_rate >= 60:
            return "Moderate"
        elif self.completion_rate >= 40:
            return "Challenging"
        else:
            return "Difficult"

    def get_consistency_score(self) -> str:
        """Get consistency score based on streaks and completion rate"""
        if self.completion_rate >= 90 and self.current_streak >= 7:
            return "Excellent"
        elif self.completion_rate >= 75 and self.current_streak >= 5:
            return "Very Good"
        elif self.completion_rate >= 60 and self.current_streak >= 3:
            return "Good"
        elif self.completion_rate >= 40:
            return "Needs Improvement"
        else:
            return "Just Started"


class HabitNotFoundException(Exception):
    """Exception raised when a habit is not found"""
    pass


class UserNotFoundException(Exception):
    """Exception raised when a user is not found"""
    pass


class DatabaseException(Exception):
    """Exception raised for database-related errors"""
    pass
