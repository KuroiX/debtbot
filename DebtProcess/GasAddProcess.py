import discord

from DebtProcess import Process


class GasAddProcess(Process):
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int):
        # needs to be called first to initialize other instance variables ???
        super().__init__(user1, user2, reaction_message_id)

        self._handles: list[callable] = [self.__handle_distance, self.__handle_gas_spent, self.__handle_price_per_y]

        self._question_for: dict[callable, callable] = {self.__handle_distance: self.__ask_for_distance,
                                                        self.__handle_gas_spent: self.__ask_for_gas_spent,
                                                        self.__handle_price_per_y: self.__ask_for_price_per_y}

        self._distance = 0
        self._gas_per_distance = 0
        self._price_per_y = 0

    def retrieve_information(self):
        result = self._distance * (self._gas_per_distance / 100) * self._price_per_y
        return result, f"{self._distance}km * ({self._gas_per_distance}l / 100km) * {self._price_per_y}€/l= {result}€"

    async def __ask_for_distance(self):
        await self.user1.send("Enter the distance traveled in km.")

    async def __handle_distance(self, message: discord.Message):
        self._distance = float(message.content)
        return

    async def __ask_for_gas_spent(self):
        await self.user1.send("Enter the gas spent per 100km.")

    async def __handle_gas_spent(self, message: discord.Message):
        self._gas_per_distance = float(message.content)
        return

    async def __ask_for_price_per_y(self):
        await self.user1.send("Enter the price per l gas.")

    async def __handle_price_per_y(self, message: discord.Message):
        self._price_per_y = float(message.content)
        return
