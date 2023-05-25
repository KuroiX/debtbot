import sqlite3 as sl

from .sqlite_requests import get_balance, update_balance


class Account:

    connection: sl.Connection

    def __init__(self, user_id_1: int, user_id_2: int):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.balance = get_balance(self.user_id_1, self.user_id_2)

    def update(self, amount: float):
        self.balance += amount
        update_balance(self.user_id_1, self.user_id_2, self.balance)

    def is_owner(self, user_id: int):
        return user_id == self.user_id_1
