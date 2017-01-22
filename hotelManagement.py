import sqlite3
import sys

_conn = sqlite3.connect('cronhoteldb.db')

def parseConfig(configPath):

def createTables:
    _conn.executescript("""
        CREATE TABLE TaskTimes(
            TaskId INTEGER PRIMARY KEY NOT NULL,
            DoEvery INTEGER NOT NULL,
            NumTimes INTEGER NOT NULL
        );

        CREATE TABLE Tasks(
            TaskId INTEGER NOT NULL,
            TaskName TEXT NOT NULL,
            Parameter INTEGER,

            FOREIGN KEY(TaskId) REFERENCES TaskTimes(TaskId),
            PRIMARY KEY(TaskId)
        );

        CREATE TABLE Rooms(
            RoomNumber INTEGER PRIMARY KEY NOT NULL
        );

        CREATE TABLE Residents(
            RoomNumber INTEGER NOT NULL,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,

            FOREIGN KEY(RoomNumber) REFERENCES Rooms(RoomNumber),
            PRIMARY KEY(RoomNumber)
        );
    """)

def room(splited_data):

def breakfast(splited_data):

def wakeup(splited_data):

def clean(splited_data):

def insertData(data):
    splited_data=str.split(',')
    options={
        'room':room(splited_data),
        'clean':clean(splited_data),
        'wakeup':wakeup(splited_data),
        'breakfast':breakfast(splited_data),
    }
    options[splited_data[0]]()

def main(configPath):
    parseConfig(configPath)


if __name__ == '__main__':
    main(sys.argv)





