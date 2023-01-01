import re
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user

from forms import CreateRideForm
from models.profile import Profile
from models.ride import Ride
from models.vehicle import Vehicle

rides = Blueprint('rides', __name__, template_folder='templates')


@rides.route('/rides')
def rides_template():
    form = CreateRideForm()
    all_rides = Ride.get_all_rides()
    return render_template('rides.html', rides=all_rides, page='Rides', form=form)


# @rides.route('/createRide', methods=['POST'])
# @login_required
# def create_ride():
#     if request.method == 'POST':
#         car = request.form.get('car')
#         origin = request.form.get('origin')
#         destination = request.form.get('destination')
#         date = request.form.get('date')
#         hour = request.form.get('hour')
#         description = request.form.get('description')
#         available_seats = request.form.get('availableSeats')
#         license_plate = re.findall(r"(?<=\()(.*?)(?=\))", car)
#         vehicle_id = Vehicle.get_vehicle_id_by_license_plate(license_plate[0])
#         Ride.create_ride(Ride(vehicle_id=vehicle_id, user_id=current_user.id, ride_date=date, ride_hour=hour,
#                         number_of_available_seats=available_seats, origin=origin, destination=destination, description=description))
#         return redirect('/')


@rides.route('/getRideData/<ride_id>/<card_type>', methods=['GET'])
@login_required
def getRideData(ride_id, card_type):
    passengers = Ride.get_ride_passengers(ride_id)
    ride = Ride.get_ride_by_id(ride_id)
    vehicle = Vehicle.get_vehicle_by_id(ride.vehicle_id)
    return render_template('card-content.html', passengers=passengers, ride=ride, vehicle=vehicle, card_type=card_type)


@rides.route('/minhasBoleias', methods=['GET'])
@login_required
def minhasBoleias():
    profile = Profile.get_profile(current_user.id)
    boleias = Ride.get_active_rides(current_user.id)
    historicos = Ride.get_historic_rides(current_user.id)
    return render_template('minhasBoleias.html', profile=profile, boleias=boleias, historicos=historicos)


@rides.route('/createRide', methods=['POST'])
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
def delete_ride(ride_id):
    Ride.delete_ride_admin(ride_id)
    return redirect('/rides')


@rides.route('/getDeleteRideModal/<ride_id>', methods=['GET'])
def get_delete_ride_modal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    return render_template('delete-ride-modal.html', ride=ride)


@rides.route('/getEditRideModal/<ride_id>', methods=['GET'])
def get_edit_ride_modal(ride_id):
    ride = Ride.get_ride_by_id(ride_id)
    form = CreateRideForm(id=ride.id, user_id=ride.user_id, vehicle_id=ride.vehicle_id, date=ride.ride_date,
                          hour=ride.ride_hour, seats=ride.number_of_available_seats, status=ride.status, origin=ride.origin,
                          destination=ride.destination, description=ride.description, created_at=ride.created_at, updated_at=ride.updated_at)

    return render_template('edit-ride-modal.html', ride=ride, form=form)
