import time
import hashlib
import json

import requests
from urllib.parse import quote_plus
import slackbot_settings as conf


def gen_sig():
    return hashlib.md5(
        conf.ROVI_API_KEY.encode('utf-8') +
        conf.ROVI_SHARED_SECRET.encode('utf-8') +
        repr(int(time.time()))).hexdigest()


def get_track_image(artist, album):
    """
    Get album art from Rovi API.
    :param artist:
    :param album:
    :return:
    """
    headers = {
        "Accept-Encoding": "gzip"
    }
    req = requests.get(
        'http://api.rovicorp.com/recognition/v2.1/music/match/album?apikey=' +
        conf.ROVI_API_KEY + '&sig=' + gen_sig() + '&name= ' +
        quote_plus(album) + '&performername=' + quote_plus(artist) + '&include=images&size=1',
        headers=headers)
    print((req.content))

    result = json.loads(req.content)
    print(result)
    try:
        return result['matchResponse']['results'][0]['album']['images'] \
            [0]['front'][3]['url']
    except (KeyError, IndexError):
        pass
