from os import getenv

DEFAULT_REPLY = 'Hey there! I kinda didn\'t get what you mean, sorry.'

# the bot name
NAME = 'sonlack'

PLUGINS = [
    'core.sonlack',
]

API_TOKEN = getenv('SLACK_API_TOKEN', None)

SPEAKER_IP = getenv('SPEAKER_IP', None)

ROVI_API_KEY = getenv('ROVI_API_KEY', None)
ROVI_SHARED_SECRET = getenv('ROVI_SHARED_SECRET', None)