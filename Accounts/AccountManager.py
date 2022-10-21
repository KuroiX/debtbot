from abc import abstractmethod, ABC

from Accounts import Account


class AccountManager(ABC):
    def __init__(self):
        # also possible with user_id -> acc_id, acc_id -> acc, acc_id -> owner
        self._accounts: dict[(int, int): float] = {}

    @abstractmethod
    def fetch(self, user_id_1: int, user_id_2: int) -> Account:
        pass

    @abstractmethod
    async def create(self, user_id_1: int, user_id_2: int) -> Account:
        pass