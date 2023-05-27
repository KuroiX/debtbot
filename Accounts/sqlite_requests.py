import sqlite3 as sl

from .sqlite_statements import *


def create_acc(id_1: int, id_2: int):
    with sl.connect("accounts.db") as con:
        con.execute(sql_create(id_1, id_2, 0.00))


def acc_in_database(id_1: int, id_2: int):
    with sl.connect("accounts.db") as con:
        data_1: sl.Cursor = con.execute(sql_find(id_1, id_2))
        data_2: sl.Cursor = con.execute(sql_find(id_2, id_1))
        first, second = False, False
        for row in data_1:
            first = True
            break
        for row in data_2:
            second = True
            break
        return first, second


def find_all_accs(id_1: int):
    with sl.connect("accounts.db") as con:
        data_1: sl.Cursor = con.execute(sql_find_all(id_1))
        result = []
        for row in data_1:
            result.append(row)
        return result


def get_balance(id_1, id_2):
    # this only works if the account already exists, which it does
    with sl.connect("accounts.db") as con:
        data = con.execute(sql_find(id_1, id_2))
        return [row[2] for row in data][0]


def update_balance(id_1, id_2, balance):
    with sl.connect("accounts.db") as con:
        con.execute(sql_update(id_1, id_2, balance))
