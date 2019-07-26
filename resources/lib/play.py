import config
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import session
from aussieaddonscommon import utils

_url = sys.argv[0]
_handle = int(sys.argv[1])


def parse_m3u8(data, qual=-1):
    """
    Parse the retrieved m3u8 stream list into a list of dictionaries
    then return the url for the highest quality stream.
    """
    ver = 0
    if '#EXT-X-VERSION:3' in data:
        ver = 3
        data.remove('#EXT-X-VERSION:3')
    if '#EXT-X-VERSION:4' in data:
        ver = 4
        data.remove('#EXT-X-VERSION:4')
    count = 1
    m3u_list = []
    while count < len(data):
        if ver == 3 or ver == 0:
            line = data[count]
            line = line.strip('#EXT-X-STREAM-INF:')
            line = line.strip('PROGRAM-ID=1,')
            if 'CODECS' in line:
                line = line[:line.find('CODECS')]
            if line.endswith(','):
                line = line[:-1]
            line = line.strip()
            line = line.split(',')
            linelist = [i.split('=') for i in line]
            linelist.append(['URL', data[count + 1]])
            m3u_list.append(dict((i[0], i[1]) for i in linelist))
            count += 2

        if ver == 4:
            line = data[count]
            line = line.strip('#EXT-X-STREAM-INF:')
            line = line.strip('PROGRAM-ID=1,')
            values = line.split(',')
            for value in values:
                if value.startswith('BANDWIDTH'):
                    bw = value
                elif value.startswith('RESOLUTION'):
                    res = value
            url = data[count + 1]
            m3u_list.append(
                dict([bw.split('='), res.split('='), ['URL', url]]))
            count += 3

    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    utils.log('Available streams are: {0}'.format(sorted_m3u_list))
    stream = sorted_m3u_list[qual]['URL']
    return stream


def play_video(params):
    """
    Determine content and pass url to Kodi for playback
    """
    try:
        with session.Session() as sess:
            url = config.BRIGHTCOVE_URL.format(params['id'])
            data = sess.get(url).text.splitlines()
        streamurl = parse_m3u8(data)
        play_item = xbmcgui.ListItem(path=streamurl)
        xbmcplugin.setResolvedUrl(_handle, True, play_item)
    except Exception:
        utils.handle_error('Unable to play video')
