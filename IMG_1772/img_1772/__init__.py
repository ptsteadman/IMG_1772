from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import SignedCookieSessionFactory

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory('img_1772')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings, session_factory=my_session_factory)
    config.add_static_view('img_1772_static', 'static', cache_max_age=3600)
    config.add_route('index', '/IMG_1772')
    config.scan()
    return config.make_wsgi_app()
