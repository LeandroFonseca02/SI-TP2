from dataclasses import dataclass
from flask_security import RoleMixin
from controllers.db import db

roles_users_table = db.Table(
    "role_user",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

@dataclass
class Role(db.Model, RoleMixin):
    id: int
    name: str
    description: str

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @staticmethod
    def get_all_roles():
        return db.session.query(Role).all()

    @staticmethod
    def get_all_users_roles():
        return db.session.query(roles_users_table).all()

    @staticmethod
    def create_role_admin(id, name, description):
        role = Role(name=name, description=description)
        if len(id) != 0:
            role.id = int(id)
        db.session.add(role)
        db.session.commit()

    @staticmethod
    def edit_role_admin(role, id, name, description):
        role.id = int(id)
        role.name = name
        role.description = description
        db.session.commit()

    @staticmethod
    def delete_role_admin(id):
        db.session.query(Role).filter(Role.id == int(id)).delete()
        db.session.commit()

    @staticmethod
    def get_role_by_id(id):
        return db.session.query(Role).filter(Role.id == int(id)).first()



