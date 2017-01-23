import sqlite3
import time

_conn = sqlite3.connect('cronhoteldb.db')


def dohoteltask(task_name, parameter):

    if task_name == 'clean':
        return clean()
    return wakeup_n_brakefast(task_name, parameter)


def clean(self):
    joined = """SELECT m.RoomNumber as RoomNumber, r.FirstName as FirstName
        FROM Rooms as m
        LEFT JOIN Residents as s
        ON m.RoomNumber = s.RoomNumber"""

    select = """SELECT RoomNumber
        FROM ( ? )
        WHERE FirstName IS NULL
        ORDER BY RoomNumber ASC""", [joined, ]

    c = self._conn.cursor()
    c.execute(select)

    rooms = ""
    for row in c.fetchall():
        rooms += "{}, ".format(*row)
    rooms = rooms[:-1]
    time_now = time.clock()

    print 'Rooms {} were cleaned at {}'.format(rooms, time_now)
    return time_now


def wakeup_n_brakefast(self, task_name, parameter):
    c = self._conn.cursor()
    c.execute("""
            SELECT FirstName, LastName FROM Residents WHERE RoomNumber = ?
        """, [parameter])
    res = c.fetchone()
    time_now = time.clock()
    if task_name == 'wakeup':
        print '{} {} in room {} received a wakeup call at {}'.format(res[0], res[1], parameter, time_now)
    else:
        print '{} {} in room {} has been served breakfast at {}'.format(res[0], res[1], parameter, time_now)

    return time_now

