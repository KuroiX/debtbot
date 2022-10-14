import inspect
import discord

import DebtProcess
import UnicodeReactions as React


class AddProcess(DebtProcess.Process):
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int):
        super().__init__(user1, user2, reaction_message_id)

        self.__amount = 0.00
        self.__payer = None
        self.__comment = None

        self.__sub_process = None

        self.__state = 0
        self.__handles: list[callable] = [self.__handle_type, self.__handle_amount, self.__handle_payer,
                                          self.__handle_comment, self.__handle_confirmation1,
                                          self.__handle_confirmation2]

        # self.__handles: list[callable] = [self.__handle_type]

        # technically doable with name search too
        # but then the methods need to fit to the naming scheme
        # TODO: maybe look into decorators??
        self.__question_for: dict[callable, callable] = {self.__handle_type: self.__ask_for_type,
                                                         self.__handle_payer: self.__ask_for_payer,
                                                         self.__handle_amount: self.__ask_for_amount,
                                                         self.__handle_comment: self.__ask_for_comment,
                                                         self.__handle_confirmation1: self.__ask_for_confirmation1,
                                                         self.__handle_confirmation2: self.__ask_for_confirmation2}

    # region probably into abstract parent class

    async def start(self):
        await self.__ask_next_question()

    async def process(self, args) -> bool:
        if self.__sub_process is not None:
            return await self.__do_sub_process(args)
        else:
            return await self.__do_current_process(args)

    async def __do_sub_process(self, args) -> bool:
        sub_result = self.__sub_process.process(args)

        if sub_result:
            self.__sub_process = None

        return sub_result & (self.__state >= len(self.__handles))

    async def __do_current_process(self, args) -> bool:
        func = self.__handles[self.__state]

        if isinstance(args, discord.RawReactionActionEvent):
            if args.message_id != self._reaction_message_id:
                return False
            # not sure if this is bad code or not, but it's cool
            # also it is actually pretty nice because that way one only has to make sure
            # that the signature name is correct
            # and can change the order in the init only
            # furthermore potential to move it to the parent class, because that should be the same
            # in every process.
            # but then it might get confusing? who knows
            # another option is to have two more lists that do the same or another dict
            # (probably dict is best)
            # with a dict, process_reaction and process_messages can be fused probably
            if "payload" not in inspect.signature(func).parameters:
                print("Not a payload func")
                return False
        elif isinstance(args, discord.Message):
            if "message" not in inspect.signature(func).parameters:
                print("Not a message func")
                return False

        await func(args)

        self.__state += 1
        result = self.__state >= len(self.__handles)

        if not result:
            await self.__ask_next_question()

        return result & (self.__sub_process is None)

    # endregion

    # region questions

    async def __ask_for_type(self):
        msg = await self.user1.send("What do you want to add?\n"
                                    f"```{React.A}: Single Item\n"
                                    f"{React.B}: Multi Item\n"
                                    f"{React.C}: Gas```")

        await msg.add_reaction(React.A)
        await msg.add_reaction(React.B)
        await msg.add_reaction(React.C)

        self._reaction_message_id = msg.id

    async def __ask_for_amount(self):
        await self.user1.send("How much did it cost? (Format: x.yz)")

    async def __ask_for_payer(self):
        msg = await self.user1.send(f"Who paid? A: {self.user1.name} or B: {self.user2.name}?")

        await msg.add_reaction(React.A)
        await msg.add_reaction(React.B)

        self._reaction_message_id = msg.id

    async def __ask_for_confirmation1(self):
        msg = await self.user1.send(f"Summary:"
                                    f"{self.__debt_request_summary()}"
                                    f"Is that right?")

        await msg.add_reaction(React.YES)
        await msg.add_reaction(React.NO)

        self._reaction_message_id = msg.id

    async def __ask_for_confirmation2(self):
        msg = await self.user2.send(f"{self.user1.name} requested an new debt:"
                                    f"{self.__debt_request_summary()}"
                                    f"Do you accept?")

        await msg.add_reaction(React.YES)
        await msg.add_reaction(React.NO)

        self._reaction_message_id = msg.id

    async def __ask_for_comment(self):
        await self.user1.send("What was it about? Leave a comment for the other person.")

    # endregion

    # region handles

    async def __handle_type(self, payload: discord.RawReactionActionEvent):
        # todo handle type, currently all types do the same

        return

    async def __handle_payer(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == "\N{Regional Indicator Symbol Letter A}":
            self.__payer = True

        if payload.emoji.name == "\N{Regional Indicator Symbol Letter B}":
            self.__payer = False

        return

    async def __handle_confirmation1(self, payload: discord.RawReactionActionEvent):
        # if confirmed
        return

    async def __handle_confirmation2(self, payload: discord.RawReactionActionEvent):

        await self.user1.send(f"Request accepted, new balance is: {self.__amount}")

        return

    async def __handle_amount(self, message: discord.Message):
        amount = float(message.content)
        self.__amount = amount
        return

    async def __handle_comment(self, message: discord.Message):
        self.__comment = message.content
        return

    # endregion

    # region other & todo

    def __debt_request_summary(self) -> str:
        return (f"```"
                f"Amount:      {self.__amount}€\n"
                f"By:          {self.user1.name}\n"
                f"Your share:  50%.\n"
                f"Comment:     {self.__comment}"
                f"```")

    async def __ask_next_question(self):
        next_handle = self.__handles[self.__state]
        ask = self.__question_for[next_handle]
        await ask()

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
