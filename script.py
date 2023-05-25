import sqlite3 as sl

import Accounts
from Accounts import LocalAccountManager
from Accounts.sqlite_requests import sql_create as boi

con = sl.connect('accounts.db')

sql_create = """
        CREATE TABLE ACCOUNTS (
            id_1 INTEGER NOT NULL,
            id_2 INTEGER NOT NULL,
            balance FLOAT DEFAULT 0.00,
            PRIMARY KEY (id_1, id_2)
        );
    """

with con:
    con.execute(sql_create)
    con.execute(boi(165917354839113737, 195942026263527425, 33.54))
    data = con.execute("SELECT * FROM ACCOUNTS")
    for row in data:
        print(row)


#with con:
#    con.execute(sql_create)

"""
sql = 'INSERT INTO ACCOUNTS (id_1, id_2, balance) values(?, ?, ?)'
data = [
    (1, 2, 0.00)
]
"""

#acc = Accounts.Account(1, 2)

#acc_manager = LocalAccountManager()
"""
print(acc_in_database(2, 1))

#acc_manager.create(4, 5)

with con:
    #con.execute(sql_create(4, 5, 0.0))
    #con.execute(sql_delete(165917354839113737, 165917354839113737))
    data1 = con.execute(sql_find(4, 2))
    print(data1.rowcount > 0)
    for row in data1:
        print("hihi")
        #print(row)
    data = con.execute("SELECT * FROM ACCOUNTS")
    for row in data:
        print(row)
"""
"""

with con:
    con.execute(sql_update)
    data = con.execute("SELECT * FROM ACCOUNTS")
    for row in data:
        print(row)


with con:
    con.executemany(sql, data)

with con:
    data = con.execute("SELECT * FROM ACCOUNTS")
    for row in data:
        print(row)
"""