import discord


class Process:
    def __init__(self, user1: discord.User, user2: discord.User, reaction_message_id: int):
        self.user1 = user1
        self.user2 = user2
        self._reaction_message_id = reaction_message_id

    # todo abstract
    def process_reaction(self, payload: discord.RawReactionActionEvent) -> bool:
        pass

    def process_message(self, message: discord.Message) -> bool:
        pass
