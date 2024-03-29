import datetime
from dataclasses import dataclass

from controllers.db import db


@dataclass
class Vehicle(db.Model):
    id: int
    user_id: int
    license_plate: str
    color: str
    is_deleted: bool
    brand: str
    model: str
    created_at: str
    updated_at: str

    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='vehicle')
    license_plate = db.Column(db.String(20), unique=True)
    color = db.Column(db.String(20))
    brand = db.Column(db.String(50))
    model = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    @staticmethod
    def get_all_vehicles():
        return db.session.query(Vehicle).all()

    @staticmethod
    def get_vehicles_by_userid(user_id):
        return db.session.query(Vehicle).filter(Vehicle.user_id == user_id, Vehicle.is_deleted == False).all()

    @staticmethod
    def get_vehicle_by_id(id):
        return db.session.query(Vehicle).filter(Vehicle.id == id, Vehicle.is_deleted == False).first()

    @staticmethod
    def get_vehicle_by_id_admin(id):
        return db.session.query(Vehicle).filter(Vehicle.id == id).first()

    @staticmethod
    def create_vehicle(user_id, brand, model, color, license_plate):
        vehicle = Vehicle(user_id=user_id, license_plate=license_plate, color=color, brand=brand, model=model)
        db.session.add(vehicle)
        db.session.commit()

    @staticmethod
    def create_vehicle_admin(id, user_id, brand, model, color, license_plate, is_deleted, created_at, updated_at):
        vehicle = Vehicle(user_id=int(user_id), license_plate=license_plate, color=color, brand=brand, model=model, is_deleted=eval(is_deleted))
        if len(created_at) != 0:
            vehicle.created_at = created_at
        if len(updated_at) != 0:
            vehicle.updated_at = updated_at
        if len(id) != 0:
            vehicle.id = id
        db.session.add(vehicle)
        db.session.commit()

    @staticmethod
    def delete_vehicle(vehicle_id):
        vehicle = Vehicle.get_vehicle_by_id(int(vehicle_id))
        vehicle.is_deleted = True
        db.session.commit()

    @staticmethod
    def delete_vehicle_admin(vehicle_id):
        db.session.query(Vehicle).filter(Vehicle.id == vehicle_id).delete()
        db.session.commit()

    @staticmethod
    def get_vehicle_id_by_license_plate(license_plate):
        vehicle = db.session.query(Vehicle).filter(Vehicle.license_plate == license_plate).first()
        return vehicle.id


    @staticmethod
    def edit_vehicle(vehicle, id, user_id, license_plate, brand, model, color, is_deleted, created_at, update_at):
        vehicle.id = id
        vehicle.user_id = user_id
        vehicle.license_plate = license_plate
        vehicle.brand = brand
        vehicle.model = model
        vehicle.color = color
        vehicle.is_deleted = eval(is_deleted)
        vehicle.created_at = created_at
        vehicle.updated_at = update_at
        db.session.commit()

    # def __init__(self, user_id, license_plate, color, is_deleted, brand, model, created_at, updated_at):
    #     self.user_id = user_id
    #     self.license_plate = license_plate
    #     self.color = color
    #     self.is_deleted = is_deleted
    #     self.brand = brand
    #     self.model = model
    #     self.created_at = created_at
    #     self.updated_at = updated_at
