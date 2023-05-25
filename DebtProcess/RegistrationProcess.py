import discord

import DebtProcess
import UnicodeReactions as React
import Accounts


class RegistrationProcess(DebtProcess.Process):
    def __init__(self, requester: discord.User, recipient: discord.User, account_manager: Accounts.AccountManager):
        super().__init__(requester, recipient)

        self.__account_manager = account_manager
        self._handles = [self.__handle_confirmation]
        self._question_for = {self.__handle_confirmation: self.__ask_for_confirmation}

    def retrieve_information(self):
        pass

    async def __ask_for_confirmation(self):
        msg = await self.recipient.send(f"{self.requester} wants to create an account with you, {self.recipient}. "
                                        f"Do you agree?")
        await self._add_reaction(msg, React.YES)
        await self._add_reaction(msg, React.NO)
        self._reaction_message_id = msg.id

    async def __handle_confirmation(self, payload: discord.RawReactionActionEvent):
        reaction = payload.emoji.name

        if reaction == React.YES:
            await self.__invite_accepted()
        elif reaction == React.NO:
            await self.__invite_rejected()
        else:
            print("Reaction not registered")

    async def __invite_accepted(self):
        # todo create account outside of this class?
        # but where...
        # it it was in CommandBot, the command bot would need the result of the process as well
        # seems kinda unnecessary
        # especially because not all processes need an account manager and a callback like thing
        self.__account_manager.create(self.requester.id, self.recipient.id)

        balance = 0.00
        await self.requester.send(f"Successfully created an account with {self.recipient}.\n"
                                  f"Current balance is: {balance}€.")
        await self.recipient.send(f"Successfully created an account with {self.requester}.\n"
                                  f"Current balance is: {balance}€.")

    async def __invite_rejected(self):
        await self.requester.send(f"Seems like {self.recipient} doesn't want to open an account with you :(")
        await self.recipient.send(f"You rejected {self.requester}'s invite.")
