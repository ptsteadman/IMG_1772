from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from Youtube import Youtube
import cgi

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Video
    )

class Index(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='index', renderer='templates/index.jinja2',
            request_method='GET')
    def index_get(self):
        request = self.request
        url = request.session['url'] if 'url' in request.session else ""
        caption = request.session['caption'] if 'caption' in request.session else ""
        if 'message' in request.session:
            message = request.session['message']
            del(request.session['message'])
        else:
            message = "Only videos with less than 100 views will be accepted."
        try:
            videos = DBSession.query(Video)
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        return {'project': 'IMG_1772','url': url, 'caption': caption, 'message':
                message, 'videos' : videos}

    @view_config(route_name='index', renderer='templates/index.jinja2',
            request_method='POST')
    def index_post(self):
        request = self.request
        if request.params['url']:
            request.session['url'] = request.params['url'] 
            request.session['caption']= request.params['caption']
            if len(request.session['caption']) > 1000:
                request.session['message'] = "Your thoughts are too long."
                return HTTPFound(location='/')
            capt = cgi.escape(request.session['caption'])
            num_views = Youtube.get_num_views(request.session['url'])
            vid = Youtube.video_id(request.session['url'])
            if num_views is False:
                request.session['message'] = "That URL has a problem."
                return HTTPFound(location='/')
            if num_views > 100:
                request.session['message'] = "This video has over 100 views."
                return HTTPFound(location='/')
            test = DBSession.query(Video).filter(Video.youtube_id == vid).first()
            if test is not None:
                request.session['message'] = "This video is already in IMG_1772."
                return HTTPFound(location='/')
            # ok the video and caption are okay
            video = Video(youtube_id=vid,caption=capt,added_by="test", views=
                        num_views)
            DBSession.add(video)
            request.session['message'] = "Video added to IMG_1772."
            return HTTPFound(location='/')
        return HTTPFound(location='/')

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_IMG_1772_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

