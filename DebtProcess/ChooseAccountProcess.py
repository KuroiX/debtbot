import discord

from DebtProcess import Process
import UnicodeReactions as React


class ChooseAccountProcess(Process):
    def __init__(self, requester: discord.User, recipient: discord.User, recipients: list[discord.User], bot):
        super().__init__(requester, recipient)

        self.__recipients = recipients
        self._bot = bot
        self.user: discord.User

        self.reactions = [React.A, React.B, React.C, React.D, React.E, React.F, React.G, React.H, React.I, React.J]
        self.reactions_dict: [str, discord.User] = {}

        self._handles: list[callable] = [self.__handle_choosing_acc, ]

        self._question_for: dict[callable, callable] = {self.__handle_choosing_acc: self.__ask_for_choosing_acc}

    def next_steps(self):
        return 0, (self.requester, self.user)

    def retrieve_information(self):
        pass

    async def __handle_choosing_acc(self, payload: discord.RawReactionActionEvent):
        user = self.reactions_dict[payload.emoji.name]
        self.user = user

    async def __ask_for_choosing_acc(self):
        output = "On which account to you want to add something? ```"
        i = 0
        extra = "```"

        for user in self.__recipients:
            output += f"\n{self.reactions[i]}: {user.name}"
            self.reactions_dict[self.reactions[i]] = user
            i = i + 1
            if i >= 10:
                extra += "Some names could not be added... (max 10)"
                break
#            output += "\n"

        output += extra

        msg = await self.requester.send(output)

        i = 0
        for user in self.__recipients:
            await self._add_reaction(msg, self.reactions[i])
            i = i + 1
            if i >= 10:
                break

        self._reaction_message_id = msg.id
