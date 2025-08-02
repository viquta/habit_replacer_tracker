#!/usr/bin/env python3

"""
Simplified Habit Tracker CLI Application
Clean version with only the essential features:
1. Create habits
2. Edit and delete habits  
3. Track habit completions
4. View analytics (4 essential functions)
"""

import sys
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import box

# Import backend services
try:
    from backend.services import (
        HabitService, HabitCompletionService, HabitAnalyticsService, 
        UserService
    )
    from backend.models import Habit, HabitPeriod, HabitNotFoundException, DatabaseException
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Backend not available: {e}")
    print("❌ Database backend is required for this application to function")
    BACKEND_AVAILABLE = False


class SimpleHabitTrackerCLI:
    """
    Simplified CLI application for the Habit Tracker
    Only includes essential functionality as specified in requirements
    """
    
    def __init__(self):
        self.console = Console()
        self.running = True
        
        if BACKEND_AVAILABLE:
            try:
                self.user_service = UserService()
                self.habit_service = HabitService()
                self.completion_service = HabitCompletionService()
                self.analytics_service = HabitAnalyticsService()
                
                # Ensure demo user exists
                self.current_user = self.user_service.get_current_user()
                
            except Exception as e:
                self.console.print(f"❌ Failed to initialize services: {e}")
                sys.exit(1)
        else:
            sys.exit(1)

    def show_header(self):
        """Display application header"""
        header = Panel(
            "🎯 Simple Habit Tracker\nTrack your daily and weekly habits",
            style="bold blue",
            box=box.ROUNDED
        )
        self.console.print(header)

    def show_main_menu(self):
        """Display main menu with essential options only"""
        self.console.print("\n" + "="*50)
        self.console.print("📋 MAIN MENU")
        self.console.print("="*50)
        self.console.print("1. 🆕 Create New Habit")
        self.console.print("2. ✏️  Edit Habit")
        self.console.print("3. 🗑️  Delete Habit")
        self.console.print("4. ✅ Mark Habit Complete")
        self.console.print("5. 📊 View Analytics")
        self.console.print("6. 📋 List All Habits")
        self.console.print("7. ❌ Exit")
        self.console.print("="*50)

    def create_habit(self):
        """Create a new habit"""
        self.console.print("\n🆕 CREATE NEW HABIT")
        self.console.print("-" * 30)
        
        try:
            habit_name = Prompt.ask("📝 Habit name")
            if not habit_name.strip():
                self.console.print("❌ Habit name cannot be empty")
                return
                
            description = Prompt.ask("📄 Description (optional)", default="")
            
            period_choice = Prompt.ask(
                "⏰ Period", 
                choices=["daily", "weekly"], 
                default="daily"
            )
            
            # Create the habit
            habit = self.habit_service.create_habit(habit_name, description, period_choice)
            
            self.console.print(f"✅ Created habit: {habit.habit_name} ({habit.period.value})")
            
        except Exception as e:
            self.console.print(f"❌ Error creating habit: {e}")

    def list_habits(self):
        """List all active habits"""
        try:
            habits = self.habit_service.get_all_habits()
            
            if not habits:
                self.console.print("📭 No habits found. Create one first!")
                return None
            
            table = Table(title="Your Habits", box=box.ROUNDED)
            table.add_column("#", style="cyan", width=3)
            table.add_column("Habit Name", style="green", min_width=20)
            table.add_column("Period", style="yellow", width=10)
            table.add_column("Description", style="blue", min_width=20)
            
            for i, habit in enumerate(habits, 1):
                table.add_row(
                    str(i),
                    habit.habit_name,
                    habit.period.value,
                    habit.description or "No description"
                )
            
            self.console.print(table)
            return habits
            
        except Exception as e:
            self.console.print(f"❌ Error listing habits: {e}")
            return None

    def edit_habit(self):
        """Edit an existing habit"""
        habits = self.list_habits()
        if not habits:
            return
            
        try:
            choice = IntPrompt.ask("Enter habit number to edit", default=1)
            
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                
                self.console.print(f"\n✏️ Editing: {habit.habit_name}")
                
                new_name = Prompt.ask("New name", default=habit.habit_name)
                new_desc = Prompt.ask("New description", default=habit.description or "")
                new_period = Prompt.ask("New period", choices=["daily", "weekly"], default=habit.period.value)
                
                updated_habit = self.habit_service.update_habit(
                    habit.habit_id, new_name, new_desc, new_period
                )
                
                self.console.print(f"✅ Updated habit: {updated_habit.habit_name}")
            else:
                self.console.print("❌ Invalid habit number")
                
        except Exception as e:
            self.console.print(f"❌ Error editing habit: {e}")

    def delete_habit(self):
        """Delete a habit"""
        habits = self.list_habits()
        if not habits:
            return
            
        try:
            choice = IntPrompt.ask("Enter habit number to delete", default=1)
            
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                
                confirm = Confirm.ask(f"Are you sure you want to delete '{habit.habit_name}'?")
                if confirm:
                    self.habit_service.delete_habit(habit.habit_id)
                    self.console.print(f"✅ Deleted habit: {habit.habit_name}")
                else:
                    self.console.print("❌ Deletion cancelled")
            else:
                self.console.print("❌ Invalid habit number")
                
        except Exception as e:
            self.console.print(f"❌ Error deleting habit: {e}")

    def mark_habit_complete(self):
        """Mark a habit as complete for today"""
        habits = self.list_habits()
        if not habits:
            return
            
        try:
            choice = IntPrompt.ask("Enter habit number to mark complete", default=1)
            
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                
                # Check if already completed today
                if self.completion_service.is_habit_completed_today(habit.habit_id):
                    self.console.print(f"✅ {habit.habit_name} is already completed today!")
                    return
                
                notes = Prompt.ask("Add notes (optional)", default="")
                
                completion = self.completion_service.complete_habit(habit.habit_id, notes=notes)
                self.console.print(f"✅ Marked '{habit.habit_name}' as complete!")
                
            else:
                self.console.print("❌ Invalid habit number")
                
        except Exception as e:
            self.console.print(f"❌ Error marking habit complete: {e}")

    def view_analytics(self):
        """View analytics using the 4 essential functions"""
        self.console.print("\n📊 ANALYTICS")
        self.console.print("-" * 30)
        
        try:
            # 1. Currently tracked habits
            tracked_habits = self.analytics_service.get_currently_tracked_habits()
            self.console.print(f"📈 Currently tracked habits: {len(tracked_habits)}")
            for habit in tracked_habits:
                self.console.print(f"  • {habit.habit_name} ({habit.period.value})")
            
            # 2. Habits by periodicity
            daily_habits = self.analytics_service.get_habits_with_same_periodicity(HabitPeriod.DAILY)
            weekly_habits = self.analytics_service.get_habits_with_same_periodicity(HabitPeriod.WEEKLY)
            
            self.console.print(f"\n📅 Daily habits: {len(daily_habits)}")
            for habit in daily_habits:
                self.console.print(f"  • {habit.habit_name}")
                
            self.console.print(f"\n📅 Weekly habits: {len(weekly_habits)}")
            for habit in weekly_habits:
                self.console.print(f"  • {habit.habit_name}")
            
            # 3. Longest streak across all habits
            longest_all = self.analytics_service.get_longest_run_streak_all_habits()
            if longest_all['habit']:
                self.console.print(f"\n🏆 Best streak: {longest_all['habit_name']} - {longest_all['streak_length']} days")
            else:
                self.console.print("\n🏆 No streaks yet - start completing habits!")
            
            # 4. Individual habit streaks
            self.console.print(f"\n🔥 Individual habit streaks:")
            for habit in tracked_habits:
                streak = self.analytics_service.get_longest_run_streak_for_habit(habit.habit_id)
                self.console.print(f"  • {habit.habit_name}: {streak} days")
                
        except Exception as e:
            self.console.print(f"❌ Error getting analytics: {e}")

    def run(self):
        """Main application loop"""
        self.show_header()
        
        while self.running:
            try:
                self.show_main_menu()
                
                choice = Prompt.ask(
                    "\n🎯 Choose an option",
                    choices=["1", "2", "3", "4", "5", "6", "7"],
                    default="6"
                )
                
                if choice == "1":
                    self.create_habit()
                elif choice == "2":
                    self.edit_habit()
                elif choice == "3":
                    self.delete_habit()
                elif choice == "4":
                    self.mark_habit_complete()
                elif choice == "5":
                    self.view_analytics()
                elif choice == "6":
                    self.list_habits()
                elif choice == "7":
                    self.console.print("👋 Goodbye!")
                    self.running = False
                
                if self.running:
                    Prompt.ask("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                self.console.print("\n👋 Goodbye!")
                self.running = False
            except Exception as e:
                self.console.print(f"❌ Unexpected error: {e}")


def main():
    """Entry point for the application"""
    if not BACKEND_AVAILABLE:
        print("❌ Backend services are not available. Please check your setup.")
        sys.exit(1)
    
    app = SimpleHabitTrackerCLI()
    app.run()


if __name__ == "__main__":
    main()
