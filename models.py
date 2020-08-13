"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
NO_IMAGE_DEFAULT = 'https://thumbs.dreamstime.com/b/no-image-available-icon-photo-camera-flat-vector-illustration-132483097.jpg'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
    primary_key=True,
    autoincrement=True)
    
    first_name = db.Column(db.String(50),
    nullable=False)

    last_name = db.Column(db.String(50),
    nullable=False)

    image_url = db.Column(db.Text, nullable=False,
    default=NO_IMAGE_DEFAULT)

    posts = db.relationship("Post", back_populates="user", cascade="all, delete", passive_deletes=True)


class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
    primary_key=True,
    autoincrement=True)

    title = db.Column(db.Text, nullable=False,
    default='Untitled')

    content = db.Column(db.Text, nullable=False,
    default = '')

    created_at = db.Column(db.DateTime, nullable=False,
    default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

    user = db.relationship("User", back_populates="posts")


class TagPost(db.Model):
    """TagPost through relationship model"""

    __tablename__ = 'tags_posts'

    tag_id = db.Column(db.Integer,
    db.ForeignKey("tags.id"),
    primary_key=True)

    post_id = db.Column(db.Integer,
    db.ForeignKey("posts.id"),
    primary_key=True)

class Tag(db.Model):
    """Tag model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
    autoincrement=True,
    primary_key=True)

    name = db.Column(db.String(100), 
    nullable=False)

    posts = db.relationship('Post',
    secondary = 'tags_posts',
    backref='tags')






