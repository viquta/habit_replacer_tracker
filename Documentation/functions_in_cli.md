CLI.py (Presentation)
    ↓ uses models for data transfer
services.py (Business Logic)  
    ↓ uses models for domain operations
database.py (Data Access)
    ↓ converts between models and database records
models.py (Domain Models) ← **Foundation for everything**




...

CLI.py
    ↓
services.py  
    ↓
database.py → BaseDAO.get_db_connection()
    ↓
db_connection.py → get_connection()
    ↓
config.py → get_database_connection_string()  ← **Critical Link!**
    ↓
SQL Server (localhost\SQLEXPRESS)



viquta: which which functions the CLI is using, which ones call which backend functions and which ones call init-db.sql 

GitHub Copilot: I'll analyze the CLI code to identify which functions are being used, their relationships with backend functions, and any connections to the database initialization. Let me examine the code structure and dependencies. Now let me look at the backend services and database files to understand the complete function hierarchy: Based on the analysis of the code and file structure, I can now provide a comprehensive overview of the CLI functions, their backend relationships, and database connections.

## CLI Functions and Their Backend Function Calls

Here's the breakdown of which CLI functions call which backend functions and how they connect to the database:

### **1. CLI Initialization (`__init__`)**
**Backend Services Initialized:**
- `SystemService()` - System initialization and health checks
- `HabitService()` - Core habit management 
- `HabitCompletionService()` - Completion tracking
- `HabitAnalyticsService()` - Analytics and insights
- `UserService()` - User management

**Database Connection:**
- Calls `SystemService.initialize_system()` which creates demo user and habits if none exist
- This eventually calls the init-db.sql script through the database setup process

### **2. Main Menu Functions**

#### **`manage_habits_menu()`**
**Backend Functions Called:**
- `HabitService.get_all_habits()` → `HabitDAO.get_habits_by_user_id()`
- `HabitService.create_habit()` → `HabitDAO.create_habit()`
- `HabitService.update_habit()` → `HabitDAO.update_habit()`
- `HabitService.delete_habit()` → `HabitDAO.delete_habit()`

#### **`log_completion_menu()`**
**Backend Functions Called:**
- `HabitService.get_all_habits()` → `HabitDAO.get_habits_by_user_id()`
- `HabitService.get_habits_due_today()` → Custom logic with `HabitCompletionDAO`
- `HabitCompletionService.is_habit_completed_today()` → `HabitCompletionDAO.get_completion_by_habit_and_date()`
- `HabitCompletionService.complete_habit()` → `HabitCompletionDAO.create_completion()`
- `HabitCompletionService.uncomplete_habit()` → `HabitCompletionDAO.delete_completion()`
- `HabitCompletionService.get_completion_calendar()` → `HabitCompletionDAO.get_completions_by_date_range()`

#### **`view_analytics_menu()`**
**Backend Functions Called:**
- `HabitService.get_all_habits()` → `HabitDAO.get_habits_by_user_id()`
- `HabitAnalyticsService.get_all_habits_analytics()` → Multiple DAO calls
- `HabitAnalyticsService.get_habit_trends()` → `HabitCompletionService.get_completions_for_date_range()`
- `HabitAnalyticsService.get_weekly_progress_summary()` → Multiple completion queries

#### **`search_habits_menu()`**
**Backend Functions Called:**
- `HabitService.search_habits()` → `HabitDAO.search_habits()`
- `HabitService.get_all_habits()` → `HabitDAO.get_habits_by_user_id()`

### **3. Backend Service Hierarchy**

#### **UserService**
- `create_demo_user()` → `UserDAO.create_user()`
- `get_current_user()` → `UserDAO.get_user_by_username()`

#### **HabitService**
- `create_habit()` → `HabitDAO.create_habit()`
- `get_all_habits()` → `HabitDAO.get_habits_by_user_id()`
- `get_habit_by_id()` → `HabitDAO.get_habit_by_id()`
- `update_habit()` → `HabitDAO.update_habit()`
- `delete_habit()` → `HabitDAO.delete_habit()`
- `search_habits()` → `HabitDAO.search_habits()`
- `get_habits_due_today()` → Custom logic using `HabitCompletionDAO`

#### **HabitCompletionService**
- `complete_habit()` → `HabitCompletionDAO.create_completion()`
- `uncomplete_habit()` → `HabitCompletionDAO.delete_completion()`
- `get_habit_completions()` → `HabitCompletionDAO.get_completions_by_habit_id()`
- `is_habit_completed_today()` → `HabitCompletionDAO.get_completion_by_habit_and_date()`
- `get_completion_calendar()` → `HabitCompletionDAO.get_completions_by_date_range()`

#### **HabitAnalyticsService**
- `get_comprehensive_analytics()` → `AnalyticsDAO.get_current_streaks()`, `AnalyticsDAO.get_longest_streaks()`, `AnalyticsDAO.get_completion_statistics()`
- `get_all_habits_analytics()` → Multiple analytics DAO calls
- `get_habit_trends()` → `HabitCompletionService.get_completions_for_date_range()`
- `get_weekly_progress_summary()` → Multiple completion queries

#### **SystemService**
- `initialize_system()` → `UserService.create_demo_user()`, `HabitService.get_all_habits()`, creates demo habits
- `get_system_status()` → Multiple service health checks

### **4. Database Connection via init-db.sql**

**Direct Connection:**
- The init-db.sql script is **NOT directly called** by CLI functions
- Instead, it's executed during the database setup phase through setup.py

**Database Initialization Process:**
1. setup.py → `setup_database()` → Runs init-db.sql script
2. init-db.sql creates:
   - `HabitTrackerDB` database
   - Tables: `Users`, `Habits`, `HabitCompletions`
   - Analytics views: `CurrentStreaks`, `LongestStreaks`, `WeeklyProgress`
   - Sample data: 5 pre-defined habits with 4-week test data
   - Database roles and permissions

**Runtime Database Access:**
- All CLI functions → Backend Services → DAO Classes → `db_connection.get_connection()`
- The connection module imports from db_connection.py

### **5. Function Call Flow Example**

When a user creates a habit in the CLI:
```
CLI.create_habit() 
→ HabitService.create_habit()
→ UserService.get_current_user() 
→ UserDAO.get_user_by_username()
→ HabitDAO.create_habit()
→ BaseDAO.get_db_connection()
→ db_connection.get_connection()
→ SQL Server Database (created by init-db.sql)
```

The init-db.sql script provides the foundation database schema and initial data that all these functions operate on, but it's not directly called during runtime - only during the initial setup phase.