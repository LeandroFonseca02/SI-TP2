import re
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

from forms import CreateRideForm
from models.profile import Profile
from models.ride import Ride
from models.vehicle import Vehicle

rides = Blueprint('rides', __name__, template_folder='templates')


@rides.route('/rides')
@login_required
def rides_template():
    form = CreateRideForm()
    all_rides = Ride.get_all_rides()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('rides.html', rides=all_rides, page='Rides', form=form, profile=profile)


@rides.route('/createRide', methods=['POST'])
@login_required
def createRide():
    form = request.form
    Ride.create_ride_admin(id=form.get('id'), user_id=form.get('user_id'), vehicle_id=form.get('vehicle_id'),
                           date=form.get('date'),
                           hour=form.get('hour'), seats=form.get('seats'), status=form.get('status'),
                           origin=form.get('origin'), destination=form.get('destination'),
                           description=form.get('description'),
                           created_at=form.get('created_at'), updated_at=form.get('updated_at'))
    return redirect('/rides')


@rides.route('/editRide/<ride_id>', methods=['POST'])
@login_required
def update_ride(ride_id):
    form = request.form
    ride = Ride.get_ride_by_id(ride_id)
    Ride.edit_ride(ride=ride, id=form.get('id'), user_id=form.get('user_id'), vehicle_id=form.get('vehicle_id'),
                   date=form.get('date'),
                   hour=form.get('hour'), seats=form.get('seats'), status=form.get('status'),
                   origin=form.get('origin'), destination=form.get('destination'), description=form.get('description'),
                   created_at=form.get('created_at'), updated_at=form.get('updated_at'))
    return redirect('/rides')


@rides.route('/deleteride/<ride_id>', methods=['DELETE'])
@login_required
def delete_ride(ride_id):
    Ride.delete_ride_admin(ride_id)
    return redirect('/rides')


@rides.route('/getDeleteRideModal/<ride_id>', methods=['GET'])
@login_required
def get_delete_ride_modal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('delete-ride-modal.html', ride=ride)


@rides.route('/getEditRideModal/<ride_id>', methods=['GET'])
@login_required
def get_edit_ride_modal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    form = CreateRideForm(id=ride.id, user_id=ride.user_id, vehicle_id=ride.vehicle_id, date=ride.ride_date,
                          hour=ride.ride_hour, seats=ride.number_of_available_seats, status=ride.status, origin=ride.origin,
                          destination=ride.destination, description=ride.description, created_at=ride.created_at, updated_at=ride.updated_at)

    return render_template('edit-ride-modal.html', ride=ride, form=form)
