from Accounts import Account, AccountManager


class LocalAccountManager(AccountManager):

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
