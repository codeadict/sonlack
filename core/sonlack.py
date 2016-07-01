import re
import random

import spotipy
from soco import SoCo

from slackbot.bot import listen_to, respond_to
from slacker import Slacker
import slackbot_settings as conf

SLACK_MSG_DEFAULT_KWARGS = {
    'as_user': False,
    'username': conf.NAME.capitalize(),
    'icon_url': 'https://avatars.slack-edge.com/2016-06-30/55979414291_73f334a62a9e2750436a_72.png',
}

spotify = spotipy.Spotify()
slack = Slacker(conf.API_TOKEN)
speaker = SoCo(conf.SPEAKER_IP)


@listen_to('^help$', re.IGNORECASE)
@respond_to('^help$', re.IGNORECASE)
def help(message):
    """
    Shows Robot Help.
    """
    try:
        print('Got command help')
        message.reply('\n'.join((
            ' :musical_note: :guitar: :robot_face: Hello! I\'m ' + conf.NAME + '. and i play cool',
            ' music on your Sonos speakers.  Here\'s how I work: :rock:\n'
            '  -  `@' + conf.NAME + ' help` -- Shows this help.',
            '  -  `@' + conf.NAME + ' playing` -- Get current song info.',
            '  -  `@' + conf.NAME + ' search <SONG_NAME>` -- Search for a song.',
            '  -  `@' + conf.NAME + ' add <SONG_NAME>` -- Add song and start playing it.',
            '  -  `@' + conf.NAME + ' stop <SONG_NAME>` -- Stops playing.',
            '  -  `@' + conf.NAME + ' next` -- Play next song on playlist.',
            '  -  `@' + conf.NAME + ' prev` -- Play previous song on playlist.',
            '  -  `@' + conf.NAME + '  :thumbsdown:` -- Skips the current song.',
            '  -  `@' + conf.NAME + ' vol` -- Show current volume.',
            '  -  `@' + conf.NAME + ' vol <VOLUME>` -- Sets volume to the specified level.',
        )))
    except Exception as e:
        print(message, e)


@listen_to('^search (.*)', re.IGNORECASE)
@respond_to('^search (.*)', re.IGNORECASE)
def search(message, song_name):
    """
    Search for a song.
    """
    try:
        print('Got command search {}'.format(song_name))
        if not song_name:
            message.reply(
                'Please provide a song name')
            return
        songs = spotify.search(q=song_name, limit=5)
        if 'tracks' in songs and len(songs['tracks']['items']):
            message.reply('_Found songs:_')
            found = []
            for i, song in enumerate(songs['tracks']['items']):
                found.append(
                    ' ' + str(i + 1) + '. `' + song['name'] + '` by ' + song['artists'][0]['name'])
            message.send_webapi('\n'.join(found))
        else:
            message.reply(':face_with_head_bandage: Can\'t find any song with this name.')
    except Exception as e:
        print(message, e)


@listen_to(':thumbsdown:', re.IGNORECASE)
@respond_to(':thumbsdown:', re.IGNORECASE)
def skip(message):
    """
    Skips current song.
    """
    responses = [
        'There is two kinds of music, the good, and the bad. I play the good kind.',
        'If I find myself just not feeling like playing songs anymore, I think I\'ll drop it.',
        'Well! Think that\'s an awful song. Playing next.',
        'We should removing that shit.',
        'LOL! What a bad taste.',
        'I should in fairness add that peoples taste in music is reputedly deplorable.',
        'Bad taste is simply saying the truth before it should be said.',
        'I like all music. The only music I don\'t like is bad music.'
    ]
    try:
        print('Got command skip.')
        message.reply(random.choice(responses))
    except Exception as e:
        print(message, e)


@listen_to('^vol ([0-9]+)$', re.IGNORECASE)
@respond_to('^vol ([0-9]+)$', re.IGNORECASE)
def volume(message, value):
    """
    Shows current volume
    """
    print('Got command Volume.')
    try:
        if value and int(value):
            message.reply('Setting volume to {}'.format(value))
            speaker.volume = value
        else:
            message.reply(speaker.volume)
    except Exception as e:
        print(message, e)


@listen_to('next', re.IGNORECASE)
@respond_to('next', re.IGNORECASE)
def next(message):
    """
    Play next song.
    """
    try:
        print('Got command Next.')
        message.reply(speaker.next())
    except Exception as e:
        print(message, e)


@listen_to('prev', re.IGNORECASE)
@respond_to('prev', re.IGNORECASE)
def previous(message):
    """
    Play previous song.
    """
    try:
        print('Got command Previous.')
        message.reply(speaker.previous())
    except Exception as e:
        print(message, e)