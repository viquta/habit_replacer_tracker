#!/usr/bin/env python3

##################################################################################
#prompt to Claude Sonnet 4 (with context from the previous conversation and access to 
#repo requirements that I wrote earlier (see Documentation/project_requirements.md)): 
#I don't have a backend or a database connection set yet, and I'd like to 
# first create a CLI with dummy components just see how it will look like.
#
#I'm imagining something like:
#📝 Manage Habits
#✅ Log Habit Completion
#📊 View Progress & Analytics
#🔍 Search & Filter Habits
#⚙️ Settings
#❓ Help
#🚪 Exit
#And is there a way to have the CLI more "app like / GUI like"? 
# i think there was some click library and make it nice and colorful. Please :)
##################################################################################
"""
Habit Tracker CLI Application
Users can create, manage, and inspect habits they define in a convenient way
"""

import sys
#import os #will need later
from datetime import datetime, date
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich.tree import Tree
from rich import box
import time

class DummyHabit:
    """Dummy habit class for demonstration purposes"""
    def __init__(self, name: str, description: str, period: str, created_date: date):
        self.name = name
        self.description = description
        self.period = period  # 'daily' or 'weekly'
        self.created_date = created_date
        self.completions = []  # List of completion dates
        self.streak = 0

class HabitTrackerCLI:
    def __init__(self):
        self.console = Console()
        self.habits = self._load_dummy_habits()
        
    def _load_dummy_habits(self) -> List[DummyHabit]:
        """Load some dummy habits for demonstration"""
        dummy_habits = [
            DummyHabit("💧 Drink 8 glasses of water", "Stay hydrated throughout the day", "daily", date(2025, 1, 1)),
            DummyHabit("📖 Read for 30 minutes", "Read books or articles for personal growth", "daily", date(2025, 1, 5)),
            DummyHabit("🏃‍♂️ Exercise", "Physical activity for health", "daily", date(2025, 1, 10)),
            DummyHabit("🧘 Meditation", "10 minutes of mindfulness", "daily", date(2025, 1, 15)),
            DummyHabit("🏠 Clean house", "Weekly house cleaning routine", "weekly", date(2025, 1, 7)),
        ]
        
        # Add some dummy completion data
        for habit in dummy_habits:
            if habit.period == "daily":
                habit.streak = 5
            else:
                habit.streak = 2
                
        return dummy_habits

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
        status_text = Text()
        status_text.append(f"📅 Today: {datetime.now().strftime('%B %d, %Y')} | ", style="dim")
        status_text.append(f"🎯 Active Habits: {len(self.habits)} | ", style="dim")
        status_text.append(f"⚡ Total Streaks: {sum(h.streak for h in self.habits)}", style="dim")
        
        self.console.print(Align.center(status_text))
        self.console.print()

    def manage_habits_menu(self):
        """Submenu for habit management"""
        self.console.clear()
        self.show_header()
        
        # Create habits table
        habits_table = Table(
            title="[bold bright_green]Your Habits[/bold bright_green]",
            box=box.ROUNDED,
            border_style="bright_green"
        )
        
        habits_table.add_column("Habit", style="bold", width=30)
        habits_table.add_column("Period", justify="center", width=10)
        habits_table.add_column("Streak", justify="center", width=8)
        habits_table.add_column("Created", justify="center", width=12)
        
        for habit in self.habits:
            period_style = "bright_yellow" if habit.period == "daily" else "bright_magenta"
            streak_style = "bright_green" if habit.streak > 0 else "dim"
            
            habits_table.add_row(
                habit.name,
                f"[{period_style}]{habit.period}[/{period_style}]",
                f"[{streak_style}]{habit.streak}[/{streak_style}]",
                habit.created_date.strftime("%b %d")
            )
        
        self.console.print(habits_table)
        self.console.print()
        
        # Management options
        options = [
            ("1", "➕ Create new habit"),
            ("2", "✏️  Edit existing habit"),
            ("3", "🗑️  Delete habit"),
            ("4", "⬅️  Back to main menu")
        ]
        
        for num, option in options:
            self.console.print(f"  {num}. {option}")
        
        self.console.print()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            self.create_habit()
        elif choice == "2":
            self.console.print("[yellow]Edit functionality - Coming soon![/yellow]")
            input("\nPress Enter to continue...")
        elif choice == "3":
            self.console.print("[red]Delete functionality - Coming soon![/red]")
            input("\nPress Enter to continue...")
        elif choice == "4":
            return

    def create_habit(self):
        """Create a new habit (dummy implementation)"""
        self.console.print()
        self.console.print(Panel(
            "[bold bright_green]Create New Habit[/bold bright_green]",
            border_style="bright_green"
        ))
        
        name = Prompt.ask("🏷️  Habit name")
        description = Prompt.ask("📝 Description")
        period = Prompt.ask("⏰ Period", choices=["daily", "weekly"], default="daily")
        
        # Simulate creating habit
        with Progress(
            TextColumn("[bold blue]Creating habit..."),
            BarColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("Creating", total=100)
            for i in range(100):
                time.sleep(0.01)
                progress.update(task, advance=1)
        
        self.console.print(f"[bright_green]✅ Habit '{name}' created successfully![/bright_green]")
        input("\nPress Enter to continue...")

    def log_completion_menu(self):
        """Menu for logging habit completions"""
        self.console.clear()
        self.show_header()
        
        self.console.print(Panel(
            "[bold bright_yellow]Log Habit Completion[/bold bright_yellow]",
            border_style="bright_yellow"
        ))
        
        # Show today's habits
        today_table = Table(
            title="[bold]Today's Habits[/bold]",
            box=box.ROUNDED,
            border_style="bright_yellow"
        )
        
        today_table.add_column("", width=3)
        today_table.add_column("Habit", width=35)
        today_table.add_column("Status", justify="center", width=15)
        
        for i, habit in enumerate(self.habits, 1):
            if habit.period == "daily":
                status = "[bright_green]✅ Done[/bright_green]" if i % 2 == 0 else "[dim]⏳ Pending[/dim]"
                today_table.add_row(str(i), habit.name, status)
        
        self.console.print(today_table)
        self.console.print()
        
        choice = Prompt.ask("Select habit to complete (or 'b' for back)", default="b")
        if choice.lower() != 'b':
            self.console.print(f"[bright_green]✅ Habit completed! Streak updated![/bright_green]")
            input("\nPress Enter to continue...")

    def view_analytics_menu(self):
        """Display progress and analytics"""
        self.console.clear()
        self.show_header()
        
        # Create analytics dashboard
        analytics_layout = Table.grid(padding=1)
        analytics_layout.add_column()
        analytics_layout.add_column()
        
        # Streaks panel
        streaks_table = Table(box=box.ROUNDED, border_style="bright_blue")
        streaks_table.add_column("Habit", width=25)
        streaks_table.add_column("Current Streak", justify="center", width=15)
        
        for habit in sorted(self.habits, key=lambda x: x.streak, reverse=True):
            streak_color = "bright_green" if habit.streak >= 7 else "bright_yellow" if habit.streak >= 3 else "white"
            streaks_table.add_row(
                habit.name,
                f"[{streak_color}]{habit.streak} days[/{streak_color}]"
            )
        
        streaks_panel = Panel(
            streaks_table,
            title="[bold bright_blue]🔥 Current Streaks[/bold bright_blue]",
            border_style="bright_blue"
        )
        
        # Stats panel
        total_habits = len(self.habits)
        daily_habits = len([h for h in self.habits if h.period == "daily"])
        weekly_habits = len([h for h in self.habits if h.period == "weekly"])
        avg_streak = sum(h.streak for h in self.habits) / total_habits if total_habits > 0 else 0
        
        stats_text = f"""
[bold]📊 Statistics[/bold]

Total Habits: [bright_cyan]{total_habits}[/bright_cyan]
Daily Habits: [bright_yellow]{daily_habits}[/bright_yellow]
Weekly Habits: [bright_magenta]{weekly_habits}[/bright_magenta]
Average Streak: [bright_green]{avg_streak:.1f} days[/bright_green]
Longest Streak: [bright_red]{max(h.streak for h in self.habits) if self.habits else 0} days[/bright_red]
        """
        
        stats_panel = Panel(
            stats_text.strip(),
            border_style="bright_green"
        )
        
        analytics_layout.add_row(streaks_panel, stats_panel)
        self.console.print(analytics_layout)
        
        self.console.print()
        input("Press Enter to continue...")

    def search_habits_menu(self):
        """Search and filter habits"""
        self.console.clear()
        self.show_header()
        
        self.console.print(Panel(
            "[bold bright_cyan]🔍 Search & Filter Habits[/bold bright_cyan]",
            border_style="bright_cyan"
        ))
        
        search_term = Prompt.ask("Enter search term (or press Enter to see all)")
        
        # Simple search simulation
        filtered_habits = [h for h in self.habits if search_term.lower() in h.name.lower()] if search_term else self.habits
        
        if filtered_habits:
            results_table = Table(box=box.ROUNDED, border_style="bright_cyan")
            results_table.add_column("Habit", width=30)
            results_table.add_column("Description", width=35)
            results_table.add_column("Period", justify="center", width=10)
            
            for habit in filtered_habits:
                results_table.add_row(habit.name, habit.description, habit.period)
            
            self.console.print(results_table)
        else:
            self.console.print("[yellow]No habits found matching your search.[/yellow]")
        
        self.console.print()
        input("Press Enter to continue...")

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