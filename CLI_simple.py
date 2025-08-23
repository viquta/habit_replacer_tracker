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
    Made a class to encapsulate all functionality and to follow OOP principles
    """
    #every class has an __init__ method, which is a constructor that initializes the class
    def __init__(self):
        self.console = Console()
        self.running = True

        #i made BACKEND_AVAILABLE variable in the try-except block above, 
        #hence, if the backend is not available, we cannot initialize services
        if BACKEND_AVAILABLE:
            try:
                self.user_service = UserService()
                self.habit_service = HabitService()
                self.completion_service = HabitCompletionService()
                self.analytics_service = HabitAnalyticsService()
                
                # Ensure demo user exists --> I think I made this in the db setup script
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
            box=box.ROUNDED # i can actually have a lot of creative styles here: https://rich.readthedocs.io/en/stable/appendix/box.html 
        )
        self.console.print(header)

    def show_main_menu(self):
        """Display main menu ... this is pretty redundant, but it's good practice to use docstrings"""
        self.console.print("\n" + "="*50)
        self.console.print("📋 MAIN MENU")
        self.console.print("="*50)
        self.console.print("1. 🆕 Create New Habit")
        self.console.print("2. ✏️  Edit Habit")
        self.console.print("3. 🗑️  Delete Habit")
        self.console.print("4. ✅ Mark Habit Complete")
        self.console.print("5. 📊 View Analytics")
        self.console.print("6. 📋 List All Habits")
        self.console.print("7. 📅 View Completion History")
        self.console.print("8. ❌ Exit")
        self.console.print("="*50)
        self.console.print("💡 Tip: Press Enter to list your habits (default option)")
        self.console.print("💡 Press Ctrl+C anytime to exit")

    def create_habit(self):
        """As I named it,this creates a new habit"""
        self.console.print("\n🆕 CREATE NEW HABIT")
        self.console.print("-" * 30)
        
        try:
            habit_name = Prompt.ask("📝 Habit name")
            if not habit_name.strip(): #checks if the habit name is empty
                self.console.print("❌ Habit name cannot be empty")
                return
                
            #i reflected a lot on this, and I think it's a good idea to remind the user about the habit's trigger, routine, and reward
            self.console.print("💭 Consider including your trigger, routine, and reward in the description")
            self.console.print("💡 Example: 'Trigger: After morning coffee, Routine: 10 push-ups, Reward: Feel energized'")
            description = Prompt.ask("📄 Description (optional)", default="")
            # pretty good documentation on the prompt.ask method: https://rich.readthedocs.io/en/stable/prompt.html
            
            self.console.print("💡 Daily habits: track every day (e.g., exercise, reading)")
            self.console.print("💡 Weekly habits: track once per week (e.g., grocery shopping, planning)")
            
            period_choice = Prompt.ask(
                "⏰ Period", 
                choices=["daily", "weekly"], 
                default="daily"
            )
            
            # Create the habit by going through the habit service (See the backend/services.py file)
            #stateful operation
            habit = self.habit_service.create_habit(habit_name, description, period_choice)
            #
            #   Before: Database has N habits
            #       ↓
            #   habit = self.habit_service.create_habit(...)  ← STATEFUL OPERATION
            #       ↓
            #   After: Database has N+1 habits (permanent change)
            #
            self.console.print(f"✅ Created habit: {habit.habit_name} ({habit.period.value})")
            
        except Exception as e:
            self.console.print(f"❌ Error creating habit: {e}")

    def list_habits(self):
        """List all active habits"""
        try:
            habits = self.habit_service.get_all_habits() #calls the get_all_habits method from the HabitService
            #now we have the list of habits called habits
            if not habits:
                self.console.print("📭 No habits found. Create one first!")
                return None
            
            table = Table(title="Your Habits", box=box.ROUNDED)
            table.add_column("#", style="cyan", width=3)
            table.add_column("Habit Name", style="green", min_width=20)
            table.add_column("Period", style="yellow", width=10)
            table.add_column("Created", style="magenta", width=12)
            table.add_column("Description", style="blue", min_width=20)
            
            for i, habit in enumerate(habits, 1): # i always forget the syntax: enumerate(iterable, start)
                # Format creation date
                created_display = habit.created_date.strftime("%Y-%m-%d") if habit.created_date else "Unknown"
                
                table.add_row( 
                    str(i), #here is the i in the for loop and this is converted to a string
                    habit.habit_name,
                    habit.period.value, #daily or weekly
                    created_display,
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
                self.console.print("💭 Consider updating your trigger, routine, and reward in the description")
                self.console.print("💡 Example: 'Trigger: After morning coffee, Routine: 10 push-ups, Reward: Feel energized'")
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
        """Mark a habit as complete for any date"""
        habits = self.list_habits()
        if not habits:
            return
            
        try:
            choice = IntPrompt.ask("Enter habit number to mark complete", default=1)
            
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                
                # Ask for the completion date
                self.console.print("💡 Examples: 'today', '2025-08-01', '2025-07-30'")
                date_input = Prompt.ask(
                    "📅 Date to mark complete (YYYY-MM-DD or 'today')", 
                    default="today"
                )
                
                # Parse the date
                if date_input.lower() == "today":
                    completion_date = date.today()
                else:
                    try:
                        completion_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                        
                        # Validate date range - no more than 1 year in the past, no future dates
                        today = date.today()
                        max_past = today.replace(year=today.year - 1)
                        
                        if completion_date < max_past:
                            self.console.print(f"❌ Date too far in the past. Cannot mark habits complete before {max_past}")
                            return
                        elif completion_date > today:
                            self.console.print(f"❌ Cannot mark habits complete for future dates. Please use today or an earlier date.")
                            return
                            
                    except ValueError:
                        self.console.print("❌ Invalid date format. Please use YYYY-MM-DD")
                        return
                
                # Check if already completed for this date
                completion = self.completion_service.completion_dao.get_completion_by_habit_and_date(
                    habit.habit_id, completion_date
                )
                if completion:
                    self.console.print(f"✅ {habit.habit_name} is already completed on {completion_date}!")
                    return
                
                self.console.print("💭 Reflect: What triggered this habit? How do you feel after completing it?")
                notes = Prompt.ask("Add notes (optional)", default="")
                
                # Complete the habit for the specified date
                completion = self.completion_service.complete_habit(
                    habit.habit_id, completion_date=completion_date, notes=notes
                )
                self.console.print(f"✅ Marked '{habit.habit_name}' as complete for {completion_date}!")
                
            else:
                self.console.print("❌ Invalid habit number")
                
        except Exception as e:
            self.console.print(f"❌ Error marking habit complete: {e}")

    def view_analytics(self):
        """View analytics using the 4 essential functions with rich tables"""
        self.console.print("\n📊 ANALYTICS DASHBOARD")
        self.console.print("-" * 50)
        
        try:
            # 1. Currently tracked habits overview
            tracked_habits = self.analytics_service.get_currently_tracked_habits()
            
            # Overview panel
            overview_panel = Panel(
                f"📈 Total Active Habits: {len(tracked_habits)}",
                title="Overview",
                style="bold green",
                box=box.ROUNDED
            )
            self.console.print(overview_panel)
            
            # 2. Habits by periodicity in a table
            daily_habits = self.analytics_service.get_habits_with_same_periodicity(HabitPeriod.DAILY)
            weekly_habits = self.analytics_service.get_habits_with_same_periodicity(HabitPeriod.WEEKLY)
            
            periodicity_table = Table(title="📅 Habits by Period", box=box.ROUNDED)
            periodicity_table.add_column("Period", style="cyan", width=10)
            periodicity_table.add_column("Count", style="yellow", width=8)
            periodicity_table.add_column("Habits", style="green", min_width=30)
            
            daily_names = ", ".join([h.habit_name for h in daily_habits]) if daily_habits else "None"
            weekly_names = ", ".join([h.habit_name for h in weekly_habits]) if weekly_habits else "None"
            
            periodicity_table.add_row("Daily", str(len(daily_habits)), daily_names)
            periodicity_table.add_row("Weekly", str(len(weekly_habits)), weekly_names)
            
            self.console.print(periodicity_table)
            
            # 3. Longest streak across all habits - separate for daily and weekly
            daily_habits = self.analytics_service.get_habits_with_same_periodicity(HabitPeriod.DAILY)
            weekly_habits = self.analytics_service.get_habits_with_same_periodicity(HabitPeriod.WEEKLY)
            
            # Best daily streak
            if daily_habits:
                best_daily_streak = None
                best_daily_habit = None
                for habit in daily_habits:
                    streak = self.analytics_service.get_longest_run_streak_for_habit(habit.habit_id)
                    if best_daily_streak is None or streak > best_daily_streak:
                        best_daily_streak = streak
                        best_daily_habit = habit
                
                if best_daily_streak and best_daily_streak > 0:
                    daily_streak_panel = Panel(
                        f"🏆 {best_daily_habit.habit_name}\n🔥 {best_daily_streak} days",
                        title="Best Daily Streak",
                        style="bold green",
                        box=box.ROUNDED
                    )
                else:
                    daily_streak_panel = Panel(
                        "No daily streaks yet - start completing daily habits!",
                        title="Best Daily Streak",
                        style="dim",
                        box=box.ROUNDED
                    )
            else:
                daily_streak_panel = Panel(
                    "No daily habits found",
                    title="Best Daily Streak",
                    style="dim",
                    box=box.ROUNDED
                )
            
            # Best weekly streak
            if weekly_habits:
                best_weekly_streak = None
                best_weekly_habit = None
                for habit in weekly_habits:
                    streak = self.analytics_service.get_longest_run_streak_for_habit(habit.habit_id)
                    if best_weekly_streak is None or streak > best_weekly_streak:
                        best_weekly_streak = streak
                        best_weekly_habit = habit
                
                if best_weekly_streak and best_weekly_streak > 0:
                    # For weekly habits, the streak should be displayed as weeks, not days
                    # Assuming the streak is returned in the appropriate unit (weeks for weekly habits)
                    weekly_streak_panel = Panel(
                        f"🏆 {best_weekly_habit.habit_name}\n🔥 {best_weekly_streak} weeks",
                        title="Best Weekly Streak",
                        style="bold blue",
                        box=box.ROUNDED
                    )
                else:
                    weekly_streak_panel = Panel(
                        "No weekly streaks yet - start completing weekly habits!",
                        title="Best Weekly Streak",
                        style="dim",
                        box=box.ROUNDED
                    )
            else:
                weekly_streak_panel = Panel(
                    "No weekly habits found",
                    title="Best Weekly Streak",
                    style="dim",
                    box=box.ROUNDED
                )
            
            # Display both panels side by side using columns
            from rich.columns import Columns
            self.console.print(Columns([daily_streak_panel, weekly_streak_panel]))
            
            # 4. Individual habit streaks in a table
            if tracked_habits:
                streaks_table = Table(title="🔥 Individual Habit Streaks", box=box.ROUNDED)
                streaks_table.add_column("Habit Name", style="green", min_width=25)
                streaks_table.add_column("Period", style="cyan", width=10)
                streaks_table.add_column("Current Streak", style="yellow", width=15)
                streaks_table.add_column("Status", style="magenta", min_width=25)
                
                for habit in tracked_habits:
                    streak = self.analytics_service.get_current_streak_for_habit(habit.habit_id)
                    
                    # Add visual indicators for streak status
                    if streak == 0:
                        status = "🟡 Getting started"
                    elif streak >= 30:
                        status = "🔥 On fire!"
                    elif streak >= 7:
                        status = "💪 Building momentum"
                    else:
                        status = "📈 Growing"
                    
                    streak_display = f"{streak} {'days' if habit.period.value == 'daily' else 'weeks'}"
                    
                    streaks_table.add_row(
                        habit.habit_name,
                        habit.period.value.title(),
                        streak_display,
                        status
                    )
                
                self.console.print(streaks_table)
            else:
                no_habits_panel = Panel(
                    "Create your first habit to start tracking streaks!",
                    title="No Habits Found",
                    style="dim",
                    box=box.ROUNDED
                )
                self.console.print(no_habits_panel)
                
        except Exception as e:
            self.console.print(f"❌ Error getting analytics: {e}")

    def view_completion_history(self):
        """View completion history for a specific habit"""
        habits = self.list_habits()
        if not habits:
            return
            
        try:
            choice = IntPrompt.ask("Enter habit number to view history", default=1)
            
            if 1 <= choice <= len(habits):
                habit = habits[choice - 1]
                
                self.console.print(f"\n📅 COMPLETION HISTORY: {habit.habit_name}")
                self.console.print(f"Created: {habit.created_date.strftime('%Y-%m-%d') if habit.created_date else 'Unknown'}")
                self.console.print("-" * 50)
                
                # Get completions for this habit
                completions = self.completion_service.get_habit_completions(habit.habit_id, limit=20)
                
                if not completions:
                    self.console.print("📭 No completions found for this habit yet.")
                    return
                
                # Create completion history table
                table = Table(title=f"Recent Completions ({len(completions)} shown)", box=box.ROUNDED)
                table.add_column("Date", style="green", width=12)
                table.add_column("Time", style="cyan", width=10)
                table.add_column("Notes", style="blue", min_width=30)
                
                for completion in completions:
                    completion_time = completion.created_at.strftime("%H:%M:%S") if completion.created_at else "Unknown"
                    completion_date = completion.completion_date.strftime("%Y-%m-%d") if completion.completion_date else "Unknown"
                    notes = completion.notes or "No notes"
                    
                    table.add_row(completion_date, completion_time, notes)
                
                self.console.print(table)
                
                # Show current streak
                current_streak = self.analytics_service.get_current_streak_for_habit(habit.habit_id)
                self.console.print(f"\n🔥 Current streak: {current_streak} {'days' if habit.period.value == 'daily' else 'weeks'}")
                
            else:
                self.console.print("❌ Invalid habit number")
                
        except Exception as e:
            self.console.print(f"❌ Error viewing completion history: {e}")

    def run(self):
        """Main application loop"""
        self.show_header()
        
        while self.running:
            try:
                self.show_main_menu()
                
                choice = Prompt.ask(
                    "\n🎯 Choose an option",
                    choices=["1", "2", "3", "4", "5", "6", "7", "8"],
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
                    self.view_completion_history()
                elif choice == "8":
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
