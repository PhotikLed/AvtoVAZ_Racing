import sqlite3


def get_tuning():
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT * FROM params'
    tunings = cur.execute(sql).fetchall()
    con.close()

    return tunings


def get_tuning_by_name(name):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT * FROM params WHERE car_id IN (SELECT id FROM cars WHERE car == ?)'
    params = cur.execute(sql, (name,)).fetchone()
    con.close()

    return params
