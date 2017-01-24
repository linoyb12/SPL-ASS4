import sqlite3
import os.path
import hotelWorker
import time

_conn = 0
is_first_iter = True

task_last_time_exec={
}


def connect():
    global _conn
    _conn = sqlite3.connect('cronhoteldb.db')


def has_more_tasks():
    #_conn1 = sqlite3.connect('cronhoteldb.db')
    query_data = _conn.cursor()

    query_data.execute("""
        SELECT * FROM TaskTimes WHERE NumTimes>0""")

    query_data = query_data.fetchall()

    if len(query_data) > 0:
        return True

    return False


def decrease_task_times(task_id):
    _cur = _conn.cursor()
    _cur.execute("""
        UPDATE TaskTimes SET NumTimes=NumTimes-1 WHERE TaskId =(?)
    """, [task_id])
    _conn.commit()


def init():
    cur = _conn.cursor()
    cur.execute("""
                 SELECT * FROM Tasks
               """)
    tmp_cur = list(cur)
    for line in tmp_cur:
        task_last_time_exec[line[0]] = hotelWorker.dohoteltask(line[1], line[2])
        decrease_task_times(line[0])


def execute_tasks():
    cur = _conn.cursor()
    cur.execute("""SELECT Tasks.TaskId, TaskName, Parameter, DoEvery
        FROM Tasks JOIN TaskTimes ON Tasks.TaskId=TaskTimes.TaskId WHERE TaskTimes.NumTimes>0""")
    for line in cur:
        temp_time = task_last_time_exec[line[0]] + line[3]
        if temp_time < time.time():
            task_last_time_exec[line[0]] = hotelWorker.dohoteltask(line[1], line[2])
            decrease_task_times(line[0])


def main():
    while os.path.isfile('cronhoteldb.db') :
        connect()
        global is_first_iter
        if has_more_tasks():
            if is_first_iter:
                init()
                is_first_iter = False
            else:
                execute_tasks()
        else:
            break

if __name__ == '__main__':
    main()