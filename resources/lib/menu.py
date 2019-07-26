import comm
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils

_url = sys.argv[0]
_handle = int(sys.argv[1])


def list_categories():
    listing = []
    categories = comm.get_genres()
    categories.insert(0, 'Featured')
    categories.insert(0, 'All shows')
    for category in categories:
        li = xbmcgui.ListItem(category)
        urlString = '{0}?action=listcategories&category={1}'
        url = urlString.format(_url, category)
        is_folder = True
        listing.append((url, li, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_shows(params):
    try:
        shows = comm.get_shows(params)
        genre = ('All' if params['category'] == 'All shows'
                 else params['category'])
        listing = []
        for s in shows:
            if genre == 'All':
                pass
            else:
                if not genre == s.genre:
                    continue
            li = xbmcgui.ListItem(s.title,
                                  iconImage=s.thumb,
                                  thumbnailImage=s.thumb)
            li.setArt({'fanart': s.get_fanart(),
                       'banner': s.get_banner()})
            url = '{0}?action=listshows&category={1}{2}'.format(
                _url, params['category'], s.make_kodi_url())
            is_folder = True
            listing.append((url, li, is_folder))
        xbmcplugin.addSortMethod(
            _handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to list shows')


def list_episodes(params):
    try:
        episodes = comm.get_episodes(params)
        listing = []
        if episodes:
            page = episodes[0].page
            for e in episodes:
                li = xbmcgui.ListItem(e.title,
                                      iconImage=e.thumb,
                                      thumbnailImage=e.thumb)
                li.setArt({'fanart': e.fanart})
                url = '{0}?action=listepisodes{1}'.format(_url,
                                                          e.make_kodi_url())
                is_folder = False
                li.setProperty('IsPlayable', 'true')
                li.setInfo('video', {'plot': e.desc,
                                     'plotoutline': e.desc,
                                     'duration': e.duration,
                                     'date': e.get_airdate()})
                listing.append((url, li, is_folder))

            if episodes[0].total_episodes - (page*30) > 30:
                url = '{0}?action=listshows{1}&page={2}'.format(
                    _url, episodes[0].make_kodi_url(), episodes[0].page+1)
                is_folder = True
                li = xbmcgui.ListItem('next page')
                listing.append((url, li, is_folder))
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to list episodes')


def list_featured():
    try:
        episodes = comm.get_featured()
        listing = []
        for e in episodes:
            li = xbmcgui.ListItem(e.title,
                                  iconImage=e.thumb,
                                  thumbnailImage=e.thumb)
            urlString = '{0}?action=listfeatured&show={1}&id={2}'
            url = urlString.format(_url, e.title, e.id)
            is_folder = False
            li.setInfo('video', {'plot': e.desc, 'plotoutline': e.desc})
            li.setProperty('IsPlayable', 'true')
            listing.append((url, li, is_folder))
        xbmcplugin.addSortMethod(
            _handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to list featured')
