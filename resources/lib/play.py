import config
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import session
from aussieaddonscommon import utils

_url = sys.argv[0]
_handle = int(sys.argv[1])

def play_video(params):
    """
    Determine content and pass url to Kodi for playback
    """
    try:
        with session.Session() as sess:
            url = (params['hlsurl'] + '&format=m3u8')
            utils.log("M3U8 URL: %s" % url)
        play_item = xbmcgui.ListItem(path=url)
        xbmcplugin.setResolvedUrl(_handle, True, play_item)
    except Exception:
        utils.handle_error('Unable to play video')
