"""Seed file to make sample data for Users db."""

from models import User, db, connect_db
from app import create_app

# Create all tables
app = create_app("blogly", testing=False)
#connect_db(app)
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add Users
alan = User(first_name='Alan', last_name='Alda', image_url='https://image.tmdb.org/t/p/original/jUuUbPuMGonFT5E2pcs4alfqaCN.jpg')
joel = User(first_name='Joel', last_name='Burton', image_url='https://akns-images.eonline.com/eol_images/Entire_Site/20161119/rs_634x951-161219055646-634.joel-mchale.121916.jpg?fit=around|634:951&output-quality=90&crop=634:951;center,top')
jane = User(first_name='Jane', last_name='Smith', image_url='https://images5.fanpop.com/image/photos/31900000/Jane-Seymour-poses-for-photgraphers-during-the-24th-MIPCOM-in-Cannes-jane-seymour-31964348-1468-2048.jpg')

# Add new objects to session, so they'll persist
db.session.add(alan)
db.session.add(joel)
db.session.add(jane)

# Commit--otherwise, this never gets saved!
db.session.commit()
