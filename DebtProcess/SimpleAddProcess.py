import discord

from DebtProcess import Process


class SimpleAddProcess(Process):
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int, is_multi_item: bool):
        # needs to be called first to initialize other instance variables ???
        super().__init__(user1, user2, reaction_message_id)
        self.__is_multi_item = is_multi_item

        self._handles: list[callable] = [self.__handle_amount]

        self._question_for: dict[callable, callable] = {self.__handle_amount: self.__ask_for_amount}

        self._amount = []

    def retrieve_information(self):
        result = []
        for i, item in enumerate(self._amount):
            if i == len(self._amount) - 1:
                result.append(f"{item}€")
            else:
                result.append(f"{item}€ + ")

        result_sum = sum(self._amount)

        if self.__is_multi_item:
            result.append(f" = {result_sum}€")

        final = "".join(result)
        return result_sum, final

    async def __ask_for_amount(self):
        await self.user1.send("Enter the price of the next item. Finish entering items by entering 0. (Format: x.yz)")

    async def __handle_amount(self, message: discord.Message):
        amount = float(message.content)

        if amount == 0 & self.__is_multi_item:
            return

        self._amount.append(amount)

        if self.__is_multi_item:
            self._state -= 1

        return
