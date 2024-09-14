from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime

from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.sql import func

from database import Base



class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), unique=True, nullable=False)

    newsposts = relationship("NewsPost", back_populates="category")

   

class NewsPost(Base):
    __tablename__ = 'newspost'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id'))

    title = Column(String(255), nullable=False)

    description = Column(Text, nullable=False)

    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    images = relationship("Image", back_populates='newspost', lazy='selectin',  cascade="all, delete-orphan")

    category = relationship("Category", back_populates='newsposts')

    comments = relationship("NewsPostComments", back_populates='newspost')







class Image(Base):
    __tablename__ = 'posts_image'

    id = Column(Integer, primary_key=True, autoincrement=True)

    news_post_id = Column(Integer, ForeignKey('newspost.id', ondelete='CASCADE'), nullable=False)

    image = Column(String, nullable=False) 

    uploaded_at = Column(DateTime, server_default=func.now())

    newspost = relationship("NewsPost", back_populates="images")

class NewsPostComments(Base):

    __tablename__ = 'news_post_comment'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    news_post_id = Column(Integer, ForeignKey('newspost.id', ondelete='CASCADE'))

    comment = Column(String)

    newspost = relationship("NewsPost", back_populates='comments')
