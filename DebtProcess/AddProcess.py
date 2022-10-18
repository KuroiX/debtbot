import discord

import DebtProcess
import Accounts
import UnicodeReactions as React


class AddProcess(DebtProcess.Process):
    def __init__(self, requester: discord.User, recipient: discord.User, account: Accounts.Account):
        # needs to be called first to initialize other instance variables ???
        super().__init__(requester, recipient)

        self.__amount = 0.00
        self.__requester_share = 0.00
        self.__requester_is_payer = None
        self.__comment = None
        self.__account = account

        self._handles: list[callable] = [self.__handle_type, self.__handle_payer, self.__handle_share,
                                         self.__handle_comment, self.__handle_confirmation1,
                                         self.__handle_confirmation2]

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

        msg = await self.requester.send("What do you want to add?\n"
                                        f"```{React.A}: Single Item\n"
                                        f"{React.B}: Multi Item\n"
                                        f"{React.C}: Gas```")

        await self._add_reaction(msg, React.A)
        await self._add_reaction(msg, React.B)
        await self._add_reaction(msg, React.C)

        self._reaction_message_id = msg.id

    async def __handle_type(self, payload: discord.RawReactionActionEvent):
        reaction = payload.emoji.name

        # todo no case statement
        # let it extend dynamically like a language package
        if reaction == React.A:
            self._sub_process = DebtProcess.SimpleAddProcess(self.requester, self.recipient, False)
        elif reaction == React.B:
            self._sub_process = DebtProcess.SimpleAddProcess(self.requester, self.recipient, True)
        else:
            self._sub_process = DebtProcess.GasAddProcess(self.requester, self.recipient)

        return

    async def __ask_for_payer(self):
        msg = await self.requester.send(f"Who paid?"
                                        f"```A: {self.requester.name}\n"
                                        f"B: {self.recipient.name}```")

        await self._add_reaction(msg, React.A)
        await self._add_reaction(msg, React.B)

        self._reaction_message_id = msg.id

    async def __handle_payer(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == React.A:
            self.__requester_is_payer = True

        if payload.emoji.name == React.B:
            self.__requester_is_payer = False

        return

    async def __ask_for_share(self):
        await self.requester.send("What was your share in [0, 1]?")

    async def __handle_share(self, message: discord.Message):
        share = float(message.content)
        self.__requester_share = share

    async def __ask_for_comment(self):
        await self.requester.send("What was it about? Leave a comment for the other person.")

    async def __handle_comment(self, message: discord.Message):
        self.__comment = message.content
        return

    async def __ask_for_confirmation1(self):
        msg = await self.requester.send(f"Summary:"
                                        f"{self.__debt_request_summary(self.__account.is_owner(self.requester.id), True)}"
                                        f"Is that right?")

        await self._add_reaction(msg, React.YES)
        await self._add_reaction(msg, React.NO)

        self._reaction_message_id = msg.id

    async def __handle_confirmation1(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == React.YES:
            return

        if payload.emoji.name == React.NO:
            await self.requester.send("Ok, let's try again!")
            self._state = -1
            return

    async def __ask_for_confirmation2(self):
        msg = await self.recipient.send(f"{self.requester.name} requested an new debt:"
                                        f"{self.__debt_request_summary(self.__account.is_owner(self.recipient.id), False)}"
                                        f"Do you accept?")

        await self._add_reaction(msg, React.YES)
        await self._add_reaction(msg, React.NO)

        self._reaction_message_id = msg.id

    async def __handle_confirmation2(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == React.YES:
            await self.__addition_accepted()
            return
        elif payload.emoji.name == React.NO:
            await self.__addition_rejected()
            return

    # region other & todo

    def __debt_request_summary(self, is_owner, is_requester) -> str:
        requester_is_owner = self.__account.is_owner(self.requester.id)
        share_multiplier = 1 - self.__requester_share if requester_is_owner else self.__requester_share
        share = self.__requester_share if is_requester else 1 - self.__requester_share

        payer = self.requester.name if self.__requester_is_payer else self.recipient.name
        payer_multiplier = 1 if (self.__requester_is_payer & is_requester) else -1

        iff = (requester_is_owner & is_requester) | (not requester_is_owner & (not is_requester))
        user_multiplier = 1 if iff else -1
        prev = self.__account.balance * user_multiplier
        debt_sum = self.__calculate_debt() * user_multiplier
        new_result = prev + debt_sum

        return (f"```"
                f"Amount:      {self._sub_process_info[0][1]}\n"
                f"By:          {payer} (*{payer_multiplier})\n"
                f"Your share:  {share * 100}% (*{share_multiplier})\n"
                f"Comment:     {self.__comment}\n"
                f"-----------------------------------------------\n"
                f"Account:     {prev}€ {(self._sub_process_info[0][0] * share_multiplier * payer_multiplier)}€"
                f" = {new_result}€"
                f"```")

    def __calculate_debt(self):
        requester_is_owner = self.__account.is_owner(self.requester.id)
        user_multiplier = 1 if requester_is_owner else -1
        share_multiplier = 1 - self.__requester_share if requester_is_owner else self.__requester_share
        payer_multiplier = 1 if self.__requester_is_payer else -1
        debt_sum = self._sub_process_info[0][0]
        return debt_sum * share_multiplier * user_multiplier * payer_multiplier

    async def __addition_accepted(self):
        await self.requester.send(f"Request accepted, new balance is: coming soon")
        await self.recipient.send(f"Request accepted, new balance is: coming soon")

    async def __addition_rejected(self):
        await self.requester.send(f"Seems like your request was denied.")
        # todo maybe ask user2 why?
        # in subprocess :D
        await self.recipient.send(f"You denied {self.requester}'s request.")

    # endregion
