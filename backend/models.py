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


class HabitNotFoundException(Exception):
    """Exception raised when a habit is not found"""
    pass


class UserNotFoundException(Exception):
    """Exception raised when a user is not found"""
    pass


class DatabaseException(Exception):
    """Exception raised for database-related errors"""
    pass
