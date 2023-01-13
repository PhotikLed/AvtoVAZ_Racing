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


def has_bought(name):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT has_bought FROM buy WHERE car_id IN (SELECT id FROM cars WHERE car == ?)'
    bought = cur.execute(sql, (name,)).fetchone()
    con.close()
    print(bought[0])
    return bought[0]


def get_cost(name):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT price FROM buy WHERE car_id IN (SELECT id FROM cars WHERE car == ?)'
    price = cur.execute(sql, (name,)).fetchone()
    con.close()

    return price[0]


def set_bought(name):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = '''UPDATE buy
            SET has_bought = 1
            WHERE car_id IN (SELECT id FROM cars WHERE car == ?)'''
    cur.execute(sql, (name,))
    con.commit()
    con.close()


def get_tun_price(tun):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT price FROM tuning_price WHERE name = ?'
    price = cur.execute(sql, (tun,)).fetchone()
    con.close()

    return price[0]


def get_max_and_cur_count_of_upgrades(tun):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT cur_upgrades, max_upgrades FROM tuning_price WHERE name = ?'
    cur_count, max_count = cur.execute(sql, (tun,)).fetchone()
    con.close()

    return cur_count, max_count


def get_size_upgrade(tun):
    con = sqlite3.connect('sysparams/tuning.db')
    cur = con.cursor()
    sql = 'SELECT size_upgrades FROM tuning_price WHERE name = ?'
    size = cur.execute(sql, (tun,)).fetchone()
    con.close()

    return size[0]


def set_upgrade(tun):
    cur_count, max_count = get_max_and_cur_count_of_upgrades(tun)
    if cur_count < max_count:
        con = sqlite3.connect('sysparams/tuning.db')
        cur = con.cursor()
        sql = '''UPDATE tuning_price
                SET has_bought = 1
                WHERE car_id IN (SELECT id FROM cars WHERE car == ?)'''
        cur.execute(sql, (tun,))
        con.commit()
        con.close()
