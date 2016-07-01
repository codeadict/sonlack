import json

import re
import random

import spotipy
from soco import SoCo

from slackbot.bot import listen_to, respond_to
from slacker import Slacker
import slackbot_settings as conf
from core.utils import get_track_image

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
        print((message, e))


@listen_to('^search (.*)', re.IGNORECASE)
@respond_to('^search (.*)', re.IGNORECASE)
def search(message, song_name):
    """
    Search for a song.
    """
    try:
        print(('Got command search {}'.format(song_name)))
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
        print((message, e))


@listen_to(':thumbsdown:', re.IGNORECASE)
@respond_to(':thumbsdown:', re.IGNORECASE)
@listen_to('meh!', re.IGNORECASE)
@respond_to('meh!', re.IGNORECASE)
@listen_to('I dont like it', re.IGNORECASE)
@respond_to('I dont like it', re.IGNORECASE)
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
        message.reply(speaker.next())
    except Exception as e:
        print((message, e))


@listen_to('^vol$', re.IGNORECASE)
@listen_to('^vol ([0-9]+)$', re.IGNORECASE)
@respond_to('^vol$', re.IGNORECASE)
@respond_to('^vol ([0-9]+)', re.IGNORECASE)
def volume(message, value=None):
    """
    Shows current volume
    """
    print('Got command Volume.')
    try:
        if value:
            message.reply('Setting volume to {}'.format(value))
            speaker.volume = value
        else:
            print('Print the volume')
            message.reply('Current volume is: *{}*'.format(speaker.volume))
    except Exception as e:
        print((message, e))


@listen_to('next', re.IGNORECASE)
@respond_to('next', re.IGNORECASE)
def next(message):
    """
    Play next song.
    """
    try:
        print('Got command Next.')
        message.reply(next(speaker))
    except Exception as e:
        print((message, e))


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
        print((message, e))


@listen_to('^playing$', re.IGNORECASE)
@respond_to('^playing$', re.IGNORECASE)
def playing(message):
    """
    Play previous song.
    """
    #try:
    print('Got command Playing.')
    song = speaker.get_current_track_info()
    #image_url = get_track_image(song.get('artist'), song.get('album'))
    #print(image_url)
    attachments = [
        {
            "color": "#D30782",
            "pretext": ":musical_note: :musical_note: Now playing:",
            "author_name": song.get('artist'),
            #"thumb_url": image_url,
            "title": song.get('title'),
            "fields": [
                {
                    "title": "Album",
                    "value": song.get('album'),
                    "short": False
                },
                {
                    "title": "Duration",
                    "value": song.get('duration'),
                    "short": False
                }
            ]
        }
    ]
    message.send_webapi('', json.dumps(attachments))

@listen_to('^play$', re.IGNORECASE)
@respond_to('^play$', re.IGNORECASE)
def play():
    print('Got command Play.')
    speaker.play()