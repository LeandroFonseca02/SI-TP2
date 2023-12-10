import datetime
from dataclasses import dataclass

from controllers.db import db
from models.reservation import Reservation


@dataclass
class Ride(db.Model):
    id: int
    user_id: int
    vehicle_id: int
    ride_date: str
    ride_hour: str
    number_of_available_seats: int
    status: str
    origin: str
    destination: str
    description: str
    created_at: str
    updated_at: str

    __tablename__ = 'ride'
    __table_args__ = (db.UniqueConstraint('user_id', 'vehicle_id', 'ride_date', 'ride_hour'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='ride')
    vehicle_id = db.Column('vehicle_id', db.ForeignKey('vehicle.id'))
    vehicle = db.relationship('Vehicle', backref='ride')
    ride_date = db.Column(db.Date)
    ride_hour = db.Column(db.Time)
    number_of_available_seats = db.Column(db.Integer())
    status = db.Column(db.String(50), default='Aberta')
    origin = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    description = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)


    @staticmethod
    def get_all_rides():
        return db.session.query(Ride).all()


    @staticmethod
    def get_index_rides(user_id):
        query = """
        
        SELECT DISTINCT r.id,
                        rs.user_id,
                        to_char(r.ride_date, 'MM') AS ride_date_month,
                        to_char(r.ride_date, 'DD') AS ride_date_day,
                        to_char(r.ride_hour, 'HH') AS ride_hours,
                        to_char(r.ride_hour, 'MI') AS ride_minutes,
                        r.number_of_available_seats,
                        r.status,
                        r.origin,
                        r.destination,
                        rs.is_driver
        FROM ride AS r,reservation rs
        WHERE r.status = 'Aberta'
          AND rs.ride_id = r.id
          AND rs.is_driver = TRUE
          AND r.id NOT IN (
                SELECT DISTINCT r.id
                FROM ride AS r
                    INNER JOIN reservation rs ON r.id = rs.ride_id
                WHERE rs.user_id =""" + str(user_id) + """)"""

        return db.session.execute(query).all()


    @staticmethod
    def get_ride_passengers(ride_id):
        query = """
        SELECT u.id AS user_id,
        email,
        first_name,
        last_name,
        photo,
        phone_number,
        classification
        FROM "user" AS u
             JOIN profile p ON u.id = p.user_id
             JOIN reservation r ON u.id = r.user_id
             JOIN ride r2 ON r2.id = r.ride_id
        WHERE r.status = 'Aberta' AND r2.id =
        """ + ride_id

        return db.session.execute(query).all()

    @staticmethod
    def get_ride_by_id(ride_id):
        return db.session.query(Ride).filter(Ride.id == int(ride_id)).first()

    @staticmethod
    def create_ride(ride):
        db.session.add(ride)
        db.session.commit()
        Reservation.create_reservation(Reservation(user_id=ride.user_id, ride_id=ride.id, is_driver=True))


    @staticmethod
    def get_active_rides(user_id):
        query = """
            SELECT r.id,
               r.user_id,
               to_char(r.ride_date, 'MM') AS ride_date_month,
               to_char(r.ride_date, 'DD') AS ride_date_day,
               to_char(r.ride_hour, 'HH') AS ride_hours,
               to_char(r.ride_hour, 'MI') AS ride_minutes,
               r.number_of_available_seats,
               r.status,
               r.origin,
               r.destination
            FROM ride AS r
            WHERE (r.status = 'Aberta' OR r.status = 'Confirmada')
            AND r.user_id =""" + str(user_id)
        return db.session.execute(query).all()


    @staticmethod
    def get_historic_rides(user_id):
        query = """
            SELECT r.id,
               r.user_id,
               to_char(r.ride_date, 'MM') AS ride_date_month,
               to_char(r.ride_date, 'DD') AS ride_date_day,
               to_char(r.ride_hour, 'HH') AS ride_hours,
               to_char(r.ride_hour, 'MI') AS ride_minutes,
               r.number_of_available_seats,
               r.status,
               r.origin,
               r.destination
            FROM ride AS r
            WHERE (r.status = 'Concluida' OR r.status = 'Cancelada')
              AND r.user_id =""" + str(user_id)
        return db.session.execute(query).all()


    @staticmethod
    def create_ride_admin(id, user_id, vehicle_id, date, hour, seats, status, origin, destination, description, created_at, updated_at):
        ride = Ride(user_id=int(user_id), vehicle_id=int(vehicle_id), ride_date=date, ride_hour=hour, number_of_available_seats=int(seats), status=status, origin=origin, destination=destination, description=description)
        if len(id) != 0:
            ride.id = id
        if len(created_at) != 0:
            ride.created_at = created_at
        if len(updated_at) != 0:
            ride.updated_at = updated_at
        db.session.add(ride)
        db.session.commit()

    @staticmethod
    def delete_ride_admin(ride_id):
        db.session.query(Ride).filter(Ride.id == int(ride_id)).delete()
        db.session.commit()

    @staticmethod
    def edit_ride(ride, id, user_id, vehicle_id, date, hour, seats, status, origin, destination, description, created_at, updated_at):
        ride.id = id
        ride.user_id = user_id
        ride.vehicle_id = vehicle_id
        ride.ride_date = date
        ride.ride_hour = hour
        ride.number_of_available_seats = seats
        ride.status = status
        ride.origin = origin
        ride.description = destination
        ride.description = description
        ride.created_at = created_at
        ride.updated_at = updated_at
        db.session.commit()


    @staticmethod
    def get_number_all_rides():
        return len(db.session.query(Ride).all())

    @staticmethod
    def get_number_completed_rides():
        return len(db.session.query(Ride).filter(Ride.status == 'Concluida').all())
        # def __init__(self, user_id, vehicle_id, ride_date, number_of_available_seats, status, origin, destination,
        #              created_at, updated_at):
        #     self.user_id = user_id
        #     self.vehicle_id = vehicle_id
        #     self.ride_date = ride_date
        #     self.number_of_available_seats = number_of_available_seats
        #     self.status = status
        #     self.origin = origin
        #     self.destination = destination
        #     self.created_at = created_at
        #     self.updated_at = updated_at