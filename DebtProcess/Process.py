import inspect
from abc import ABC, abstractmethod

import discord


class Process(ABC):

    def __init__(self, requester: discord.User, recipient: discord.User):
        self.requester = requester
        self.recipient = recipient
        self._reaction_message_id = -1

        self._state = 0
        # todo figure out cleaner way (???)
        self._handles: list[callable] = []
        self._question_for: dict[callable, callable] = {}

        self._sub_process = None
        self._sub_process_info = []

        self._active_reactions = []

    @abstractmethod
    def retrieve_information(self):
        pass

    async def start(self):
        await self.__ask_next_question()

    async def process(self, args) -> bool:
        if self._sub_process is not None:
            return await self.__do_sub_process(args)
        else:
            return await self.__do_current_process(args)

    async def _add_reaction(self, msg: discord.Message, reaction: str):
        await msg.add_reaction(reaction)
        self._active_reactions.append(reaction)

    def __clear_reactions(self):
        self._active_reactions.clear()

    async def __ask_next_question(self):
        if self._sub_process is not None:
            await self._sub_process.start()

        else:
            next_handle = self._handles[self._state]
            ask = self._question_for[next_handle]
            await ask()

    async def __do_sub_process(self, args) -> bool:
        sub_result = await self._sub_process.process(args)

        if sub_result:
            self._sub_process_info.append(self._sub_process.retrieve_information())
            self._sub_process = None

        result = self._state >= len(self._handles)

        if (not result) & sub_result:
            await self.__ask_next_question()

        return sub_result & result

    async def __do_current_process(self, args) -> bool:
        func = self._handles[self._state]

        if isinstance(args, discord.RawReactionActionEvent):
            if args.message_id != self._reaction_message_id:
                return False

            reaction = args.emoji.name
            if reaction not in self._active_reactions:
                return False
            # TODO: test against currently active reactions and if accepted, flush
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

        self.__clear_reactions()
        await func(args)

        self._state += 1
        result = self._state >= len(self._handles)

        if not result:
            await self.__ask_next_question()

        return result & (self._sub_process is None)
