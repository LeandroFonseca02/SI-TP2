from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, current_user

from forms import CreateReservationForm
from models.profile import Profile
from models.reservation import Reservation

reservations = Blueprint('reservations', __name__, template_folder='templates')


@reservations.route('/reservations')
@login_required
def reservations_template():
    form = CreateReservationForm()
    all_reservations = Reservation.get_all_reservations()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('reservation.html', reservations=all_reservations, page='Reservations', form=form, profile=profile)


@reservations.route('/createReservation', methods=['POST'])
@login_required
def createReservation():
    form = request.form
    Reservation.create_reservation_admin(id=form.get('id'), user_id=form.get('user_id'), ride_id=form.get('ride_id'),
                                         status=form.get('status'),
                                         is_driver=form.get('is_driver'),
                                         created_at=form.get('created_at'), updated_at=form.get('updated_at'))
    return redirect('/reservations')


@reservations.route('/editReservation/<reservation_id>', methods=['POST'])
@login_required
def update_reservation(reservation_id):
    form = request.form
    reservation = Reservation.get_reservation_by_id(reservation_id)
    Reservation.edit_reservation_admin(reservation=reservation, id=form.get('id'), user_id=form.get('user_id'), ride_id=form.get('ride_id'),
                                       status=form.get('status'),
                                       is_driver=form.get('is_driver'),
                                       created_at=form.get('created_at'), updated_at=form.get('updated_at'))
    return redirect('/reservations')


@reservations.route('/deletereservation/<reservation_id>', methods=['DELETE'])
@login_required
def delete_reservation(reservation_id):
    Reservation.delete_reservation_admin(reservation_id)
    return redirect('/reservations')


@reservations.route('/getDeleteReservationModal/<reservation_id>', methods=['GET'])
@login_required
def get_delete_reservation_modal(reservation_id):
    reservation = Reservation.get_reservation_by_id(reservation_id)
    return render_template('delete-reservation-modal.html', reservation=reservation)


@reservations.route('/getEditReservationModal/<reservation_id>', methods=['GET'])
@login_required
def get_edit_reservation_modal(reservation_id):
    reservation = Reservation.get_reservation_by_id(reservation_id)
    form = CreateReservationForm(id=reservation.id, user_id=reservation.user_id, ride_id=reservation.ride_id,
                          status=reservation.status,
                          is_driver=reservation.is_driver,
                          created_at=reservation.created_at,
                          updated_at=reservation.updated_at)

    return render_template('edit-reservation-modal.html', reservation=reservation, form=form)
