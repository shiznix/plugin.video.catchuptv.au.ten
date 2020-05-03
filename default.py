import sys
import xbmc

from urlparse import parse_qsl
from resources.lib import menu
from resources.lib import play


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listcategories':
            menu.list_shows(params)
        elif params['action'] == 'listshows':
            menu.list_seasons(params)
        elif params['action'] == 'listseasons':
            menu.list_episodes(params)
        elif params['action'] == 'listepisodes':
            play.play_video(params)
    else:
        menu.list_categories()

if __name__ == '__main__':
    router(sys.argv[2][1:])
