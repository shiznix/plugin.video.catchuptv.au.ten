import os
import sys
import urllib
import unicodedata
import xbmc
import xbmcaddon
import xbmcgui

def get_addon():
    return xbmcaddon.Addon()

def get_addon_id():
    """Helper function for returning the version of the running add-on"""
    return get_addon().getAddonInfo('id')


def get_addon_name():
    """Helper function for returning the version of the running add-on"""
    return get_addon().getAddonInfo('name')


def get_addon_version():
    """Helper function for returning the version of the running add-on"""
    return get_addon().getAddonInfo('version')

def ensure_ascii(s):

    if sys.version_info >= (3, 0):
        return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')

    else:
        return unicodedata.normalize('NFD', s.decode('utf-8')).encode('ascii', 'ignore')

def log(s):
    xbmc.log("[%s v%s] %s" % (get_addon_name(), get_addon_version(), ensure_ascii(s)), level=xbmc.LOGNOTICE)

def dbg(s):
    from pprint import pformat
    s = pformat(s, 4, 200)
    xbmc.log("[%s v%s] %s" % (get_addon_name(), get_addon_version(), ensure_ascii(s)), level=xbmc.LOGNOTICE)


def handle_error(message):
    if isinstance(message, str):
        message = message.split('\n')

    message = ["%s v%s" % (get_addon_name(), get_addon_version())] + message

    xbmcgui.Dialog().ok(*message)

def build_next_url(params):
    params['page'] = int(params['page']) + 1 if 'page' in params else 1
    params['query'] = urllib.quote_plus(params['query'])
    return '&'.join('{k}={v}'.format(k=_, v=params[_]) for _ in params)
