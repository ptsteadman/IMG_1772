import json
import urllib2
from urlparse import urlparse, parse_qs

class Youtube(object):
    ''' Class for getting data from youtube '''

    @staticmethod 
    def video_id(value):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        query = urlparse(value)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        # fail?
        return None

    @staticmethod
    def get_num_views(url):
        vid = Youtube.video_id(url)
        data_url = "https://gdata.youtube.com/feeds/api/videos/" + vid
        data_url = data_url + "?v=2&alt=json"
        try:
            data = json.load(urllib2.urlopen(data_url))
            num_views = data['entry']['yt$statistics']['viewCount']
        except:
            return False
        return int(num_views)


