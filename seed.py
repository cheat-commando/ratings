"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Movie, Rating
from datetime import datetime

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        movie_id, raw_title, released_at, _, chunk = row.split('|', 4)
        title = raw_title[:-7]
        imdb_url, _ = chunk.split('|', 1)

        movie = Movie(movie_id=movie_id,
                        title=title,
                        released_at=datetime.strptime(released_at,'%d-%b-%Y'),
                        imdb_url=imdb_url)
        
        db.session.add(movie)
    
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, movie_id, score, _ = row.split()
        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.session.add(rating)

    db.session.commit()





def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_movie_id():
    result = db.session.query(func.max(Movie.movie_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('movies_movie_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_rating_id():
    result = db.session.query(func.max(Rating.rating_id)).one()
    max_id = int(result[0])
    query = "SELECT setval('ratings_rating_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
    # set_val_movie_id()
    # set_val_rating_id()
