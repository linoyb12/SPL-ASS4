import sqlite3
import os.path
import hotelWorker
import time


_conn = sqlite3.connect('cronhoteldb.db')
count_iter=1

task_last_time_exec={
}

def has_more_tasks():
    query_data = _conn.cursor()

    query_data.execute("""
        SELECT *
        FROM TaskTimes
        WHERE NumTimes>0
    """)

    if query_data.rowcount > 0:
        return True

    return False


def decrease_task_times(task_id):
    _conn.execute("""
        UPDATE TaskTimes SET NumTimes=NumTimes-1 WHERE TaskId =(?,)
    """,[task_id, ])


def init():
    cur = _conn.cursor()
    cur.execute("""
                 SELECT * FROM Tasks
               """)
    for line in cur:
        task_last_time_exec[line[0]]=hotelWorker.dohoteltask(line[1],line[2])
        decrease_task_times(line[0])


def execute_tasks():
    cur = _conn.cursor()
    cur.execute("""
        SELECT TaskId, TaskName, Parameter, DoEvery
        FROM Tasks JOIN TaskTimes ON Tasks.TaskId=TaskTimes.TaskId WHERE TaskTimes.NumTimes>0""")
    for line in cur:
        temp_time = task_last_time_exec[line[0]].add(cur[3])
        if temp_time > time.clock():
            task_last_time_exec[line[0]] = hotelWorker.dohoteltask(line[1], line[2])
            decrease_task_times(line[0])


def main():
    while os.path.isfile('cronhoteldb.db') and has_more_tasks():
        if count_iter == 1:
            init()
        else:
            execute_tasks()
