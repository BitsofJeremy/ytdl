# ### CREATE A DB ###

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Added  pool_size=10, max_overflow=20
# https://docs.sqlalchemy.org/en/20/errors.html#error-3o7r
engine = create_engine('sqlite:///ytdl_database.db', pool_size=10, max_overflow=20)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Channels(Base):
    """ Individual channel data """
    __tablename__ = 'channels'

    """
    {
    "id": "Integer",  # created by DB
    "channel_name": "string", *required
    "url": "string", *required
    "videos": "Array of Video channel_names"
    "filters": "Array of video filters"
    }
    """

    id = Column(Integer, primary_key=True)
    channel_name = Column(String())
    url = Column(String())
    videos = relationship("Videos", cascade="all, delete-orphan")
    filters = relationship("VideoFilters", cascade="all, delete-orphan")

    def __init__(self, channel_name, url):
        self.channel_name = channel_name
        self.url = url

    def update(self, **kwargs):
        """ Updates a subscription """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return "{0} - {1}".format(self.channel_name, self.url)

    @property
    def serialize(self):
        """ Returns a dictionary of the subscription information """
        return {
            "id": self.id,
            "channel_name": self.channel_name,
            "url": self.url,
            "videos": self.videos,
            "filters": self.filters
        }


class Videos(Base):
    """ Individual Videos data """
    __tablename__ = 'videos'

    """
    {
    "id": "Integer",  # created by DB
    "channel": "string", *required
    "channel_id": "FK -> Channels",
    "video_url": "string", *required
    "video_title": "string", *required
    "video_id": "string", *required
    # String for now, switch to datetime later
    "date_published": "datetime", *required
    "summary": "string",
    "media_thumbnail": "string",
    "downloaded": "Boolean",
    "removed": "Boolean",
    "moved": "Boolean",
    }
    """

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel_name = Column(String())
    video_url = Column(String())
    video_title = Column(String())
    video_id = Column(String())
    date_published = Column(String())
    summary = Column(String())
    media_thumbnail = Column(String())
    downloaded = Column(Boolean(), default=False)
    removed = Column(Boolean(), default=False)
    moved = Column(Boolean(), default=False)

    def __init__(self, channel_id, video_title, video_id, video_url, date_published, summary, media_thumbnail):
        self.channel_id = channel_id
        self.video_title = video_title
        self.video_id = video_id
        self.video_url = video_url
        self.date_published = date_published
        self.summary = summary
        self.media_thumbnail = media_thumbnail

    def __repr__(self):
        return "{0} - {1}".format(self.id, self.video_title)

    def update(self, **kwargs):
        """ Updates a video """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def serialize(self):
        """ Returns a dictionary of the video information """
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "video_url": self.video_url,
            "video_title": self.video_title,
            "video_id": self.video_id,
            "date_published": self.date_published,
            "summary": self.summary,
            "media_thumbnail": self.media_thumbnail,
            "downloaded": self.downloaded,
            "removed": self.removed,
            "moved": self.moved,
        }


class VideoFilters(Base):
    """ Filters Table """
    __tablename__ = 'video_filters'

    """
    {
    "id": "Integer",  # created by DB
    "channel_name": "string",
    "channel_id": "FK -> Channels",
    "filter_name": "string", *required
    "filter_text": "string", *required
    "enabled": "Boolean",
    }
    """

    id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel_name = Column(String())
    filter_name = Column(String())
    filter_text = Column(String())
    enabled = Column(Boolean(), default=False)

    def __init__(self, channel_id, channel_name, filter_name, filter_text, enabled):
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.filter_name = filter_name
        self.filter_text = filter_text
        self.enabled = enabled

    def __repr__(self):
        return "{0} - {1}".format(self.id, self.filter_name)

    def update(self, **kwargs):
        """ Updates a filter """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def serialize(self):
        """ Returns a dictionary of the filter information """
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "channel_name": self.channel_name,
            "filter_name": self.filter_name,
            "filter_text": self.filter_text,
            "enabled": self.enabled
        }


def main():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()
    session.close()
    print("Created DB")


if __name__ == '__main__':
    main()
