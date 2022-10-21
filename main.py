from Bots import CommandBot
import Accounts


def main():
    account_manager = Accounts.LocalAccountManager()
    command_bot = CommandBot.CommandBot(account_manager)
    command_bot.run_bot()


if __name__ == "__main__":
    main()
