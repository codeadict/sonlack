import logging
from slackbot.bot import Bot

logger = logging.getLogger('sonlack')


def main():
    """Then main Bot application"""
    bot = Bot()
    print('Sonlack is rocking now. Enjoy your favorite music...')
    bot.run()


if __name__ == "__main__":
    main()
