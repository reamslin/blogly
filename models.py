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

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='posts')





