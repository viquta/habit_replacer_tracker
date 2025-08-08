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
    # i like enums here because they constrain the input to only the allowed values (daily/weekly)
    # this helps me avoid typos like 'dai ly' and gives me autocomplete
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class User:
    """User model representing a user in the system"""
    # dataclass auto-generates __init__, __repr__, and equality methods for me
    # i keep Optional[int] for IDs because they are None until the DB assigns them
    user_id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    email: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        # __post_init__ runs right after dataclass creates the object
        # i set defaults that depend on runtime (timestamps) here
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Habit: #does it matter if the variables are a bit different than in database?
    """Habit model representing a habit in the system"""
    # same pattern: IDs are None before persistence
    habit_id: Optional[int] = None
    user_id: Optional[int] = None
    habit_name: str = ""
    description: str = ""
    # accept either Enum or raw string; i normalize to Enum in __post_init__
    period: HabitPeriod | str = HabitPeriod.DAILY 
    created_date: Optional[date] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        # i normalize all time-related defaults here so every Habit has sensible values
        if self.created_date is None:
            self.created_date = date.today()
        if self.created_at is None:
            self.created_at = datetime.now()
        # small convenience: allow constructing with strings ("daily"/"weekly")
        if isinstance(self.period, str):
            self.period = HabitPeriod(self.period)

    def __str__(self) -> str:
        # nice human-readable representation used in lists and tables
        period_enum = self.period if isinstance(self.period, HabitPeriod) else HabitPeriod(self.period)
        return f"{self.habit_name} ({period_enum.value})"


@dataclass
class HabitCompletion:
    """HabitCompletion model representing a completed habit instance"""
    # this is an event log entry: which habit, on what date, with optional notes
    completion_id: Optional[int] = None
    habit_id: Optional[int] = None
    completion_date: Optional[date] = None
    notes: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        # default to "today" if no completion date provided
        if self.completion_date is None:
            self.completion_date = date.today()
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class UserSetting:
    """UserSetting model for user preferences"""
    # simple key/value settings per user; can be extended later
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
    # i prefer explicit custom exceptions so higher layers can catch specific cases
    pass


class UserNotFoundException(Exception):
    """Exception raised when a user is not found"""
    pass


class DatabaseException(Exception):
    """Exception raised for database-related errors"""
    # this wraps low-level DB/driver errors so the CLI doesn't need to know details
    pass
