import discord

import DebtProcess
import UnicodeReactions as React


class AddProcess(DebtProcess.Process):
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int):
        # needs to be called first to initialize other instance variables ???
        super().__init__(user1, user2, reaction_message_id)

        self.__amount = 0.00
        self.__user1_share = 0.00
        self.__payer = None
        self.__comment = None

        # self.__sub_process = None

        self._handles: list[callable] = [self.__handle_type, self.__handle_payer, self.__handle_share,
                                         self.__handle_comment, self.__handle_confirmation1,
                                         self.__handle_confirmation2]

        # self.__handles: list[callable] = [self.__handle_type]

        # technically doable with name search too
        # but then the methods need to fit to the naming scheme
        # TODO: maybe look into decorators??
        self._question_for: dict[callable, callable] = {self.__handle_type: self.__ask_for_type,
                                                        self.__handle_payer: self.__ask_for_payer,
                                                        self.__handle_comment: self.__ask_for_comment,
                                                        self.__handle_confirmation1: self.__ask_for_confirmation1,
                                                        self.__handle_confirmation2: self.__ask_for_confirmation2,
                                                        self.__handle_share: self.__ask_for_share}

    def retrieve_information(self):
        # todo
        pass

    async def __ask_for_type(self):

        msg = await self.user1.send("What do you want to add?\n"
                                    f"```{React.A}: Single Item\n"
                                    f"{React.B}: Multi Item\n"
                                    f"{React.C}: Gas```")

        await msg.add_reaction(React.A)
        await msg.add_reaction(React.B)
        await msg.add_reaction(React.C)

        self._reaction_message_id = msg.id

    async def __handle_type(self, payload: discord.RawReactionActionEvent):
        reaction = payload.emoji.name

        # todo no case statement
        if reaction == React.A:
            self._sub_process = DebtProcess.SimpleAddProcess(self.user1, self.user2, -1, False)
        elif reaction == React.B:
            self._sub_process = DebtProcess.SimpleAddProcess(self.user1, self.user2, -1, True)
        else:
            await self.user1.send("Function does not exist yet!")
            self._state -= 1

        return

    async def __ask_for_payer(self):
        msg = await self.user1.send(f"Who paid?"
                                    f"```A: {self.user1.name}\n"
                                    f"B: {self.user2.name}```")

        await msg.add_reaction(React.A)
        await msg.add_reaction(React.B)

        self._reaction_message_id = msg.id

    async def __handle_payer(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == React.A:
            self.__payer = True

        if payload.emoji.name == React.B:
            self.__payer = False

        return

    async def __ask_for_share(self):
        await self.user1.send("What was your share in [0, 1]?")

    async def __handle_share(self, message: discord.Message):
        share = float(message.content)
        self.__user1_share = share

    async def __ask_for_comment(self):
        await self.user1.send("What was it about? Leave a comment for the other person.")

    async def __handle_comment(self, message: discord.Message):
        self.__comment = message.content
        return

    async def __ask_for_confirmation1(self):
        msg = await self.user1.send(f"Summary:"
                                    f"{self.__debt_request_summary(True)}"
                                    f"Is that right?")

        await msg.add_reaction(React.YES)
        await msg.add_reaction(React.NO)

        self._reaction_message_id = msg.id

    async def __handle_confirmation1(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == React.YES:
            return

        if payload.emoji.name == React.NO:
            await self.user1.send("Ok, let's try again!")
            self._state = -1
            return

    async def __ask_for_confirmation2(self):
        msg = await self.user2.send(f"{self.user1.name} requested an new debt:"
                                    f"{self.__debt_request_summary(False)}"
                                    f"Do you accept?")

        await msg.add_reaction(React.YES)
        await msg.add_reaction(React.NO)

        self._reaction_message_id = msg.id

    async def __handle_confirmation2(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == React.YES:
            await self.user1.send(f"Request accepted, new balance is: coming soon")
            await self.user2.send(f"Request accepted, new balance is: coming soon")
            return

        if payload.emoji.name == React.NO:
            await self.user1.send(f"Seems like your request was denied.")
            # todo maybe ask user2 why?
            # in subprocess :D
            await self.user2.send(f"You denied {self.user1}'s request.")
            return

    # region other & todo

    def __debt_request_summary(self, is_user_1) -> str:

        share = self.__user1_share if is_user_1 else 1 - self.__user1_share
        share *= 100

        return (f"```"
                f"Amount:      {self._sub_process_info[0][1]}\n"
                f"By:          {self.user1.name}\n"
                f"Your share:  {share}%.\n"
                f"Comment:     {self.__comment}\n"
                f"--------------------------------------------------------------\n"
                f"Account:     before - (sum) * share"
                f"```")

    async def __addition_accepted(self):
        # todo

        balance = 0.00
        await self.user1.send(f"Successfully created an account with {self.user2}.\nCurrent balance is: {balance}€.")
        await self.user2.send(f"Successfully created an account with {self.user1}.\nCurrent balance is: {balance}€.")

    async def __addition_rejected(self):
        # todo
        await self.user1.send(f"Seems like {self.user2} doesn't want to open an account with you :(")
        await self.user2.send(f"You rejected {self.user1}'s invite.")

    # endregion
