"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


""" def connect_db(app):
        db.app = app
        db.init_app(app)
        app.app_context().push()
#db.create_all() """
def connect_db(app):    
    with app.app_context():
        db.app = app
        db.init_app(app)
        #db.create_all()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.Text,
                        nullable=False)
    
    last_name = db.Column(db.Text,
                        nullable=False)
    
    image_url = db.Column(db.Text,
                        nullable=False,
                        default = DEFAULT_IMAGE_URL)
    

    def __repr__(self):
        u = self
        return f"<User id={u.id} first name={u.first_name} last name={u.last_name} profile pic={u.image_url}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.Text,
                      nullable=False,
                      default= "No Title Given")
    
    content = db.Column(db.Text,
                        nullable=False,
                        default = "No Content Given")
    
    created_at = db.Column(db.Text,
                           nullable=False,
                           default='2024-01-01 12:00:00')
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    
    user = db.relationship('User', backref=db.backref('posts', passive_deletes=True))