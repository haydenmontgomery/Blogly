"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):    
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                        nullable=False,
                        unique=True)
    
    last_name = db.Column(db.String(50),
                        nullable=False,
                        unique=True)
    
    image_url = db.Column(db.String,
                        nullable=True,
                        unique=True)
    
    def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last name={u.last_name} profile pic={u.image_url}>"