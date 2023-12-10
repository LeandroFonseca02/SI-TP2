import datetime
from dataclasses import dataclass
from controllers.db import db


@dataclass
class Profile(db.Model):
    id: int
    user_id: int
    first_name: str
    last_name: str
    registration_date: str
    photo: str
    phone_number: str
    classification: float

    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', backref='profile')
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    photo = db.Column(db.Text, default='../static/images/icons/profile-icon.svg')
    phone_number = db.Column(db.String(30), unique=True)
    classification = db.Column(db.Float(), db.CheckConstraint('classification >= 1 AND classification <= 5'),
                               default=2.5)

    def __str__(self):
        return self.first_name

    @staticmethod
    def get_all_profiles():
        return db.session.query(Profile).all()

    @staticmethod
    def create_profile(user_id, first_name, last_name, phone_number):
        profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name, phone_number=phone_number)
        db.session.add(profile)
        db.session.commit()


    @staticmethod
    def create_profile_admin(id, user_id, first_name, last_name, registration_date, photo, phone_number, classification):
        if classification is None:
            classification = 2.5
        profile = Profile(user_id=int(user_id), first_name=first_name, last_name=last_name,
                          phone_number=phone_number, classification=classification)
        if id is not None:
            profile.id = int(id)
        if registration_date is not None:
            profile.registration_date = registration_date



        db.session.add(profile)
        db.session.commit()
        if photo is not None:
            Profile.update_photo(int(user_id), photo)


    @staticmethod
    def get_profile(user_id):
        return db.session.query(Profile).filter(Profile.user_id == user_id).first()

    @staticmethod
    def get_profile_by_id(id):
        return db.session.query(Profile).filter(Profile.id == int(id)).first()

    @staticmethod
    def delete_user(id):
        db.session.query(Profile).filter(Profile.id == int(id)).delete()
        db.session.commit()

    @staticmethod
    def edit_profile(profile, profile_id, user_id, first_name, last_name, registration_date, photo, phone_number, classification):
        profile.id = int(profile_id)
        profile.user_id = user_id
        profile.first_name = first_name
        profile.last_name = last_name
        profile.registration_date = registration_date
        profile.phone_number = phone_number
        profile.classification = classification
        if photo is not None:
            profile.photo = photo
        db.session.commit()

    @staticmethod
    def update_photo(user_id, photo):
        profile = Profile.get_profile(user_id)
        profile.photo = photo
        db.session.commit()

    @staticmethod
    def update_name_phone(user_id, first_name, last_name, phone):
        profile = Profile.get_profile(user_id)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.phone_number = phone
        db.session.commit()


    # def __init__(self, user_id, first_name, last_name, registration_date, photo, phone_number, classification):
    #     self.user_id = user_id
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.registration_date = registration_date
    #     self.photo = photo
    #     self.phone_number = phone_number
    #     self.classification = classification