from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    youtube_id = Column(Text)
    caption = Column(Text)
    views = Column(Integer)
    added_by = Column(Text)

Index('youtube_id_index', Video.youtube_id, unique=True, mysql_length=255)
