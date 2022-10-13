import discord
import os
from dotenv import load_dotenv


def unsubscribe(bot: discord.Client):
    @bot.event
    async def on_message(message: discord.Message):
        if message.author == bot.user:
            return

        await message.channel.send("this is my last message")


class HiBot:

    bot: discord.Client

    def __init__(self):
        default_flags = discord.Intents.default()
        default_flags.message_content = True

        self.bot = discord.Client(intents=default_flags)

        load_dotenv()

        @self.bot.event
        async def on_message(message: discord.Message):
            if message.author == self.bot.user:
                return

            # call user.state.on_message as state machine

            print(message.content)

            msg = await message.channel.send("Tag leude!")
            await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
            await msg.add_reaction('\N{CROSS MARK}')

            # unsubscribe(self.bot)

        @self.bot.event
        async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
            print("reaction")
            if user == self.bot.user:
                return

            # call user.state.on_message as state machine

            msg = await reaction.message.channel.send("Nice reaction!")
            # msg.id

        @self.bot.event
        async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
            if payload.user_id == self.bot.user.id:
                return

            # payload.message_id ==
            if payload.emoji == '\N{WHITE HEAVY CHECK MARK}':
                print("yay")

            print(payload.emoji)

    def run_bot(self):
        self.bot.run(os.getenv("TOKEN"))
