# flake8: noqa

GITHUB_API_URL = 'https://api.github.com/repos/xbmc-catchuptv-au/plugin.video.catchuptv.au.ten'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
ISSUE_API_AUTH = 'eGJtY2JvdDo1OTQxNTJjMTBhZGFiNGRlN2M0YWZkZDYwZGQ5NDFkNWY4YmIzOGFj'
GIST_API_URL = 'https://api.github.com/gists'

CATEGORIES = ['Featured', 'TV Shows', 'News']
SHOWLIST_URL = "http://vod.ten.com.au/config/android-v2"
EPISODEQUERY_URL = "https://v.tenplay.com.au/api/videos/bcquery?command=search_videos&state=act&isMetro=false{0}&get_item_count=true&page_size=30&page_number={1}&video_fields=id,shortDescription,length,videoStillURL,startDate,endDate,ssa_url&custom_fields=start_date_app,clip_title,tv_channel,tv_show,restriction_bymember,tv_season,tv_week,web_content_url,program_classification&platformgroup=ott&platform=YW5kcm9pZA%3D%3D&all=video_type_long_form:Full+Episodes&all=tv_season:{2}"
BRIGHTCOVE_URL = "http://c.brightcove.com/services/mobile/streaming/index/master.m3u8?videoId={0}"
FEATURED_URL = "https://v.tenplay.com.au/api/Homepage/index?state=act"