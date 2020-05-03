import urlparse
import urllib
import unicodedata
import utils

class wrapper(object):
    def __init__(self):
        pass

    def make_kodi_url(self):
        url = ''

        for key in self.__dict__:
            value = self.__dict__[key]

            if isinstance(value, unicode):
                value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
            if isinstance(value, str):
                value = urllib.quote_plus(value)
            url += '&{0}={1}'.format(key, value)

        return url

    def parse_kodi_url(self, url):
        params = urlparse.parse_qsl(url)
        for item in params.keys():
            setattr(self, item, urllib.unquote_plus(params[item]))

    def __get__(self, obj, val):
        if isinstance(val, str):
            return urllib.unquote_plus(val)
        return val
