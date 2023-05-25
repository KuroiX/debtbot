def sql_create(id_1: int, id_2: int, balance: float):
    return f"INSERT INTO ACCOUNTS (id_1, id_2, balance) values ({id_1}, {id_2}, {balance})"

def sql_update(id_1: int, id_2: int, balance: float):
    return f"UPDATE ACCOUNTS SET balance = {balance} WHERE id_1 = {id_1} AND id_2 = {id_2}";

def sql_find_any(id_1: int, id_2: int):
    return f"SELECT * FROM ACCOUNTS WHERE id_1 = {id_1} AND id_2 = {id_2} OR id_2 = {id_2} AND id_1 = {id_1}"

def sql_find(id_1: int, id_2: int):
    return f"SELECT * FROM ACCOUNTS WHERE id_1 = {id_1} AND id_2 = {id_2}"

def sql_delete(id_1: int, id_2: int):
    return f"DELETE FROM ACCOUNTS WHERE id_2 = {id_1} AND id_2 = {id_2}"