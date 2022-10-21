from replit import db

class Account:
    def __init__(self, user_id_1: int, user_id_2: int):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.balance = 0.00

    def update(self, amount: float):
        self.balance += amount
        db[(self.user_id_1, self.user_id_2)] = self.balance

    def is_owner(self, user_id: int):
        return user_id == self.user_id_1
