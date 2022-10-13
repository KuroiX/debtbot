import DebtProcess
import discord


class RegistrationProcess(DebtProcess.Process):
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int):
        super().__init__(user1, user2, reaction_message_id)

        self.__accept_emoji = '\N{WHITE HEAVY CHECK MARK}'
        self.__reject_emoji = '\N{CROSS MARK}'

    async def process_reaction(self, payload: discord.RawReactionActionEvent) -> bool:
        if payload.message_id != self._reaction_message_id:
            return False

        if payload.emoji.name == self.__accept_emoji:
            await self.__invite_accepted()
            return True

        if payload.emoji.name == self.__reject_emoji:
            await self.__invite_rejected()
            return True

        return False

    async def __invite_accepted(self):
        balance = 0.00
        await self.user1.send(f"Successfully created an account with {self.user2}.\nCurrent balance is: {balance}€.")
        await self.user2.send(f"Successfully created an account with {self.user1}.\nCurrent balance is: {balance}€.")

    async def __invite_rejected(self):
        await self.user1.send(f"Seems like {self.user2} doesn't want to open an account with you :(")
        await self.user2.send(f"You rejected {self.user1}'s invite.")
