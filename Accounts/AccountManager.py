from Accounts import Account


class AccountManager:
    def __init__(self):
        # also possible with user_id -> acc_id, acc_id -> acc, acc_id -> owner
        self._accounts: dict[(int, int): float] = {}

    def fetch(self, user_id_1: int, user_id_2: int) -> Account:
        if (user_id_1, user_id_2) in self._accounts:
            return self._accounts[(user_id_1, user_id_2)]
        if (user_id_2, user_id_1) in self._accounts:
            return self._accounts[(user_id_2, user_id_1)]

        return None

    async def create(self, user_id_1: int, user_id_2: int) -> Account:
        acc = Account(user_id_1, user_id_2)
        self._accounts[(user_id_1, user_id_2)] = acc
        return acc
