import datetime
from dataclasses import dataclass
from controllers.db import db


@dataclass
class Reservation(db.Model):
    id: int
    user_id: int
    ride_id: int
    status: str
    is_driver: bool
    created_at: str
    updated_at: str

    __tablename__ = 'reservation'
    __table_args__ = (db.UniqueConstraint('user_id', 'ride_id'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reservation')
    ride_id = db.Column('ride_id', db.ForeignKey('ride.id'))
    ride = db.relationship('Ride', backref='reservation')
    status = db.Column(db.String(50), default='Aberta')
    is_driver = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)


    @staticmethod
    def get_all_reservations():
        return db.session.query(Reservation).all()


    @staticmethod
    def create_reservation(reservation):
        db.session.add(reservation)
        db.session.commit()

    @staticmethod
    def get_active_reservations(user_id):
        query = """
            SELECT r.id,
               r.user_id,
               to_char(r.ride_date, 'MM') AS ride_date_month,
               to_char(r.ride_date, 'DD') AS ride_date_day,
               to_char(r.ride_hour, 'HH') AS ride_hours,
               to_char(r.ride_hour, 'MI') AS ride_minutes,
               r.number_of_available_seats,
               rs.status,
               r.origin,
               r.destination
            FROM ride AS r,
                 reservation AS rs
            WHERE (rs.status = 'Aberta' OR rs.status = 'Confirmada')
              AND rs.ride_id = r.id
              AND rs.is_driver = FALSE
              AND rs.user_id = """ + str(user_id)
        return db.session.execute(query).all()


    @staticmethod
    def get_historic_reservations(user_id):
        query = """
                SELECT r.id,
                   r.user_id,
                   to_char(r.ride_date, 'MM') AS ride_date_month,
                   to_char(r.ride_date, 'DD') AS ride_date_day,
                   to_char(r.ride_hour, 'HH') AS ride_hours,
                   to_char(r.ride_hour, 'MI') AS ride_minutes,
                   r.number_of_available_seats,
                   rs.status,
                   r.origin,
                   r.destination
                FROM ride AS r,
                     reservation AS rs
                WHERE (rs.status = 'Concluida' OR rs.status = 'Cancelada')
                  AND rs.ride_id = r.id
                  AND rs.is_driver = FALSE
                  AND rs.user_id =""" + str(user_id)
        return db.session.execute(query).all()


    @staticmethod
    def cancel_reservation(ride_id, user_id):
        reservation = db.session.query(Reservation).filter(Reservation.ride_id == int(ride_id),
                                                           Reservation.user_id == user_id).first()
        reservation.status = 'Cancelada'
        db.session.commit()


    @staticmethod
    def create_reservation_admin(id, user_id, ride_id, status, is_driver, created_at, updated_at):
        reservation = Reservation(user_id=user_id, ride_id=ride_id, status=status, is_driver=eval(is_driver))
        if len(id) != 0:
            reservation.id = id
        if len(created_at) != 0:
            reservation.created_at = created_at
        if len(updated_at) != 0:
            reservation.updated_at = updated_at

        db.session.add(reservation)
        db.session.commit()


    @staticmethod
    def delete_reservation_admin(id):
        db.session.query(Reservation).filter(Reservation.id == int(id)).delete()
        db.session.commit()


    @staticmethod
    def edit_reservation_admin(reservation, id, user_id, ride_id, status, is_driver, created_at, updated_at):
        reservation.id = int(id)
        reservation.user_id = int(user_id)
        reservation.ride_id = int(ride_id)
        reservation.status = status
        reservation.is_driver = eval(is_driver)
        reservation.created_at = created_at
        reservation.updated_at = updated_at
        db.session.commit()


    @staticmethod
    def get_reservation_by_id(id):
        return db.session.query(Reservation).filter(Reservation.id == int(id)).first()


    @staticmethod
    def get_number_reservations():
        return len(db.session.query(Reservation).all())

    # def __init__(self, user_id, ride_id, created_at, updated_at):
    #     self.user_id = user_id
    #     self.ride_id = ride_id
    #     self.created_at = created_at
    #     self.updated_at = updated_at
