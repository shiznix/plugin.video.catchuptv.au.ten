import base64
import classes
import config
import json
import time
import urllib

from aussieaddonscommon import session


def create_authheader():
    """Generate token to use for all API requests"""
    timestr = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    encoded = base64.b64encode(timestr)
    return {"X-Network-Ten-Auth": encoded}


def fetch_url(url):
    with session.Session(force_tlsv1=True) as sess:
        res = sess.get(url, headers=create_authheader())
        return res.text


def get_shows(params):
    data = json.loads(fetch_url(config.SHOWLIST_URL))
    listing = []
    for show in data['Browse TV']['Shows']:
        x = len(show['Seasons'])
        multi_season = len(show['Seasons']) > 1
        for x, season in reversed(list(enumerate(show['Seasons']))):
            s = classes.series()
            s.query = show['query']
            s.thumb = show['videoStillURL']
            s.fanart = show['bannerURL']
            s.season = show['Seasons'][x-1]
            s.genre = show['genre']
            if multi_season:
                s.title = '{0} Season {1}'.format(show['title'], s.season)
            else:
                s.title = show['title']
            listing.append(s)
    return listing


def get_episodes(params):
    page = params.get('page', 0)
    url = config.EPISODEQUERY_URL.format(
        urllib.unquote(params['query']), page, params['season'])
    if params['category'] == 'News' or params['category'] == 'Sport':
        url = url.replace('&all=video_type_long_form:Full+Episodes', '')
    data = json.loads(fetch_url(url))
    listing = []
    for episode in data['items']:
        e = classes.episode()
        e.thumb = episode['videoStillURL']
        e.fanart = urllib.unquote(params.get('fanart', ''))
        e.title = episode['customFields'].get('clip_title')
        if not e.title:
            e.title = episode.get('name')
        e.desc = episode['shortDescription']
        e.duration = episode['length']/1000
        e.airdate = episode['customFields']['start_date_act']
        e.page = int(page)
        e.id = episode['id']
        e.total_episodes = int(data['total_count'])
        if e.total_episodes > 30:
            e.query = urllib.quote(params['query'])
            e.season = params['season']
            e.category = params['category']
        listing.append(e)
    return listing


def get_featured():
    data = json.loads(fetch_url(config.FEATURED_URL))
    listing = []
    for episode in data:
        e = classes.episode()
        e.title = episode['name']
        if not e.title:
            continue
        e.thumb = episode['videoStillURL']
        e.desc = episode['short_description']
        e.id = episode['brightcoveid']
        listing.append(e)
    return listing


def get_genres():
    data = json.loads(fetch_url(config.SHOWLIST_URL))
    listing = []
    for genre in data['Browse TV']['Genres']:
        listing.append(genre)
    return listing
