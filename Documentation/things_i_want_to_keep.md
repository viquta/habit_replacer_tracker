here is a list of functionalities that I want to keep or rearrange:


1- create habit (yes)
2- delete and edit habit (yes, but it's not essential, still keep)
3- have a script that fills in 5 predefned habits (at least one weekly and one daily) with tracking data for the past 4 weeks (yes it's in init-db.sql)
4- system that tracks when habit ahs been created, date and times habit tasks are completed + persistent data storage (yes)
5- analytics module (analytics.py) that uses functional programming to do: 
    a. return list of currently tracked habits 
    b. return list of all habits with same periodicity,
    c. return longest run streak of all defined habits, 
    d. return longest run streka for a given habit
    (hence, the analytics.py needs to change to this and these new functions need to be implemented in the services and the cli needs to use them)
6-i need to update the test_backend.py to test the things i want to keep and the things i need

