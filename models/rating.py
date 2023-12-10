import datetime
import json
from dataclasses import dataclass

import jwt

from controllers.db import db
from models.profile import Profile


@dataclass
class Rating(db.Model):
    id: int
    user_id: int
    ride_id: int
    passenger_id: int
    rating: int
    created_at: str
    updated_at: str

    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    ride_id = db.Column('ride_id', db.ForeignKey('ride.id'))
    passenger_id = db.Column('passenger_id', db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    @staticmethod
    def add_rating(ride_id, user_id, passenger_id, rating):
        db.session.add(Rating(user_id=user_id, ride_id=ride_id, passenger_id=passenger_id, rating=rating,
                              created_at=datetime.datetime.utcnow()))
        db.session.commit()
        profile = Profile.get_profile(passenger_id)
        query = """
            SELECT AVG(rating) AS user_rating FROM rating
                WHERE passenger_id =""" + str(passenger_id)
        profile_rating = db.session.execute(query).first()
        profile.classification = profile_rating.user_rating
        db.session.commit()


    @staticmethod
    def get_rating_token(user_id, ride_id):
        with open('./config/config.json') as file:
            data = json.load(file)

        SECRET_KEY = data['SECRET_KEY']
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'user_id': user_id,
            'ride_id': ride_id
        }
        encoded_jwt = jwt.encode(
            payload,
            str(SECRET_KEY),
            algorithm='HS256'
        )

        return encoded_jwt

    @staticmethod
    def verify_rating_token(token):
        with open('./config/config.json') as file:
            data = json.load(file)

        SECRET_KEY = data['SECRET_KEY']
        try:
            jwt_token = jwt.decode(
                token,
                str(SECRET_KEY),
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None

        return {"user_id": jwt_token.get('user_id'), "ride_id": jwt_token.get('ride_id')}


    @staticmethod
    def check_ratings_exist(user_id, ride_id):
        ratings = db.session.query(Rating).filter(Rating.user_id == int(user_id), Rating.ride_id == int(ride_id)).all()
        if len(ratings) == 0:
            return False
        return True


    @staticmethod
    def get_all_ratings_admin():
        return db.session.query(Rating).all()

    @staticmethod
    def add_rating_admin(id, user_id, ride_id, passenger_id, rating, created_at, updated_at):
        if len(id) != 0:
            rating = Rating(id=int(id), user_id=int(user_id), ride_id=int(ride_id), passenger_id=int(passenger_id), rating=int(rating),
                                  created_at=datetime.datetime.utcnow())
        else:
            rating = Rating(user_id=int(user_id), ride_id=int(ride_id), passenger_id=int(passenger_id), rating=int(rating),
                            created_at=datetime.datetime.utcnow())
        db.session.add(rating)
        db.session.commit()

        if len(created_at) != 0:
            rating.created_at = created_at
        if len(updated_at) != 0:
            rating.updated_at = updated_at


        profile = Profile.get_profile(passenger_id)
        query = """
            SELECT AVG(rating) AS user_rating FROM rating
                WHERE passenger_id =""" + str(passenger_id)
        profile_rating = db.session.execute(query).first()
        profile.classification = profile_rating.user_rating
        db.session.commit()


    @staticmethod
    def get_rating_by_id(id):
        return db.session.query(Rating).filter(Rating.id == int(id)).first()

    @staticmethod
    def edit_rating_admin(rating_obj, id, user_id, ride_id, passenger_id, rating, created_at, updated_at):
        rating_obj.user_id = user_id
        rating_obj.ride_id = ride_id
        rating_obj.passenger_id = passenger_id
        rating_obj.rating = rating

        if len(id) != 0:
            rating_obj.id = id
        if len(created_at) != 0:
            rating_obj.created_at = created_at
        if len(updated_at) != 0:
            rating_obj.created_at = updated_at
        db.session.commit()


    @staticmethod
    def delete_rating_admin(id):
        db.session.query(Rating).filter(Rating.id == int(id)).delete()
        db.session.commit()