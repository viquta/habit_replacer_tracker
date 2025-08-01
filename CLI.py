#!/usr/bin/env python3

"""
Habit Tracker CLI Application
Users can create, manage, and inspect habits they define in a convenient way

Updated to integrate with the backend business logic and database
"""

import sys
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.tree import Tree
from rich import box
from rich.markdown import Markdown
import time

# Import backend services
try:
    from backend.services import (
        HabitService, HabitCompletionService, HabitAnalyticsService, 
        SystemService, UserService
    )
    from backend.models import Habit, HabitPeriod, HabitNotFoundException, DatabaseException
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Backend not available: {e}")
    print("❌ Database backend is required for this application to function")
    BACKEND_AVAILABLE = False


class HabitTrackerCLI:
    """
    Main CLI application class for the Habit Tracker
    Integrated with backend services and database
    """
    
    def __init__(self):
        self.console = Console()
        self.running = True
        
        # Initialize backend services if available
        if BACKEND_AVAILABLE:
            try:
                self.system_service = SystemService()
                self.habit_service = HabitService()
                self.completion_service = HabitCompletionService()
                self.analytics_service = HabitAnalyticsService()
                self.user_service = UserService()
                
                # Initialize system and check connectivity
                if not self.system_service.initialize_system():
                    self.console.print("⚠️ Failed to initialize system. Some features may not work.", style="bold yellow")
                    
                self.backend_ready = True
            except Exception as e:
                self.console.print(f"❌ Backend initialization failed: {e}", style="bold red")
                self.backend_ready = False
        else:
            self.backend_ready = False
            
        # Show error if backend is not available
        if not self.backend_ready:
            self.console.print("❌ Database backend is required for this application to function.", style="bold red")
            self.console.print("Please ensure your database is properly configured and accessible.", style="dim red")

    def show_header(self):
        """Display beautiful app header"""
        header_text = Text()
        header_text.append("🌟 ", style="bright_yellow")
        header_text.append("HABIT TRACKER", style="bold bright_blue")
        header_text.append(" 🌟", style="bright_yellow")
        
        header_panel = Panel(
            Align.center(header_text),
            style="bright_blue",
            box=box.DOUBLE_EDGE,
            padding=(1, 2)
        )
        
        self.console.print()
        self.console.print(header_panel)
        self.console.print()

    def show_main_menu(self):
        """Display the main menu with beautiful styling"""
        self.console.clear()
        self.show_header()
        
        # Create menu options
        menu_options = [
            ("1", "📝", "Manage Habits", "Create, edit, or delete your habits"),
            ("2", "✅", "Log Habit Completion", "Mark habits as completed for today"),
            ("3", "📊", "View Progress & Analytics", "See your streaks and statistics"),
            ("4", "🔍", "Search & Filter Habits", "Find specific habits or filter by type"),
            ("5", "⚙️", "Settings", "Configure app preferences"),
            ("6", "❓", "Help", "Get help and usage information"),
            ("7", "🚪", "Exit", "Close the application")
        ]
        
        # Create a beautiful menu table
        menu_table = Table(
            show_header=False,
            box=box.ROUNDED,
            border_style="bright_cyan",
            padding=(0, 2)
        )
        
        menu_table.add_column("", style="bold bright_white", width=3)
        menu_table.add_column("", width=3)
        menu_table.add_column("Option", style="bold", width=25)
        menu_table.add_column("Description", style="dim", width=40)
        
        for num, emoji, title, desc in menu_options:
            menu_table.add_row(num, emoji, title, desc)
        
        menu_panel = Panel(
            menu_table,
            title="[bold bright_cyan]Main Menu[/bold bright_cyan]",
            border_style="bright_cyan",
            padding=(1, 2)
        )
        
        self.console.print(menu_panel)
        
        # Show current status
        if self.backend_ready:
            try:
                current_habits = self.habit_service.get_all_habits()
                total_habits = len(current_habits)
                # Get streak info from analytics if available
                try:
                    analytics_data = self.analytics_service.get_all_habits_analytics()
                    total_streaks = sum(a.current_streak for a in analytics_data)
                except:
                    total_streaks = 0
            except:
                total_habits = 0
                total_streaks = 0
        else:
            total_habits = 0
            total_streaks = 0
        
        status_text = Text()
        status_text.append(f"📅 Today: {datetime.now().strftime('%B %d, %Y')} | ", style="dim")
        status_text.append(f"🎯 Active Habits: {total_habits} | ", style="dim")
        status_text.append(f"⚡ Total Streaks: {total_streaks}", style="dim")
        
        self.console.print(Align.center(status_text))
        self.console.print()

    def manage_habits_menu(self):
        """Submenu for habit management with backend integration"""
        if not self.backend_ready:
            self.console.print("❌ Backend services are not available. Cannot manage habits without database connection.", style="bold red")
            input("\nPress Enter to continue...")
            return
            
        while True:
            self.console.clear()
            self.show_header()
            
            # Get habits from backend
            try:
                habits = self.habit_service.get_all_habits()
            except Exception as e:
                self.console.print(f"❌ Error loading habits: {e}", style="bold red")
                habits = []

            # Create habits table
            habits_table = Table(
                show_header=True,
                header_style="bold bright_cyan",
                border_style="bright_cyan",
                box=box.ROUNDED
            )
            
            habits_table.add_column("ID", style="dim", width=5)
            habits_table.add_column("Habit Name", style="bold", width=30)
            habits_table.add_column("Description", width=35)
            habits_table.add_column("Period", justify="center", width=8)
            habits_table.add_column("Status", justify="center", width=8)
            habits_table.add_column("Created", justify="center", width=12)

            for i, habit in enumerate(habits, 1):
                habit_id = str(habit.habit_id) if habit.habit_id else str(i)
                name = habit.habit_name
                description = habit.description
                period = habit.period.value if hasattr(habit.period, 'value') else habit.period
                status = "✅ Active" if habit.is_active else "❌ Inactive"
                created = habit.created_date.strftime("%Y-%m-%d") if habit.created_date else "Unknown"
                
                habits_table.add_row(habit_id, name, description, period, status, created)

            if not habits:
                empty_panel = Panel(
                    Align.center("No habits found. Create your first habit!"),
                    style="yellow",
                    title="📝 Your Habits"
                )
                self.console.print(empty_panel)
            else:
                habits_panel = Panel(
                    habits_table,
                    title="[bold bright_cyan]📝 Your Habits[/bold bright_cyan]",
                    border_style="bright_cyan"
                )
                self.console.print(habits_panel)

            # Management options
            self.console.print("\n[bold bright_cyan]Management Options:[/bold bright_cyan]")
            self.console.print("1. ➕ Create new habit")
            self.console.print("2. ✏️  Edit habit")
            self.console.print("3. 🗑️  Delete habit")
            self.console.print("4. 🔙 Back to main menu")
            
            choice = Prompt.ask("\nWhat would you like to do?", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                self.create_habit()
            elif choice == "2":
                self.edit_habit(habits)
            elif choice == "3":
                self.delete_habit(habits)
            elif choice == "4":
                break

    def create_habit(self):
        """Create a new habit with backend integration"""
        if not self.backend_ready:
            self.console.print("❌ Backend services are not available. Cannot create habits without database connection.", style="bold red")
            input("\nPress Enter to continue...")
            return
            
        self.console.print()
        self.console.print(Panel(
            "[bold bright_green]Create New Habit[/bold bright_green]",
            border_style="bright_green"
        ))
        
        try:
            name = Prompt.ask("🏷️  Habit name")
            if not name.strip():
                self.console.print("[red]❌ Habit name cannot be empty![/red]")
                input("\nPress Enter to continue...")
                return
                
            description = Prompt.ask("📝 Description (optional)", default="")
            
            # Improved period selection with numbered options
            self.console.print("\n⏰ Period:")
            self.console.print("1. daily")
            self.console.print("2. weekly")
            
            period_choice = Prompt.ask("Select period", choices=["1", "2", "daily", "weekly"], default="1")
            
            # Convert choice to period string
            if period_choice == "1" or period_choice.lower() == "daily":
                period = "daily"
            elif period_choice == "2" or period_choice.lower() == "weekly":
                period = "weekly"
            else:
                period = "daily"  # Default fallback
            
            # Create habit using backend
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Creating habit..."),
                console=self.console
            ) as progress:
                progress.add_task("Creating", total=None)
                
                habit = self.habit_service.create_habit(name, description, period)
                
            self.console.print(f"[bright_green]✅ Habit '{habit.habit_name}' created successfully![/bright_green]")
            self.console.print(f"[dim]📅 Created on: {habit.created_date}[/dim]")
                
        except DatabaseException as e:
            self.console.print(f"[red]❌ Database error: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]❌ Error creating habit: {e}[/red]")
            
        input("\nPress Enter to continue...")

    def edit_habit(self, habits):
        """Edit an existing habit"""
        if not habits:
            self.console.print("[yellow]No habits to edit![/yellow]")
            input("\nPress Enter to continue...")
            return
            
        self.console.print("\n[bold bright_cyan]Select habit to edit:[/bold bright_cyan]")
        
        # Show habits with numbers
        for i, habit in enumerate(habits, 1):
            name = habit.habit_name if self.backend_ready else habit.name
            self.console.print(f"{i}. {name}")
        
        try:
            choice = IntPrompt.ask("Enter habit number", default=1)
            if 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                
                current_name = selected_habit.habit_name
                current_desc = selected_habit.description
                current_period = selected_habit.period.value
                
                new_name = Prompt.ask("New name", default=current_name)
                new_desc = Prompt.ask("New description", default=current_desc)
                new_period = Prompt.ask("New period", choices=["daily", "weekly"], default=current_period)
                
                try:
                    updated_habit = self.habit_service.update_habit(
                        selected_habit.habit_id, new_name, new_desc, new_period
                    )
                    self.console.print(f"[green]✅ Habit '{updated_habit.habit_name}' updated successfully![/green]")
                except Exception as e:
                    self.console.print(f"[red]❌ Error updating habit: {e}[/red]")
            else:
                self.console.print("[red]Invalid habit number![/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Edit cancelled[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
            
        input("\nPress Enter to continue...")

    def delete_habit(self, habits):
        """Delete a habit"""
        if not habits:
            self.console.print("[yellow]No habits to delete![/yellow]")
            input("\nPress Enter to continue...")
            return
            
        self.console.print("\n[bold red]⚠️  Select habit to delete:[/bold red]")
        
        # Show habits with numbers
        for i, habit in enumerate(habits, 1):
            name = habit.habit_name
            self.console.print(f"{i}. {name}")
        
        try:
            choice = IntPrompt.ask("Enter habit number", default=1)
            if 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                habit_name = selected_habit.habit_name
                
                if Confirm.ask(f"Are you sure you want to delete '{habit_name}'?"):
                    try:
                        success = self.habit_service.delete_habit(selected_habit.habit_id)
                        if success:
                            self.console.print(f"[green]✅ Habit '{habit_name}' deleted successfully![/green]")
                        else:
                            self.console.print("[red]❌ Failed to delete habit[/red]")
                    except Exception as e:
                        self.console.print(f"[red]❌ Error deleting habit: {e}[/red]")
                else:
                    self.console.print("[yellow]Delete cancelled[/yellow]")
            else:
                self.console.print("[red]Invalid habit number![/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Delete cancelled[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
            
        input("\nPress Enter to continue...")

    def log_completion_menu(self):
        """Menu for logging habit completions with backend integration"""
        if not self.backend_ready:
            self.console.print("❌ Backend services are not available. Cannot log completions without database connection.", style="bold red")
            input("\nPress Enter to continue...")
            return
            
        while True:
            self.console.clear()
            self.show_header()
            
            self.console.print(Panel(
                "[bold bright_yellow]✅ Log Habit Completion[/bold bright_yellow]",
                border_style="bright_yellow"
            ))
            
            # Get habits and their completion status for today
            try:
                habits = self.habit_service.get_all_habits()
                habits_due = self.habit_service.get_habits_due_today()
            except Exception as e:
                self.console.print(f"❌ Error loading habits: {e}", style="bold red")
                input("\nPress Enter to continue...")
                return
            
            if not habits:
                self.console.print(Panel(
                    Align.center("No habits found. Create your first habit!"),
                    style="yellow"
                ))
                input("\nPress Enter to continue...")
                return
            
            # Show today's habits with completion status
            today_table = Table(
                title="[bold]📅 Today's Habits[/bold]",
                box=box.ROUNDED,
                border_style="bright_yellow"
            )
            
            today_table.add_column("#", width=3)
            today_table.add_column("Habit", width=35)
            today_table.add_column("Period", justify="center", width=10)
            today_table.add_column("Status", justify="center", width=15)
            today_table.add_column("Action", justify="center", width=12)
            
            for i, habit in enumerate(habits, 1):
                habit_name = habit.habit_name
                period = habit.period.value
                is_completed = self.completion_service.is_habit_completed_today(habit.habit_id)
                
                if is_completed:
                    status = "[bright_green]✅ Done[/bright_green]"
                    action = "[dim]Undo[/dim]"
                elif habit in habits_due:
                    status = "[yellow]⏳ Due[/yellow]"
                    action = "[green]Complete[/green]"
                else:
                    status = "[dim]➖ Not due[/dim]"
                    action = "[dim]N/A[/dim]"
                
                today_table.add_row(str(i), habit_name, period, status, action)
            
            self.console.print(today_table)
            
            # Menu options
            self.console.print("\n[bold bright_yellow]Options:[/bold bright_yellow]")
            self.console.print("• Enter habit number to complete/undo")
            self.console.print("• 'a' - Mark all due habits as complete")
            self.console.print("• 's' - Show completion calendar")
            self.console.print("• 'b' - Back to main menu")
            
            choice = Prompt.ask("\nWhat would you like to do?", default="b")
            
            if choice.lower() == 'b':
                break
            elif choice.lower() == 'a':
                self._complete_all_due_habits(habits_due)
            elif choice.lower() == 's':
                self._show_completion_calendar(habits)
            elif choice.isdigit():
                habit_num = int(choice)
                if 1 <= habit_num <= len(habits):
                    self._toggle_habit_completion(habits[habit_num - 1])
                else:
                    self.console.print("[red]Invalid habit number![/red]")
                    input("\nPress Enter to continue...")
            else:
                self.console.print("[red]Invalid choice![/red]")
                input("\nPress Enter to continue...")

    def _complete_all_due_habits(self, habits_due):
        """Complete all habits that are due today"""
        if not habits_due:
            self.console.print("[yellow]No habits are due today![/yellow]")
            input("\nPress Enter to continue...")
            return
        
        completed_count = 0
        for habit in habits_due:
            try:
                if not self.completion_service.is_habit_completed_today(habit.habit_id):
                    self.completion_service.complete_habit(habit.habit_id)
                    completed_count += 1
            except Exception as e:
                self.console.print(f"[red]❌ Error completing {habit.habit_name}: {e}[/red]")
        
        if completed_count > 0:
            self.console.print(f"[green]✅ Completed {completed_count} habits![/green]")
        else:
            self.console.print("[yellow]All due habits were already completed![/yellow]")
        
        input("\nPress Enter to continue...")

    def _toggle_habit_completion(self, habit):
        """Toggle completion status for a habit"""
        try:
            habit_name = habit.habit_name
            is_completed = self.completion_service.is_habit_completed_today(habit.habit_id)
            
            if is_completed:
                # Uncomplete the habit
                success = self.completion_service.uncomplete_habit(habit.habit_id)
                if success:
                    self.console.print(f"[yellow]↩️  Unmarked '{habit_name}' as completed[/yellow]")
                else:
                    self.console.print(f"[red]❌ Failed to unmark '{habit_name}'[/red]")
            else:
                # Complete the habit
                notes = Prompt.ask("Add notes (optional)", default="")
                completion = self.completion_service.complete_habit(habit.habit_id, notes=notes)
                self.console.print(f"[green]✅ Completed '{habit_name}'! 🎉[/green]")
                    
        except DatabaseException as e:
            if "already completed" in str(e).lower():
                self.console.print(f"[yellow]'{habit_name}' is already completed today![/yellow]")
            else:
                self.console.print(f"[red]❌ Database error: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def _show_completion_calendar(self, habits):
        """Show a completion calendar for habits"""
        if not habits:
            self.console.print("[yellow]No habits to show![/yellow]")
            input("\nPress Enter to continue...")
            return
        
        self.console.print("\n[bold bright_cyan]Select habit for calendar view:[/bold bright_cyan]")
        for i, habit in enumerate(habits, 1):
            name = habit.habit_name
            self.console.print(f"{i}. {name}")
        
        try:
            choice = IntPrompt.ask("Enter habit number", default=1)
            if 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                
                # Show real calendar
                today = date.today()
                calendar_data = self.completion_service.get_completion_calendar(
                    selected_habit.habit_id, today.year, today.month
                )
                
                self.console.print(f"\n[bold]{selected_habit.habit_name} - {today.strftime('%B %Y')}[/bold]")
                
                # Create calendar display
                calendar_table = Table(show_header=True, box=box.ROUNDED)
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                for day in days:
                    calendar_table.add_column(day, justify="center", width=5)
                
                # Add calendar rows (simplified version)
                week_days = []
                for day, completed in calendar_data.items():
                    status = "✅" if completed else "⬜"
                    week_days.append(f"{day}\n{status}")
                    
                    if len(week_days) == 7:
                        calendar_table.add_row(*week_days)
                        week_days = []
                
                # Add remaining days
                if week_days:
                    while len(week_days) < 7:
                        week_days.append("")
                    calendar_table.add_row(*week_days)
                
                self.console.print(calendar_table)
                
        except Exception as e:
            self.console.print(f"[red]❌ Error showing calendar: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def view_analytics_menu(self):
        """Display progress and analytics with backend integration"""
        self.console.clear()
        self.show_header()
        
        if not self.backend_ready:
            # Show fallback analytics menu for demo purposes
            self._show_fallback_analytics_menu()
            return
        
        # Get habits data
        try:
            habits = self.habit_service.get_all_habits()
            # Get analytics data from backend
            analytics_data = self.analytics_service.get_all_habits_analytics()
        except Exception as e:
            self.console.print(f"❌ Error loading analytics: {e}", style="bold red")
            habits = []
            analytics_data = []
        
        if not habits:
            self.console.print(Panel(
                Align.center("No habits found. Create your first habit to see analytics!"),
                style="yellow"
            ))
            input("\nPress Enter to continue...")
            return
        
        # Create analytics dashboard
        analytics_layout = Table.grid(padding=1)
        analytics_layout.add_column()
        analytics_layout.add_column()
        
        # Streaks panel
        streaks_table = Table(box=box.ROUNDED, border_style="bright_blue")
        streaks_table.add_column("Habit", width=25)
        streaks_table.add_column("Current Streak", justify="center", width=15)
        streaks_table.add_column("Completion Rate", justify="center", width=15)
        
        if analytics_data:
            # Use real analytics data
            for analytics in sorted(analytics_data, key=lambda x: x.current_streak, reverse=True):
                streak_color = "bright_green" if analytics.current_streak >= 7 else "bright_yellow" if analytics.current_streak >= 3 else "white"
                rate_color = "bright_green" if analytics.completion_rate >= 80 else "bright_yellow" if analytics.completion_rate >= 60 else "white"
                
                streaks_table.add_row(
                    analytics.habit_name,
                    f"[{streak_color}]{analytics.current_streak}[/{streak_color}]",
                    f"[{rate_color}]{analytics.completion_rate:.1f}%[/{rate_color}]"
                )
        else:
            # No analytics data available
            streaks_table.add_row("No data", "[dim]N/A[/dim]", "[dim]N/A[/dim]")
        
        streaks_panel = Panel(
            streaks_table,
            title="[bold bright_blue]🔥 Current Streaks[/bold bright_blue]",
            border_style="bright_blue"
        )
        
        # Stats panel
        total_habits = len(habits)
        daily_habits = len([h for h in habits if h.period == HabitPeriod.DAILY])
        weekly_habits = len([h for h in habits if h.period == HabitPeriod.WEEKLY])
        if analytics_data:
            avg_completion_rate = sum(a.completion_rate for a in analytics_data) / len(analytics_data)
            max_streak = max(a.current_streak for a in analytics_data) if analytics_data else 0
        else:
            avg_completion_rate = 0
            max_streak = 0
        
        stats_text = f"""
[bold]📊 Statistics[/bold]

Total Habits: [bright_cyan]{total_habits}[/bright_cyan]
Daily Habits: [bright_yellow]{daily_habits}[/bright_yellow]
Weekly Habits: [bright_magenta]{weekly_habits}[/bright_magenta]
Avg Completion Rate: [bright_green]{avg_completion_rate:.1f}%[/bright_green]
Highest Streak: [bright_red]{max_streak} days[/bright_red]
        """
        
        stats_panel = Panel(
            stats_text.strip(),
            border_style="bright_green"
        )
        
        analytics_layout.add_row(streaks_panel, stats_panel)
        self.console.print(analytics_layout)
        
        # Show additional options
        self.console.print("\n[bold bright_cyan]Analytics Options:[/bold bright_cyan]")
        self.console.print("1. 📈 View detailed habit trends")
        self.console.print("2. 🏆 Show difficulty rankings")
        self.console.print("3. 💡 Get personalized recommendations")
        self.console.print("4. 🎯 Advanced Analytics (NEW!)")
        self.console.print("5. 🔙 Back to main menu")
        
        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5"], default="5")
        
        if choice == "1":
            self._show_habit_trends()
        elif choice == "2":
            self._show_difficulty_rankings(analytics_data)
        elif choice == "3":
            self._show_recommendations(analytics_data)
        elif choice == "4":
            self._show_advanced_analytics()
        # Choice 5 (back) will naturally exit the method
    
    def _show_habit_trends(self):
        """Show habit trends over time"""
        try:
            habits = self.habit_service.get_all_habits()
            
            self.console.print("\n[bold bright_cyan]Select habit for trend analysis:[/bold bright_cyan]")
            for i, habit in enumerate(habits, 1):
                self.console.print(f"{i}. {habit.habit_name}")
            
            choice = IntPrompt.ask("Enter habit number", default=1)
            if 1 <= choice <= len(habits):
                selected_habit = habits[choice - 1]
                trends = self.analytics_service.get_habit_trends(selected_habit.habit_id)
                
                self.console.print(f"\n[bold]{selected_habit.habit_name} - Weekly Trends[/bold]")
                
                trends_table = Table(box=box.ROUNDED)
                trends_table.add_column("Week", justify="center")
                trends_table.add_column("Completions", justify="center")
                trends_table.add_column("Rate", justify="center")
                trends_table.add_column("Trend", justify="center")
                
                for i, trend in enumerate(trends):
                    week_num = f"Week {len(trends) - i}"
                    completions = str(trend['completions'])
                    rate = f"{trend['completion_rate']}%"
                    
                    if i == 0:  # Most recent week
                        trend_indicator = "📈" if trend['completion_rate'] > 70 else "📉" if trend['completion_rate'] < 50 else "➖"
                    else:
                        prev_rate = trends[i-1]['completion_rate']
                        trend_indicator = "⬆️" if trend['completion_rate'] > prev_rate else "⬇️" if trend['completion_rate'] < prev_rate else "➖"
                    
                    trends_table.add_row(week_num, completions, rate, trend_indicator)
                
                self.console.print(trends_table)
            
        except Exception as e:
            self.console.print(f"[red]❌ Error showing trends: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def _show_difficulty_rankings(self, analytics_data):
        """Show habits ranked by difficulty"""
        if not analytics_data:
            self.console.print("[yellow]No analytics data available[/yellow]")
            input("\nPress Enter to continue...")
            return
        
        # Sort by completion rate (lower = more difficult)
        sorted_habits = sorted(analytics_data, key=lambda x: x.completion_rate)
        
        self.console.print("\n[bold red]🏆 Habit Difficulty Rankings[/bold red]")
        
        difficulty_table = Table(box=box.ROUNDED, border_style="red")
        difficulty_table.add_column("Rank", justify="center", width=6)
        difficulty_table.add_column("Habit", width=30)
        difficulty_table.add_column("Completion Rate", justify="center", width=15)
        difficulty_table.add_column("Difficulty", justify="center", width=15)
        
        for i, analytics in enumerate(sorted_habits, 1):
            rank = f"#{i}"
            rate = f"{analytics.completion_rate:.1f}%"
            difficulty = analytics.get_difficulty_level()
            
            # Color coding for difficulty
            if difficulty in ["Very Difficult", "Difficult"]:
                difficulty_color = "red"
            elif difficulty == "Challenging":
                difficulty_color = "yellow"
            elif difficulty == "Moderate":
                difficulty_color = "blue"
            else:
                difficulty_color = "green"
            
            difficulty_table.add_row(
                rank,
                analytics.habit_name,
                rate,
                f"[{difficulty_color}]{difficulty}[/{difficulty_color}]"
            )
        
        self.console.print(difficulty_table)
        input("\nPress Enter to continue...")
    
    def _show_recommendations(self, analytics_data):
        """Show personalized recommendations"""
        if not analytics_data:
            self.console.print("[yellow]No analytics data available[/yellow]")
            input("\nPress Enter to continue...")
            return
        
        try:
            # Get recommendations from analytics service
            weekly_summary = self.analytics_service.get_weekly_progress_summary()
            
            self.console.print("\n[bold bright_magenta]💡 Personalized Recommendations[/bold bright_magenta]")
            
            recommendations = []
            
            # Analyze completion rates
            struggling_habits = [a for a in analytics_data if a.completion_rate < 40]
            excellent_habits = [a for a in analytics_data if a.completion_rate > 85]
            
            if struggling_habits:
                habit_names = [h.habit_name for h in struggling_habits[:2]]
                recommendations.append(f"🎯 Focus on: {', '.join(habit_names)} - they need the most attention")
            
            if excellent_habits:
                recommendations.append(f"🌟 Great job with {len(excellent_habits)} habits! Keep up the momentum")
            
            # Streak recommendations
            no_streak_habits = [a for a in analytics_data if a.current_streak == 0]
            if no_streak_habits:
                recommendations.append("🔥 Try to build a streak with at least one habit this week")
            
            # Balance recommendations
            total_completion_rate = sum(a.completion_rate for a in analytics_data) / len(analytics_data)
            if total_completion_rate < 60:
                recommendations.append("📉 Consider reducing the number of habits to focus on consistency")
            elif total_completion_rate > 85:
                recommendations.append("📈 You're doing amazing! Consider adding a new challenging habit")
            
            if not recommendations:
                recommendations.append("✨ You're on the right track! Keep maintaining your habits")
            
            for i, rec in enumerate(recommendations, 1):
                self.console.print(f"{i}. {rec}")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error generating recommendations: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def _show_advanced_analytics(self):
        """Show advanced predictive analytics using analytics.py functions"""
        try:
            habits = self.habit_service.get_all_habits()
            
            if not habits:
                self.console.print("[yellow]No habits found for advanced analytics[/yellow]")
                input("\nPress Enter to continue...")
                return
            
            self.console.clear()
            self.show_header()
            
            self.console.print(Panel(
                "[bold bright_magenta]🎯 Advanced Predictive Analytics[/bold bright_magenta]",
                border_style="bright_magenta"
            ))
            
            # Show menu for advanced analytics
            self.console.print("\n[bold bright_magenta]Advanced Analytics Options:[/bold bright_magenta]")
            self.console.print("1. 🎲 Habit Persistence Probability")
            self.console.print("2. 📊 Difficulty Prediction Analysis")
            self.console.print("3. 🔥 Streak Continuation Prediction")
            self.console.print("4. 📋 Complete Advanced Report")
            self.console.print("5. 🔙 Back to analytics menu")
            
            choice = Prompt.ask("\nSelect analysis type", choices=["1", "2", "3", "4", "5"], default="5")
            
            if choice == "1":
                self._show_persistence_probability()
            elif choice == "2":
                self._show_difficulty_prediction()
            elif choice == "3":
                self._show_streak_prediction()
            elif choice == "4":
                self._show_complete_advanced_report()
            # Choice 5 returns to previous menu
            
        except Exception as e:
            self.console.print(f"[red]❌ Error in advanced analytics: {e}[/red]")
            input("\nPress Enter to continue...")

    def _show_persistence_probability(self):
        """Show habit persistence probability analysis"""
        try:
            habits = self.habit_service.get_all_habits()
            
            self.console.print("\n[bold bright_cyan]🎲 Habit Persistence Probability Analysis[/bold bright_cyan]")
            
            persistence_table = Table(box=box.ROUNDED, border_style="bright_cyan")
            persistence_table.add_column("Habit", width=25)
            persistence_table.add_column("Probability", justify="center", width=12)
            persistence_table.add_column("Trend", justify="center", width=12)
            persistence_table.add_column("Confidence", justify="center", width=12)
            persistence_table.add_column("Key Factor", width=20)
            
            for habit in habits:
                # Calculate persistence probability using service
                persistence_result = self.analytics_service.calculate_habit_persistence_probability(
                    habit.habit_id
                )
                
                probability = persistence_result.get('probability', 0.0)
                trend = persistence_result.get('trend_direction', 'unknown')
                confidence = persistence_result.get('confidence', 'low')
                
                # Determine dominant factor
                factors = persistence_result.get('factors', {})
                if factors:
                    max_factor = max(factors.items(), key=lambda x: abs(x[1]))[0]
                    key_factor = max_factor.replace('_', ' ').title()
                else:
                    key_factor = "N/A"
                
                # Color coding
                prob_color = "bright_green" if probability > 0.7 else "bright_yellow" if probability > 0.4 else "red"
                trend_color = "bright_green" if trend == "improving" else "red" if trend == "declining" else "white"
                
                persistence_table.add_row(
                    habit.habit_name,
                    f"[{prob_color}]{probability:.1%}[/{prob_color}]",
                    f"[{trend_color}]{trend}[/{trend_color}]",
                    confidence,
                    key_factor
                )
            
            self.console.print(persistence_table)
            
        except Exception as e:
            self.console.print(f"[red]❌ Error in persistence analysis: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def _show_difficulty_prediction(self):
        """Show habit difficulty prediction analysis"""
        try:
            habits = self.habit_service.get_all_habits()
            
            self.console.print("\n[bold bright_yellow]📊 Habit Difficulty Prediction Analysis[/bold bright_yellow]")
            
            difficulty_table = Table(box=box.ROUNDED, border_style="bright_yellow")
            difficulty_table.add_column("Habit", width=25)
            difficulty_table.add_column("Predicted Difficulty", justify="center", width=18)
            difficulty_table.add_column("Early Performance", justify="center", width=16)
            difficulty_table.add_column("Dropout Risk", justify="center", width=12)
            difficulty_table.add_column("Confidence", justify="center", width=12)
            
            for habit in habits:
                # Get completion history
                completions = self.completion_service.get_habit_completions(habit.habit_id, limit=30)
                
                if len(completions) >= 7:  # Need at least a week of data
                    # Predict difficulty using service
                    difficulty_result = self.analytics_service.predict_habit_difficulty(habit.habit_id)
                    
                    predicted_difficulty = difficulty_result.get('predicted_difficulty', 'unknown')
                    early_performance = difficulty_result.get('early_performance_rate', 0.0)
                    dropout_risk = difficulty_result.get('dropout_risk_score', 0.0)
                    confidence = difficulty_result.get('confidence', 'low')
                    
                    # Color coding
                    if predicted_difficulty == 'easy':
                        diff_color = "bright_green"
                    elif predicted_difficulty == 'moderate':
                        diff_color = "bright_cyan"
                    elif predicted_difficulty == 'challenging':
                        diff_color = "bright_yellow"
                    else:
                        diff_color = "red"
                    
                    perf_color = "bright_green" if early_performance > 80 else "bright_yellow" if early_performance > 60 else "red"
                    risk_color = "red" if dropout_risk > 0.6 else "bright_yellow" if dropout_risk > 0.3 else "bright_green"
                    
                    difficulty_table.add_row(
                        habit.habit_name,
                        f"[{diff_color}]{predicted_difficulty.title()}[/{diff_color}]",
                        f"[{perf_color}]{early_performance:.1f}%[/{perf_color}]",
                        f"[{risk_color}]{dropout_risk:.1%}[/{risk_color}]",
                        confidence
                    )
                else:
                    difficulty_table.add_row(
                        habit.habit_name,
                        "[dim]Need more data[/dim]",
                        "[dim]N/A[/dim]",
                        "[dim]N/A[/dim]",
                        "low"
                    )
            
            self.console.print(difficulty_table)
            
        except Exception as e:
            self.console.print(f"[red]❌ Error in difficulty prediction: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def _show_streak_prediction(self):
        """Show streak continuation prediction analysis"""
        try:
            habits = self.habit_service.get_all_habits()
            analytics_data = self.analytics_service.get_all_habits_analytics()
            
            self.console.print("\n[bold bright_red]🔥 Streak Continuation Prediction Analysis[/bold bright_red]")
            
            streak_table = Table(box=box.ROUNDED, border_style="bright_red")
            streak_table.add_column("Habit", width=25)
            streak_table.add_column("Current Streak", justify="center", width=14)
            streak_table.add_column("Continuation Prob", justify="center", width=16)
            streak_table.add_column("Momentum", justify="center", width=12)
            streak_table.add_column("Next Milestone", justify="center", width=15)
            
            for habit in habits:
                # Get current streak from analytics
                habit_analytics = next((a for a in analytics_data if a.habit_id == habit.habit_id), None)
                current_streak = habit_analytics.current_streak if habit_analytics else 0
                
                # Get completion history
                completions = self.completion_service.get_habit_completions(habit.habit_id)
                completion_dates = [c.completion_date for c in completions]
                
                if current_streak > 0:
                    # Predict streak continuation using service
                    streak_result = self.analytics_service.predict_streak_continuation(habit.habit_id)
                    
                    continuation_prob = streak_result.get('continuation_probability', 0.0)
                    momentum = streak_result.get('streak_momentum', 'weak')
                    milestones = streak_result.get('milestone_predictions', {})
                    
                    # Find next achievable milestone
                    next_milestone = "None"
                    for milestone, prob in milestones.items():
                        milestone_days = int(milestone.split('_')[0])
                        if milestone_days > current_streak and prob > 0.3:
                            next_milestone = f"{milestone_days} days ({prob:.1%})"
                            break
                    
                    # Color coding
                    prob_color = "bright_green" if continuation_prob > 0.7 else "bright_yellow" if continuation_prob > 0.4 else "red"
                    momentum_color = "bright_green" if momentum == "strong" else "bright_yellow" if momentum == "moderate" else "red"
                    
                    streak_table.add_row(
                        habit.habit_name,
                        f"[bright_green]{current_streak} days[/bright_green]",
                        f"[{prob_color}]{continuation_prob:.1%}[/{prob_color}]",
                        f"[{momentum_color}]{momentum}[/{momentum_color}]",
                        next_milestone
                    )
                else:
                    streak_table.add_row(
                        habit.habit_name,
                        "[dim]0 days[/dim]",
                        "[dim]N/A[/dim]",
                        "[dim]No streak[/dim]",
                        "[dim]Build streak first[/dim]"
                    )
            
            self.console.print(streak_table)
            
        except Exception as e:
            self.console.print(f"[red]❌ Error in streak prediction: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def _show_complete_advanced_report(self):
        """Show a complete advanced analytics report"""
        try:
            habits = self.habit_service.get_all_habits()
            analytics_data = self.analytics_service.get_all_habits_analytics()
            
            self.console.clear()
            self.show_header()
            
            self.console.print(Panel(
                "[bold bright_magenta]📋 Complete Advanced Analytics Report[/bold bright_magenta]",
                border_style="bright_magenta"
            ))
            
            for habit in habits:
                # Get completion history
                completions = self.completion_service.get_habit_completions(habit.habit_id)
                completion_dates = [c.completion_date for c in completions]
                
                # Get current streak
                habit_analytics = next((a for a in analytics_data if a.habit_id == habit.habit_id), None)
                current_streak = habit_analytics.current_streak if habit_analytics else 0
                
                self.console.print(f"\n[bold bright_cyan]🎯 {habit.habit_name}[/bold bright_cyan]")
                
                # Persistence Analysis using service
                persistence_result = self.analytics_service.calculate_habit_persistence_probability(habit.habit_id)
                probability = persistence_result.get('probability', 0.0)
                trend = persistence_result.get('trend_direction', 'unknown')
                
                self.console.print(f"   📊 Persistence Probability: [bold]{probability:.1%}[/bold] ({trend} trend)")
                
                # Difficulty Analysis (if enough data)
                if len(completions) >= 7:
                    difficulty_result = self.analytics_service.predict_habit_difficulty(habit.habit_id)
                    predicted_difficulty = difficulty_result.get('predicted_difficulty', 'unknown')
                    dropout_risk = difficulty_result.get('dropout_risk_score', 0.0)
                    
                    self.console.print(f"   🎯 Predicted Difficulty: [bold]{predicted_difficulty.title()}[/bold] (Dropout Risk: {dropout_risk:.1%})")
                    
                    # Show recommendations
                    recommendations = difficulty_result.get('recommendations', [])
                    if recommendations:
                        self.console.print("   💡 Recommendations:")
                        for rec in recommendations[:2]:  # Show top 2 recommendations
                            self.console.print(f"      • {rec}")
                
                # Streak Analysis (if active streak)
                if current_streak > 0:
                    streak_result = self.analytics_service.predict_streak_continuation(habit.habit_id)
                    continuation_prob = streak_result.get('continuation_probability', 0.0)
                    momentum = streak_result.get('streak_momentum', 'weak')
                    
                    self.console.print(f"   🔥 Current Streak: [bold]{current_streak} days[/bold] (Continuation: {continuation_prob:.1%}, {momentum} momentum)")
                    
                    # Show milestone predictions
                    milestones = streak_result.get('milestone_predictions', {})
                    next_milestone = None
                    for milestone, prob in milestones.items():
                        milestone_days = int(milestone.split('_')[0])
                        if milestone_days > current_streak and prob > 0.3:
                            next_milestone = (milestone_days, prob)
                            break
                    
                    if next_milestone:
                        self.console.print(f"   🎯 Next Milestone: [bold]{next_milestone[0]} days[/bold] ({next_milestone[1]:.1%} probability)")
                else:
                    self.console.print("   🔥 No active streak - focus on building consistency")
            
            self.console.print(f"\n[dim]Report generated on {date.today().strftime('%B %d, %Y')}[/dim]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Error generating complete report: {e}[/red]")
        
        input("\nPress Enter to continue...")

    def search_habits_menu(self):
        """Search and filter habits with backend integration"""
        if not self.backend_ready:
            self.console.print("❌ Backend services are not available. Cannot search habits without database connection.", style="bold red")
            input("\nPress Enter to continue...")
            return
            
        self.console.clear()
        self.show_header()
        
        self.console.print(Panel(
            "[bold bright_cyan]🔍 Search & Filter Habits[/bold bright_cyan]",
            border_style="bright_cyan"
        ))
        
        search_term = Prompt.ask("Enter search term (or press Enter to see all)", default="")
        
        # Get habits and perform search
        try:
            if search_term.strip():
                filtered_habits = self.habit_service.search_habits(search_term)
            else:
                filtered_habits = self.habit_service.get_all_habits()
        except Exception as e:
            self.console.print(f"❌ Error searching habits: {e}", style="bold red")
            filtered_habits = []
        
        if filtered_habits:
            results_table = Table(box=box.ROUNDED, border_style="bright_cyan")
            results_table.add_column("Habit", width=30)
            results_table.add_column("Description", width=35)
            results_table.add_column("Period", justify="center", width=10)
            results_table.add_column("Status", justify="center", width=10)
            
            for habit in filtered_habits:
                habit_name = habit.habit_name
                description = habit.description
                period = habit.period.value if hasattr(habit.period, 'value') else str(habit.period)
                status = "✅ Active" if habit.is_active else "❌ Inactive"
                
                results_table.add_row(habit_name, description, period, status)
            
            results_panel = Panel(
                results_table,
                title=f"[bold bright_cyan]🔍 Search Results ({len(filtered_habits)} found)[/bold bright_cyan]",
                border_style="bright_cyan"
            )
            self.console.print(results_panel)
            
            # Show additional filter options
            self.console.print("\n[bold bright_cyan]Filter Options:[/bold bright_cyan]")
            self.console.print("1. 📅 Filter by daily habits only")
            self.console.print("2. 📆 Filter by weekly habits only")
            self.console.print("3. 🔄 Search again")
            self.console.print("4. 🔙 Back to main menu")
            
            choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4"], default="4")
            
            if choice == "1":
                self._filter_by_period(filtered_habits, "daily")
            elif choice == "2":
                self._filter_by_period(filtered_habits, "weekly")
            elif choice == "3":
                self.search_habits_menu()  # Recursive call for new search
            # Choice 4 (back) will naturally exit the method
            
        else:
            no_results_panel = Panel(
                Align.center(f"No habits found matching '{search_term}'" if search_term else "No habits available"),
                style="yellow",
                title="🔍 Search Results"
            )
            self.console.print(no_results_panel)
            input("\nPress Enter to continue...")
    
    def _filter_by_period(self, habits, period_filter):
        """Filter habits by period"""
        filtered = [h for h in habits if h.period.value == period_filter]
        
        if filtered:
            self.console.print(f"\n[bold bright_magenta]📅 {period_filter.title()} Habits ({len(filtered)} found)[/bold bright_magenta]")
            
            for i, habit in enumerate(filtered, 1):
                name = habit.habit_name
                desc = habit.description
                
                self.console.print(f"{i}. [bold]{name}[/bold]")
                if desc:
                    self.console.print(f"   [dim]{desc}[/dim]")
        else:
            self.console.print(f"[yellow]No {period_filter} habits found[/yellow]")
        
        input("\nPress Enter to continue...")

    def settings_menu(self):
        """Settings menu"""
        self.console.clear()
        self.show_header()
        
        settings_panel = Panel("""[bold bright_magenta]⚙️ Settings[/bold bright_magenta]

[dim]Settings functionality coming soon![/dim]

Future features:
• 🌙 Dark/Light theme toggle
• 🔔 Notification preferences  
• 📅 Default habit periods
• 💾 Export/Import data
• 🔄 Sync preferences
        """, border_style="bright_magenta")
        
        self.console.print(settings_panel)
        input("\nPress Enter to continue...")

    def help_menu(self):
        """Help and information"""
        self.console.clear()
        self.show_header()
        
        help_text = """[bold bright_blue]❓ Help & Information[/bold bright_blue]

[bold]How to use Habit Tracker:[/bold]

🏁 [bold]Getting Started:[/bold]
  • Create your first habit using 'Manage Habits'
  • Set it as daily or weekly
  • Start logging completions each day

✅ [bold]Logging Habits:[/bold]
  • Use 'Log Habit Completion' to mark habits as done
  • Build streaks by completing habits consistently
  • Track your progress over time

📊 [bold]Analytics:[/bold]
  • View your current streaks and statistics  
  • See which habits you're doing well with
  • Identify areas for improvement

🔍 [bold]Search & Filter:[/bold]
  • Find specific habits quickly
  • Filter by daily/weekly habits
  • Organize your habit list

[dim]For more help, visit our documentation or contact support.[/dim]
        """
        
        help_panel = Panel(help_text, border_style="bright_blue")
        self.console.print(help_panel)
        input("\nPress Enter to continue...")

    def run(self):
        """Main application loop"""
        try:
            while True:
                self.show_main_menu()
                
                choice = Prompt.ask(
                    "[bold bright_cyan]Select an option[/bold bright_cyan]",
                    choices=["1", "2", "3", "4", "5", "6", "7"],
                    default="1"
                )
                
                if choice == "1":
                    self.manage_habits_menu()
                elif choice == "2":
                    self.log_completion_menu()
                elif choice == "3":
                    self.view_analytics_menu()
                elif choice == "4":
                    self.search_habits_menu()
                elif choice == "5":
                    self.settings_menu()
                elif choice == "6":
                    self.help_menu()
                elif choice == "7":
                    self.console.print()
                    self.console.print(Panel(
                        "[bold bright_yellow]Thanks for using Habit Tracker! 🌟\nKeep building those great habits! 💪[/bold bright_yellow]",
                        border_style="bright_yellow"
                    ))
                    sys.exit(0)
                    
        except KeyboardInterrupt:
            self.console.print("\n[dim]Goodbye! 👋[/dim]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")
            sys.exit(1)

def main():
    """Main entry point"""
    app = HabitTrackerCLI()
    app.run()

if __name__ == "__main__":
    main()