import comm
import sys
import xbmcgui
import xbmcplugin
import utils

_url = sys.argv[0]
_handle = int(sys.argv[1])

def list_categories():
    listing = []
    categories = comm.get_genres()
    categories.insert(0, 'All shows')
    for category in categories:
        li = xbmcgui.ListItem(category)
        url = '{0}?action=listcategories&category={1}'.format(_url, category)
        listing.append((url, li, True))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_seasons(params):
    try:
        seasons = comm.get_seasons(params)
        listing = []
        for s in seasons:
            li = xbmcgui.ListItem(s.name, iconImage=s.logo, thumbnailImage=s.logo)
            url = '{0}?action=listseasons&category={1}{2}'.format(_url, params['category'], s.make_kodi_url())
            listing.append((url, li, True))

        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)

    except Exception:
        utils.handle_error('Unable to list seasons')

def list_shows(params):
    try:
        listing = []
        
        for s in comm.get_shows(params):
            if params['category'] in ['All shows', s.genre]:
                li = xbmcgui.ListItem(s.title, iconImage=s.logo, thumbnailImage=s.logo)
                li.setArt({'fanart': s.fanart, 'banner': s.banner})
                url = '{0}?action=listshows&category={1}{2}'.format(_url, params['category'], s.make_kodi_url())
                listing.append((url, li, True))

        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)

    except Exception:
        utils.handle_error('Unable to list shows')


def list_episodes(params):

    try:
        episodes = comm.get_episodes(params)
        listing = []

        for e in episodes:
            li = xbmcgui.ListItem(e.title, iconImage=e.thumb, thumbnailImage=e.thumb)
            li.setArt({'fanart': e.fanart})
            url = '{0}?action=listepisodes{1}'.format(_url, e.make_kodi_url())
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {'plot': e.desc, 'plotoutline': e.desc, 'duration': e.duration, 'date': '{0}.{1}.{2}'.format(e.airdate[8:10], e.airdate[5:7], e.airdate[0:4])})
            listing.append((url, li, False))

        if len(episodes) == 30:
            url = '{0}?action=listeseasons&{1}'.format(_url, utils.build_next_url(params))
            li = xbmcgui.ListItem('Next page')
            listing.append((url, li, True))

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)

    except Exception:
        utils.handle_error('Unable to list episodes')
