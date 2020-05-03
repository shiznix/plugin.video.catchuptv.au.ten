import config
import sys
import session
import utils
import xbmcgui
import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])

def play_video(params):
    """
    Determine content and pass url to Kodi for playback
    """
    try:
        with session.Session() as sess:
            url = params['hlsurl'] + '|User-Agent=%s' % config.USER_AGENT
        play_item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(_handle, True, play_item)
    except Exception:
        utils.handle_error('Unable to play video')
