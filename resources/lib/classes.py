import urlparse
import urllib
import unicodedata


class series(object):
    def __init__(self):
        self.season = None
        self.total_episodes = None
        self.fanart = None
        self.banner = None
        self.thumb = None
        self.query = None
        self.series_name = None
        self.series_slug = None
        self.season_name = None
        self.season_slug = None
        self.genre = None
        self.title = None

    def get_title(self):
        if self.multi_season:
            return '{0} {1}'.format(self.series_name, self.season_name)
        else:
            return self.series_name

    def make_kodi_url(self):
        d = self.__dict__
        for key, value in d.iteritems():
            if isinstance(value, unicode):
                d[key] = unicodedata.normalize(
                    'NFKD', value).encode('ascii', 'ignore')
        url = ''
        if d['thumb']:
            d['thumb'] = urllib.quote_plus(d['thumb'])
        if d['query']:
            d['query'] = urllib.quote_plus(d['query'])
        if d['fanart']:
            d['fanart'] = urllib.quote_plus(d['fanart'])
        if d['genre']:
            d['genre'] = urllib.quote_plus(d['genre'])
        if d['banner']:
            d['banner'] = urllib.quote_plus(d['banner'])
        for item in d.keys():
            url += '&{0}={1}'.format(item, d[item])
        return url

    def parse_kodi_url(self, url):
        params = urlparse.parse_qsl(url)
        for item in params.keys():
            setattr(self, item, urllib.unquote_plus(params[item]))

    def get_fanart(self):
        if self.fanart:
            return urllib.unquote_plus(self.fanart)

    def get_banner(self):
        if self.banner:
            return urllib.unquote_plus(self.banner)


class episode(object):
    def __init__(self):
        self.fanart = None
        self.thumb = None
        self.title = None
        self.desc = None
        self.airdate = None
        self.duration = None
        self.episode_no = None
        self.episode_name = None
        self.url = None
        self.page = None
        self.query = None
        self.season = None
        self.category = None
        self.id = None

    def get_title(self):
        return 'Ep {0} - {1}'.format(self.episode_no, self.episode_name)

    def get_airdate(self):
        return '{0}.{1}.{2}'.format(self.airdate[8:10],
                                    self.airdate[5:7],
                                    self.airdate[0:4])

    def make_kodi_url(self):
        d = self.__dict__
        for key, value in d.iteritems():
            if isinstance(value, unicode):
                d[key] = unicodedata.normalize(
                    'NFKD', value).encode('ascii', 'ignore')
        url = ''
        if d['thumb']:
            d['thumb'] = urllib.quote_plus(d['thumb'])
        if d['fanart']:
            d['fanart'] = urllib.quote_plus(d['fanart'])
        for item in d.keys():
            url += '&{0}={1}'.format(item, d[item])
        return url

    def parse_kodi_url(self, url):
        params = urlparse.parse_qsl(url)
        for item in params.keys():
            setattr(self, item, urllib.unquote_plus(params[item]))
