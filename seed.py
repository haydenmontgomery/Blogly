"""Seed file to make sample data for Users db."""

from models import User, Post, db, connect_db
from app import create_app

# Create all tables
app = create_app("blogly", testing=False)
#connect_db(app)
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add Users
alan = User(first_name='Alan', last_name='Alda', image_url='https://image.tmdb.org/t/p/original/jUuUbPuMGonFT5E2pcs4alfqaCN.jpg')
joel = User(first_name='Joel', last_name='Burton', image_url='https://akns-images.eonline.com/eol_images/Entire_Site/20161119/rs_634x951-161219055646-634.joel-mchale.121916.jpg?fit=around|634:951&output-quality=90&crop=634:951;center,top')
jane = User(first_name='Jane', last_name='Smith', image_url='https://images5.fanpop.com/image/photos/31900000/Jane-Seymour-poses-for-photgraphers-during-the-24th-MIPCOM-in-Cannes-jane-seymour-31964348-1468-2048.jpg')

# Add posts
p1 = Post(title="First Post!", content="Hey everyone!", created_at="2023-11-03 08:34:22", user_id=1)
p2 = Post(title="Does this work?", content="Checking if this works, thanks!", created_at="2023-11-05 11:02:42", user_id=2)
p3 = Post(title="Had a crazy dream today", content="Dreamt I was a piece of toast.", created_at="2023-12-03 13:04:40", user_id=3)
p4 = Post(title="Second Post!", content="Hey everyone! Just making a second post!", created_at="2023-12-11 04:54:02", user_id=1)
p5 = Post(title="Happy New Year!", content="Make some great resolutions!", created_at="2024-01-01 00:01:03", user_id=2)
p6 = Post(title="Joined a gym", content="Let's go!!", created_at="2024-01-03 14:20:22", user_id=3)

db.session.add_all([alan,joel,jane])
db.session.commit()
db.session.add_all([p1,p2,p3,p4,p5,p6])
# Commit--otherwise, this never gets saved!
db.session.commit()
