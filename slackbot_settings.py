from os import getenv

DEFAULT_REPLY = 'Hey there! I kinda didn\'t get what you mean, sorry.'

# the bot name
NAME = 'sonlack'

PLUGINS = [
    'core.sonlack',
]

API_TOKEN = getenv('SLACK_API_TOKEN', '')

SPEAKER_IP = getenv('SPEAKER_IP', '127.0.0.1')