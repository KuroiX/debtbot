from Accounts import Account, AccountManager

from .sqlite_requests import acc_in_database, create_acc

class LocalAccountManager(AccountManager):
    def __init__(self):
        super().__init__()

    def fetch(self, user_id_1: int, user_id_2: int) -> Account:
        if (user_id_1, user_id_2) in self._accounts:
            return self._accounts[(user_id_1, user_id_2)]
        if (user_id_2, user_id_1) in self._accounts:
            return self._accounts[(user_id_2, user_id_1)]

        first, second = acc_in_database(user_id_1, user_id_2)

        if first:
            acc = Account(user_id_1, user_id_2)
            self._accounts[(user_id_1, user_id_2)] = acc
            return acc
        if second:
            acc = Account(user_id_2, user_id_1)
            self._accounts[(user_id_2, user_id_1)] = acc
            return acc

        return None

    def create(self, user_id_1: int, user_id_2: int) -> Account:
        create_acc(user_id_1, user_id_2)

        acc = Account(user_id_1, user_id_2)
        self._accounts[(user_id_1, user_id_2)] = acc
        return acc
