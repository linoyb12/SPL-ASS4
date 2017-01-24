import sqlite3
import sys
from itertools import count


_conn = sqlite3.connect('cronhoteldb.db')
_taskId = 1
#_tasks = count()
#next(_tasks)

def next_id():
    global _taskId;
    _taskId += 1

def create_tables():
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
    _conn.execute("""
        INSERT INTO Rooms (RoomNumber) VALUES (?)
    """, [splited_data[1]])

    if splited_data.__len__() > 2:
        _conn.execute("""
            INSERT INTO Residents(RoomNumber, FirstName, LastName) VALUES (?, ?, ?)""", [splited_data[1],
                                                                                         splited_data[2],
                                                                                         splited_data[3]])


def breakfast_n_wakup(splited_data):
    _conn.execute("""
            INSERT INTO TaskTimes (TaskId, DoEvery, NumTimes) VALUES (?, ?, ?)""", [_taskId, splited_data[1], splited_data[3]])
    _conn.execute("""
        INSERT INTO Tasks (TaskId, TaskName, Parameter) VALUES (?, ?, ?)""", [_taskId, splited_data[0], splited_data[2]])
    next_id()


def clean(splited_data):
    _conn.execute("""
            INSERT INTO TaskTimes (TaskId, DoEvery, NumTimes) VALUES (?, ?, ?)""",
                  [_taskId, splited_data[1], splited_data[2]])
    _conn.execute("""
        INSERT INTO Tasks (TaskId, TaskName, Parameter) VALUES (?, ?, ?)""", [_taskId, splited_data[0], 0 ])
    next_id()

def insert_data(data):
    splited_data=data.split(',')
    options = {
        'room': room,
        'clean': clean,
        'wakeup': breakfast_n_wakup,
        'breakfast': breakfast_n_wakup,
    }
    options[splited_data[0]](splited_data)


def parse_config(config_path):
    with open(config_path) as input_file:
        for line in input_file:
            insert_data(line.strip())


def _close_db():
    _conn.commit()
    _conn.close()


def main(config_path):
    create_tables()
    parse_config(config_path)
    _close_db()


if __name__ == '__main__':
    #main(sys.argv)
    main("C:\\Users\\linoy\\Desktop\\assa4\\assignment4_shortConfig.txt")
