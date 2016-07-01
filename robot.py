import sys
import logging
from slackbot.bot import Bot
import slackbot_settings as conf

logger = logging.getLogger('sonlack')


def main():
    """Then main Bot application"""
    if not conf.API_TOKEN or not conf.SPEAKER_IP:
        print('Slack API token or Sonos speaker IP not set.\n'
              'Please add configure it before running Sonlack. Exiting...')
        sys.exit(0)
    bot = Bot()
    print('Sonlack is rocking now. Enjoy your favorite music...')
    bot.run()


if __name__ == "__main__":
    main()
