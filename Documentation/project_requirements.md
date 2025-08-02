# Project Requirements: Habit Tracker Application

## User Story (CURRENTLY NOT ACHIEVING THIS GOAL BUT ONLY THE ESSENTIALS)

> *"I have bad habits, and I am trying to replace them with good habits, but it's too difficult! If only there was an app that could help me."*

## Project Overview

**University Project**: Make a Python backend for a habit tracking app which I can roll out later.

**App Philosophy**: Thus, the goal for this app is to give the user a smooth experience to track and replace bad habits, with good ones. The smoothness part comes from the fact that the app will assume that the user is performing the habit, unless they log in that they have not performed the routine.

---

## Essential Functionalities Checklist

### Core Features
- [x] **CLI Interface**: No need for GUI, only CLI (for uni version at least)
- [x] **Periodic Habits**: Habits must be "periodic" (example: brushing teeth *every day*)
- [x] **Habit Management**: User can define new habits
- [x] **Task Completion**: Task can be completed (checked-off) at any point in time

### Progress Tracking & Analytics
- [ ] **Progress Tracking**: Ticking off habit activities for daily/weekly habits → tracking the progress + possibility of streaks of x periods
  -(NOT NECESSARY FOR ESSENTIAL FUNCTIONALITY) Example: After a week of completing habit x daily, you get a 7-day streak
- [x] **Data Storage & Analysis**: Store tracking (habit created, description, times) and use for data analysis
  - Purpose: Not for marketing, but for giving statistical analysis of user's habit development
  - Metrics: Most difficult habit, easiest, longest habit streak, etc.
- [x] **Analytics Module**: Use functional programming paradigm
  - Return list of current habits, periodicity, streaks, longest streak, etc.

---

## Technical Requirements Checklist

### Development Environment
- [x] **Python Version**: At least Python version 3.7 (or later) + tools and libraries
- [x] **No Third-Party Tools**: No third-party habit tracking tools
- [x] **Programming Paradigm**: Use Object-Oriented programming

### Documentation & Setup
- [ ] **Installation Instructions**: Detailed + self-contained installation and run instructions
- [ ] **README File**: Comprehensive README file
- [x] **Code Documentation**: Docstrings for all functions and classes

### Data & Testing
- [ ] **Pre-defined Habits**: Project comes with 5 pre-defined habits
  - [ ] At least one weekly habit
  - [ ] At least one daily habit
  - [ ] Clear documentation for each habit
- [ ] **Test Data**: For each predefined habit → provide tracking data for 4-week period (for testing)
- [ ] **Database**: Use a relational database (MS SQL Server with Docker)

### API & Interface
- [ ] **Clean API**: Clean API by exposing CLI tool
  - [ ] User can create habits
  - [ ] User can delete habits
  - [ ] User can analyze their habits
- [x] **Unit Testing**: Unit tests for coding (pytest or unittest)

---

## Implementation Notes

- **Database Choice**: MS SQL Server with Docker
- **Testing Framework**: pytest or unittest
- **Analytics Approach**: Functional programming paradigm for analytics module

