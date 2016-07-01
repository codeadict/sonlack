from os import getenv

DEFAULT_REPLY = 'Hey there! I kinda didn\'t get what you mean, sorry.'

# the bot name
NAME = 'sonlack'

PLUGINS = [
    'core.sonlack',
]

API_TOKEN = getenv('SLACK_API_TOKEN', 'xoxb-56032071207-5rHWEWhcuNmQgXppEVouML5l')

SPEAKER_IP = getenv('SPEAKER_IP', '10.10.0.62')

ROVI_API_KEY = '39gxk7ny8as24ycfhv8hwdfu'
ROVI_SHARED_SECRET = '4uNJF6bezA'