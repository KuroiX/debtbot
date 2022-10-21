from Accounts import Account, AccountManager
from replit import db


class ReplAccountManager(AccountManager):

    def fetch(self, user_id_1: int, user_id_2: int) -> Account:
        if (user_id_1, user_id_2) in self._accounts:
            return self._accounts[(user_id_1, user_id_2)]
        if (user_id_2, user_id_1) in self._accounts:
            return self._accounts[(user_id_2, user_id_1)]
        if (user_id_1, user_id_2) in db.keys():
            acc = Account(user_id_1, user_id_2)
            self._accounts[(user_id_1, user_id_2)] = acc
            return acc
        if (user_id_2, user_id_1) in db.keys():
            acc = Account(user_id_2, user_id_1)
            self._accounts[(user_id_2, user_id_1)] = acc
            return acc

        return None

    async def create(self, user_id_1: int, user_id_2: int) -> Account:
        db[(user_id_1, user_id_2)] = 0.0

        acc = Account(user_id_1, user_id_2)
        self._accounts[(user_id_1, user_id_2)] = acc
        return acc
