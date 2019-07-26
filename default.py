import os
import sys
import xbmc
import xbmcaddon
from urlparse import parse_qsl

from aussieaddonscommon import utils

addon = xbmcaddon.Addon()
cwd = xbmc.translatePath(addon.getAddonInfo('path')).decode("utf-8")
BASE_RESOURCE_PATH = os.path.join(cwd, 'resources', 'lib')
sys.path.append(BASE_RESOURCE_PATH)

import menu  # noqa: E402
import play  # noqa: E402


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listcategories':
            if params['category'] == 'Featured':
                menu.list_featured()
            else:
                menu.list_shows(params)
        elif params['action'] == 'listshows':
            menu.list_episodes(params)
        elif (params['action'] == 'listepisodes'
              or params['action'] == 'listfeatured'):
            play.play_video(params)
        elif params['action'] == 'sendreport':
            utils.user_report()
    else:
        menu.list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])
