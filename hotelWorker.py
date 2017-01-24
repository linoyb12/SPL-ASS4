import sqlite3
import time

_conn = sqlite3.connect('cronhoteldb.db')

def dohoteltask(task_name, parameter):
    if task_name == 'clean':
        return clean()

    return wakeup_n_brakefast(task_name, parameter)


def clean():
    c = _conn.cursor()
    c.execute("""SELECT Rooms.RoomNumber FROM Rooms LEFT JOIN Residents
            ON Residents.RoomNumber = Rooms.RoomNumber WHERE FirstName IS NULL
            ORDER BY Residents.RoomNumber ASC""")

    time_now=time.time()
    rooms = ""
    for row in c.fetchall():
        rooms += "{},".format(*row)
    rooms = rooms[:-1]

    print 'Rooms {} were cleaned at {}'.format(rooms, time_now)
    return time_now


def wakeup_n_brakefast(task_name, parameter):
    c = _conn.cursor()
    c.execute("""
            SELECT FirstName, LastName FROM Residents WHERE RoomNumber = (?)
        """, [parameter])
    res = c.fetchone()
    time_now = time.time()
    if task_name == 'wakeup':
        print '{} {} in room {} received a wakeup call at {}'.format(res[0], res[1], parameter, time_now)
    else:
        print '{} {} in room {} has been served breakfast at {}'.format(res[0], res[1], parameter, time_now)

    return time_now

