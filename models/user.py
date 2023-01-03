import datetime
import json
from dataclasses import dataclass
import jwt
from flask_security import UserMixin

from controllers.db import db
from models.role import roles_users_table, Role


@dataclass
class User(db.Model, UserMixin):
    id: int
    email: str
    password: str
    active: bool
    roles: str

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.Unicode(255))
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship(
        "Role", secondary=roles_users_table, backref="user", lazy=True
    )

    @staticmethod
    def get_all_users():
        return db.session.query(User).all()

    @staticmethod
    def get_user_by_email(email):
        return db.session.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(id):
        return db.session.query(User).filter(User.id == id).first()

    @staticmethod
    def update_email(id, email):
        user = User.get_user_by_id(id)
        user.email = email
        db.session.commit()

    @staticmethod
    def update_password(id, password):
        user = User.get_user_by_id(id)
        user.password = password
        db.session.commit()

    @staticmethod
    def create_user(email, password):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def create_user_admin(id, email, password, active):
        if id is None:
            user = User(email=email, password=password, active=eval(active))
        else:
            user = User(id=id, email=email, password=password, active=eval(active))
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def edit_user(user, id, email, password, active):
        user.id = int(id)
        user.email = email
        user.password = password
        user.active = eval(active)
        db.session.commit()

    @staticmethod
    def delete_user(id):
        db.session.query(User).filter(User.id == int(id)).delete()
        db.session.commit()

    def has_role(self, role):
        query = db.session.query(Role).filter(Role.name == role).first()
        if query:
            if query.name in self.roles:
                return True
        return False

    def __str__(self):
        return self.email

    def get_reset_token(self, expire_sec=1800):
        with open('./config/config.json') as file:
            data = json.load(file)

        SECRET_KEY = data['SECRET_KEY']
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expire_sec),
            'iat': datetime.datetime.utcnow(),
            'user_id': self.id
        }
        encoded_jwt = jwt.encode(
            payload,
            str(SECRET_KEY),
            algorithm='HS256'
        )

        return encoded_jwt

    @staticmethod
    def verify_reset_token(token):
        try:
            with open('./config/config.json') as file:
                data = json.load(file)

            SECRET_KEY = data['SECRET_KEY']
            data = jwt.decode(
                token,
                str(SECRET_KEY),
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return None

        return data.get('user_id')

    @staticmethod
    def add_role(user_id, role_id):
        query = "INSERT INTO role_user VALUES (" + user_id + ", " + role_id + ")"
        db.session.execute(query)
        db.session.commit()

    @staticmethod
    def get_number_users():
        return len(db.session.query(User).all())

    @staticmethod
    def delete_role_to_user(user_id, role_id):
        query = "DELETE FROM role_user WHERE user_id = " + user_id + " AND role_id = " + role_id
        db.session.execute(query)
        db.session.commit()

    @staticmethod
    def verify_user_has_role(user_id, role_id):
        query = "SELECT * FROM role_user WHERE user_id = " + str(user_id) + " AND role_id = " + str(role_id)
        checker = db.session.execute(query)
        if checker.rowcount == 0:
            return False
        else:
            return True