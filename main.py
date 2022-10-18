from Bots import CommandBot
from Accounts import AccountManager


def main():
    account_manager = AccountManager()
    command_bot = CommandBot.CommandBot(account_manager)
    command_bot.run_bot()


if __name__ == "__main__":
    main()
