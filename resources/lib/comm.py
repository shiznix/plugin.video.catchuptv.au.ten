import base64
import classes
import config
import json
import time
import urllib
import session
import utils

def fetch_url(url):

    headers = {
        'Origin': 'https://10play.com.au', 
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }

    with session.Session(force_tlsv1=True) as sess:
        sess.headers.update(headers)
        res = sess.get(url)
        return res.text

def get_shows(params):
    data = json.loads(fetch_url(config.SHOWLIST_URL))
    listing = []

    for show in data['Browse TV']['Shows']:
        s = classes.wrapper()
        s.id = int(show['id'])
        s.title = show['title']
        s.query = show['query']
        s.genre = show['genre']
        s.fanart = show['tvBackgroundURL']
        s.logo = show['logoURL']
        s.banner = show['tvBannerURL']
        s.nb_seasons = len(show['seasons'])
        listing.append(s)

    return listing


def get_seasons(params):
    data = json.loads(fetch_url(config.SHOWLIST_URL))
    listing = []

    for show in data['Browse TV']['Shows']:

        if int(show['id']) != int(params['id']):
            continue

        for season in show['seasons']:

            s = classes.wrapper()
            s.show_id = int(show['id'])
            s.logo = show['logoURL']
            s.id = season['seasonId']
            s.name = season['seasonName']
            s.query = params['query'] + season['query']
            listing.append(s)

    return listing


def get_episodes(params):

    page = params.get('page', 0)
    url = config.EPISODEQUERY_URL.format(urllib.unquote(params['query']), page)

    data = json.loads(fetch_url(url))

    listing = []
    for episode in data['items']:
        e = classes.wrapper()
        e.thumb = episode['videoStillURL']
        e.fanart = urllib.unquote(params.get('fanart', ''))
        e.title = episode['customFields'].get('clip_title')
        if not e.title:
            e.title = episode.get('name')
        if 'shortDescription' in episode:
            e.desc = episode['shortDescription'] + " ("+ episode['availability'] +")"
        elif 'longDescription' in episode:
            e.desc = episode['shortDescription'] + " ("+ episode['availability'] +")"
        else:
            e.desc = episode['name'] + " ("+ episode['availability'] +")"
        e.duration = episode['length']/1000
        e.airdate = episode['customFields']['start_date_act']
        e.page = int(page)
        e.id = episode['id']
        e.hlsurl = episode['HLSURL']
        e.total_episodes = int(data['total_count'])
        if e.total_episodes > 30:
            e.query = urllib.quote(params['query'])
            e.season = params['id']
            e.category = params['category']
        listing.append(e)
    return listing

def get_genres():
    data = json.loads(fetch_url(config.SHOWLIST_URL))
    listing = []
    for genre in data['Browse TV']['Genres']:
        listing.append(genre)
    return listing
