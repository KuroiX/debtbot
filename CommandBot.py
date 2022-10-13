import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import DebtProcess


class CommandBot(commands.Bot):

    def __init__(self):
        default_flags = discord.Intents.default()
        default_flags.message_content = True

        super().__init__(command_prefix=".", intents=default_flags)

        self.__define_commands()

        self.__running_processes: [int, DebtProcess.Process] = {}

    """
    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content[0] == ".":
            await self.process_commands(message)
            return
        # call user.state.on_message as state machine

        print(message.content)

        msg = await message.channel.send("Tag leude!")
        await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        await msg.add_reaction('\N{CROSS MARK}')

        # unsubscribe(self.bot)

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        print("reaction")
        if user == self.user:
            return

        # call user.state.on_message as state machine

        msg = await reaction.message.channel.send("Nice reaction!")
        # msg.id

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.user.id:
            return

        # payload.message_id ==
        if payload.emoji == '\N{WHITE HEAVY CHECK MARK}':
            print("yay")

        print(payload.emoji)
    """

    def __define_commands(self):
        @self.command()
        async def add_account(ctx: commands.context, user_id: int):
            sender = ctx.author
            recipient = await self.fetch_user(user_id)

            msg = await recipient.send(f"{sender} wants to create an account with you, {recipient}. Do you agree?")
            await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
            await msg.add_reaction('\N{CROSS MARK}')

            registration_process = DebtProcess.RegistrationProcess(recipient, sender, msg.id)
            self.__running_processes[recipient.id] = registration_process
            self.__running_processes[sender.id] = registration_process

        @self.command()
        async def add(ctx: commands.context, user_id: int):

            sender = ctx.author
            recipient = await self.fetch_user(user_id)

            msg = await ctx.send("What do you want to add?\n"
                                 "```\N{Regional Indicator Symbol Letter A}: Single Item\n"
                                 "\N{Regional Indicator Symbol Letter B}: Multi Item\n"
                                 "\N{Regional Indicator Symbol Letter C}: Gas```")

            await msg.add_reaction('\N{Regional Indicator Symbol Letter A}')
            await msg.add_reaction('\N{Regional Indicator Symbol Letter B}')
            await msg.add_reaction('\N{Regional Indicator Symbol Letter C}')

            addition_process = DebtProcess.AddProcess(sender, recipient, msg.id)
            self.__running_processes[recipient.id] = addition_process
            self.__running_processes[sender.id] = addition_process

        @self.command()
        async def cancel(ctx: commands.context):
            # cancels all active processes of user, so they can use the system again
            pass

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.user.id:
            return

        if payload.user_id not in self.__running_processes:
            return

        completed = await self.__running_processes[payload.user_id].process_reaction(payload)

        if completed:
            sender = self.__running_processes[payload.user_id].user1
            recipient = self.__running_processes[payload.user_id].user2
            del self.__running_processes[sender.id]
            del self.__running_processes[recipient.id]

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content[0] == ".":
            await self.process_commands(message)
            return

        sender_id = message.author.id

        if sender_id not in self.__running_processes:
            return

        completed = await self.__running_processes[sender_id].process_message(message)

        if completed:
            sender = self.__running_processes[sender_id].user1
            recipient = self.__running_processes[sender_id].user2
            del self.__running_processes[sender.id]
            del self.__running_processes[recipient.id]

    def run_bot(self):
        load_dotenv()
        self.run(os.getenv("TOKEN"))
