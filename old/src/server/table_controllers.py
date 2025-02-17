
__all__ = [
    'User',
    'video',
    'Access',
    'Search',
    'CartItems'
]
__author__ = 'Felipe Amaral'
__version__ = '0.1'

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    tag = Column(
        String(50), 
        nullable=False
    )
    city = Column(
        String(100), 
        nullable=False
    )
    region = Column(
        String(100), 
        nullable=False
    )
    country = Column(
        String(100), 
        nullable=False
    )
    creation_date = Column(
        DateTime, 
        default=datetime.now
    )
    update_date = Column(
        DateTime, 
        default=datetime.now, 
        onupdate=datetime.now
    )

class Video(base):
    __tablename__ = 'videos'

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    tag = Column(
        String(100), 
        nullable=False
    )
    url = Column(
        String(500), 
        nullable=False
    )
    title = Column(
        String(255), 
        nullable=False
    )
    duration = Column(
        Integer, 
        nullable=False
    )
    view_count = Column(
        Integer, 
        nullable=False
    )
    channel_tag = Column(
        String(100), 
        nullable=False
    )
    channel_url = Column(
        String(500), 
        nullable=False
    )
    channel_name = Column(
        String(255), 
        nullable=False
    )
    thumbnail_url = Column(
        String(500), 
        nullable=False
    )
    channel_is_verified = Column(
        Boolean, 
        nullable=False
    )
    creation_date = Column(
        DateTime, 
        default=datetime.now
    )
    update_date = Column(
        DateTime, 
        default=datetime.now, 
        onupdate=datetime.now
    )
    
class Access(base):
    __tablename__ = 'accesses'

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    user_id = Column(
        Integer, 
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False
    )
    is_active = Column(
        Boolean, 
        default=True
    )
    last_heartbeat = Column(
        DateTime, 
        default=datetime.now
    )
    creation_date = Column(
        DateTime, 
        default=datetime.now
    )

class Search(base):
    __tablename__ = 'searches'

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    user_id = Column(
        Integer, 
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False
    )
    query = Column(
        String(255), 
        nullable=False
    )
    max_results = Column(
        Integer, 
        default=50, 
        nullable=False
    )
    creation_date = Column(
        DateTime, 
        default=datetime.now
    )

class CartItems(base):
    __tablename__ = 'cart_items'

    id = Column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    user_id = Column(
        Integer, 
        ForeignKey('users.id', ondelete='CASCADE'), 
        nullable=False
    )
    video_id = Column(
        Integer, 
        ForeignKey('videos.id', ondelete='CASCADE'), 
        nullable=False
    )
    creation_date = Column(
        DateTime, 
        default=datetime.now
    )
