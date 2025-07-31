# Detailed Requirements: Habit Tracker Application

---

## Essential Functionalities Checklist

### Core Features
- [x] **CLI Interface**: No need for GUI, only CLI (for uni version at least)
- [ ] **Periodic Habits**: Habits must be "periodic" (example: brushing teeth *every day*)
            [x] can you choose in the cli?
            [ ] does the backend take care of the right thing?
            [x] does the database do it right?
- [ ] **Habit Management**: User can define new habits
            [x] can you create habits through the CLI?
            [ ] does the backend validate habit input?
            [ ] are habits stored properly in the database?
- [ ] **Task Completion**: Task can be completed (checked-off) at any point in time
            [ ] can you mark habits as complete in the CLI?
            [ ] does the backend record completion timestamps?
            [ ] are completions tracked in the database?

### Progress Tracking & Analytics
- [ ] **Progress Tracking**: Ticking off habit activities for daily/weekly habits → tracking the progress + possibility of streaks of x periods
  - Example: After a week of completing habit x daily, you get a 7-day streak
            [ ] can you view current streaks in the CLI?
            [ ] does the backend calculate streaks correctly?
            [ ] are streak calculations accurate for both daily and weekly habits?
- [ ] **Data Storage & Analysis**: Store tracking (habit created, description, times) and use for data analysis
        - Purpose: Not for marketing, but for giving statistical analysis of user's habit development
        - Metrics: Most difficult habit, easiest, longest habit streak, etc.
            [ ] is all habit data properly stored with timestamps?
            [ ] can the system identify patterns in habit completion?
            [ ] are analytics queries optimized for performance?
- [ ] **Analytics Module**: Use functional programming paradigm
  - Return list of current habits, periodicity, streaks, longest streak, etc.
            [x] are analytics functions pure and stateless?
            [x] can you get habit statistics through the CLI?
            [ ] do analytics calculations handle edge cases properly?

---

## Technical Requirements Checklist

### Development Environment
- [x] **Python Version**: At least Python version 3.7 (or later) + tools and libraries
- [ ] **No Third-Party Tools**: No third-party habit tracking tools
- [ ] **Programming Paradigm**: Use Object-Oriented programming
- [ ] **Habit Periods**: Users should be able to create habit periods (daily/weekly)

### Documentation & Setup
- [ ] **Installation Instructions**: Detailed + self-contained installation and run instructions
- [ ] **README File**: Comprehensive README file
- [ ] **Code Documentation**: Docstrings for all functions and classes
            [ ] do all classes have comprehensive docstrings?
            [ ] do all public methods have clear documentation?
            [ ] are parameter types and return values documented?

### Data & Testing
- [ ] **Pre-defined Habits**: Project comes with 5 pre-defined habits
  - [ ] At least one weekly habit
  - [ ] At least one daily habit
  - [ ] Clear documentation for each habit
- [x] **Test Data**: For each predefined habit → provide tracking data for 4-week period (for testing)
- [ ] **Database**: Use a relational database (MS SQL Server with Docker)
            [x] is the database schema properly normalized?
            [ ] are database connections handled efficiently?
            [ ] do database operations include proper error handling?

### API & Interface
- [ ] **Clean API**: Clean API by exposing CLI tool
  - [x] User can create habits
  - [ ] User can delete habits
  - [ ] User can analyze their habits
- [ ] **Unit Testing**: Unit tests for coding (pytest or unittest)
            [ ] do tests cover all core functionality?
            [ ] are edge cases properly tested?
            [ ] is test coverage above 80%?

---


