class Account:
    # def __init__(self, user_id_1: int, user_id_2: int):
    #    self.user_id_1 = user_id_1
    #    self.user_id_2 = user_id_2
    #    self.balance = 0.00

    @staticmethod
    def fetch(user_id_1: int, user_id_2: int):
        # TODO: implement
        # also might change to exception instead of return None
        # return None
        return Account.create(user_id_1, user_id_2)

    @classmethod
    async def create(cls, user_id_1: int, user_id_2: int):
        # TODO: understand why this works???
        self = Account()
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        self.balance = 0.00
        return self

