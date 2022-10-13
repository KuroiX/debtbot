import DebtProcess
import discord


class AddProcess(DebtProcess.Process):
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int):
        super().__init__(user1, user2, reaction_message_id)

        self.__accept_emoji = '\N{WHITE HEAVY CHECK MARK}'
        self.__reject_emoji = '\N{CROSS MARK}'

        self.__state = 0
        self.__amount = 0.00
        self.__payer = None
        self.__comment = None

        self.__reactions: dict[int, callable] = {0: self.__handle_type, 2: self.__handle_payer,
                                                 4: self.__handle_confirmation1, 5: self.__handle_confirmation2}
        self.__messages: dict[int, callable] = {1: self.__handle_amount, 3: self.__handle_comment}

    async def process_reaction(self, payload: discord.RawReactionActionEvent) -> bool:
        if payload.message_id != self._reaction_message_id:
            return False

        if self.__state not in self.__reactions:
            return True

        return await self.__reactions[self.__state](payload)

    async def process_message(self, message: discord.Message) -> bool:
        if self.__state not in self.__messages:
            return False

        return await self.__messages[self.__state](message)

    async def __handle_type(self, payload: discord.RawReactionActionEvent) -> bool:
        # todo handle type, currently all types do the same

        await self.user1.send("How much did it cost? (Format: x.yz)")
        self._reaction_message_id = -1
        self.__state = 1
        return False

    async def __handle_payer(self, payload: discord.RawReactionActionEvent) -> bool:
        if payload.emoji.name == "\N{Regional Indicator Symbol Letter A}":
            self.__payer = True

        if payload.emoji.name == "\N{Regional Indicator Symbol Letter B}":
            self.__payer = False

        await self.user1.send("What was it about? Leave a comment for the other person.")
        self._reaction_message_id = -1
        self.__state = 3
        return False

    async def __handle_confirmation1(self, payload: discord.RawReactionActionEvent) -> bool:
        # if confirmed

        msg = await self.user2.send(f"{self.user1.name} requested an new debt:"
                                    f"{self.debt_request_summary()}"
                                    f"Do you accept?")

        await msg.add_reaction(self.__accept_emoji)
        await msg.add_reaction(self.__reject_emoji)

        self._reaction_message_id = msg.id
        self.__state = 5
        return False

    async def __handle_confirmation2(self, payload: discord.RawReactionActionEvent) -> bool:
        # if confirmed

        await self.user1.send(f"Request accepted, new balance is: {self.__amount}")

        return True

    async def __handle_amount(self, message: discord.Message) -> bool:
        amount = float(message.content)
        self.__amount = amount

        msg = await self.user1.send(f"Who paid? A: {self.user1.name} or B: {self.user2.name}?")

        await msg.add_reaction("\N{Regional Indicator Symbol Letter A}")
        await msg.add_reaction("\N{Regional Indicator Symbol Letter B}")

        self._reaction_message_id = msg.id
        self.__state = 2
        return False

    async def __handle_comment(self, message: discord.Message) -> bool:
        self.__comment = message.content

        msg = await self.user1.send(f"Summary:"
                                    f"{self.debt_request_summary()}"
                                    f"Is that right?")

        await msg.add_reaction(self.__accept_emoji)
        await msg.add_reaction(self.__reject_emoji)

        self._reaction_message_id = msg.id
        self.__state = 4
        return False

    def debt_request_summary(self) -> str:
        return (f"```"
                f"Amount:      {self.__amount}€\n"
                f"By:          {self.user1.name}\n"
                f"Your share:  50%.\n"
                f"Comment:     {self.__comment}"
                f"```")

    async def __addition_accepted(self):
        balance = 0.00
        await self.user1.send(f"Successfully created an account with {self.user2}.\nCurrent balance is: {balance}€.")
        await self.user2.send(f"Successfully created an account with {self.user1}.\nCurrent balance is: {balance}€.")

    async def __addition_rejected(self):
        await self.user1.send(f"Seems like {self.user2} doesn't want to open an account with you :(")
        await self.user2.send(f"You rejected {self.user1}'s invite.")
