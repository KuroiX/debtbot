import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import DebtProcess
import Accounts


class CommandBot(commands.Bot):

    def __init__(self, account_manager: Accounts.AccountManager):
        default_flags = discord.Intents.default()
        default_flags.message_content = True
        super().__init__(command_prefix=".", intents=default_flags)

        self.__account_manager = account_manager

        self.__define_commands()

        self.__running_processes: [int, DebtProcess.Process] = {}

    def __define_commands(self):
        @self.command()
        async def create_account(ctx: commands.context, user_id: int):
            commander = ctx.author
            try:
                recipient = await self.fetch_user(user_id)
            except discord.errors.NotFound:
                await commander.send("Sorry, the user doesn't exist.")
                return

            # check if account already exists
            acc = self.__account_manager.fetch(commander.id, user_id)

            if acc is not None:
                await commander.send(f"An account between you and {recipient} already exists.")
                return

            registration_process = DebtProcess.RegistrationProcess(commander, recipient, self.__account_manager)
            await registration_process.start()

            self.__running_processes[recipient.id] = registration_process
            self.__running_processes[commander.id] = registration_process

        @self.command()
        async def add(ctx: commands.context):

            commander = ctx.author

            accs = self.__account_manager.find_all(commander.id)

            if len(accs) == 0:
                await commander.send(f"Seems like you don't have any accounts."
                                     f"If you want to create one, use the command ``.add_account user_id``")
                return

            recipients = []

            for user_id in accs:
                try:
                    recipient = await self.fetch_user(user_id)
                    recipients.append(recipient)
                except discord.errors.NotFound:
                    await ctx.send(f"Account {user_id} is in database, but no user could be found.")
                    pass

            choose_process = DebtProcess.ChooseAccountProcess(commander, commander, recipients, self)
            await choose_process.start()

            self.__running_processes[commander.id] = choose_process

        @self.command()
        async def add_by_id(ctx: commands.context, user_id: int):

            commander = ctx.author

            try:
                recipient = await self.fetch_user(user_id)
            except discord.errors.NotFound:
                await ctx.send("Sorry, the user doesn't exist.")
                return

            acc = self.__account_manager.fetch(commander.id, user_id)

            if acc is None:
                await commander.send(f"Seems like you don't have an account with {recipient}. "
                                     f"If you want to create one, use the command ``.add_account user_id``")
                return

            addition_process = DebtProcess.AddProcess(commander, recipient, acc)
            await addition_process.start()

            self.__running_processes[recipient.id] = addition_process
            self.__running_processes[commander.id] = addition_process

        @self.command()
        async def show(ctx: commands.context, user_id: int):
            commander = ctx.author

            try:
                recipient = await self.fetch_user(user_id)
            except discord.errors.NotFound:
                await ctx.send("Sorry, the user doesn't exist.")
                return

            acc = self.__account_manager.fetch(commander.id, user_id)

            if acc is None:
                await commander.send(f"Seems like you don't have an account with {recipient}. "
                                     f"If you want to create one, use the command ``.add_account <user_id>``")
                return

            balance = acc.balance
            if not acc.is_owner(commander.id):
                balance *= -1

            await commander.send(f"Your current balance with {recipient.name} is: {balance}€")

        @self.command()
        async def cancel(ctx: commands.context):
            # cancels all active processes of user, so they can use the system again
            pass

        @self.command()
        async def _help(ctx: commands.context):
            #  give list of all commands
            pass

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.user.id:
            return

        if payload.user_id not in self.__running_processes:
            return

        sender_id = payload.user_id

        if sender_id not in self.__running_processes:
            return

        completed = await self.__running_processes[sender_id].process(payload)

        if completed:
            code, data = self.__running_processes[sender_id].next_steps()
            self.__remove_process(sender_id)
            if code == 0:
                acc = self.__account_manager.fetch(data[0].id, data[1].id)
                await self.start_add_process(data[0], data[1], acc)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content[0] == ".":
            await self.process_commands(message)
            return

        sender_id = message.author.id

        if sender_id not in self.__running_processes:
            return

        completed = await self.__running_processes[sender_id].process(message)

        if completed:
            code, data = self.__running_processes[sender_id].next_steps()
            self.__remove_process(sender_id)
            if code == 0:
                acc = self.__account_manager.fetch(data[0].id, data[1].id)
                await self.start_add_process(data[0], data[1], acc)

    async def start_add_process(self, requester: discord.User, recipient: discord.User, acc: Accounts.Account):
        addition_process = DebtProcess.AddProcess(requester, recipient, acc)
        await addition_process.start()

        self.__running_processes[recipient.id] = addition_process
        self.__running_processes[requester.id] = addition_process

    def __remove_process(self, sender_id):
        sender = self.__running_processes[sender_id].requester
        recipient = self.__running_processes[sender_id].recipient
        del self.__running_processes[sender.id]
        if sender.id != recipient.id:
            del self.__running_processes[recipient.id]

    def run_bot(self):
        load_dotenv()
        self.run(os.getenv("TEST_TOKEN"))
