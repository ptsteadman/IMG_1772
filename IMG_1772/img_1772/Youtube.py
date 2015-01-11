import json
import urllib2
from urlparse import urlparse, parse_qs
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import random

DEVELOPER_KEY = "AIzaSyDcwqu-TxwHNgmwowXCVhsnuoie6sSQgiY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
        try:
            vid = Youtube.video_id(url)
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)
            response = youtube.videos().list(
                id = vid,
                part = "statistics"
            ).execute()
            num_views = response.get("items", [])[0]["statistics"]["viewCount"]
        except Exception as exc:
            print exc
            return False
        return int(num_views)

    @staticmethod
    def get_title(url):
        try:
            vid = Youtube.video_id(url)
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)
            response = youtube.videos().list(
                id = vid,
                part = "snippet"
            ).execute()
            title = response.get("items", [])[0]["snippet"]["title"]
        except:
            return False
        return title
    
    @staticmethod
    def get_random_video():
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)
        num = random.randint(1000,9999)

        search_response = youtube.search().list(
            q = "IMG_" + str(num),
            part = "id",
            maxResults = "25",
            type = "video",
            videoEmbeddable = "true"
        ).execute()

        videos = []

        for result in search_response.get("items", []):
            videos.append(result['id']['videoId'])
        
        video_index = random.randint(0, len(videos) - 1)
        num_views = 1000
        count = 0

        while num_views > 100 and count < 30:
            count = count + 1 # just in case
            vid = videos[video_index]
            response = youtube.videos().list(
                id = vid,
                part = "statistics"
            ).execute()
            num_views = int(response.get("items",[])[0]["statistics"]["viewCount"])
            if num_views > 100:
                video_index = random.randint(0, len(videos) - 1)

        return videos[video_index]
