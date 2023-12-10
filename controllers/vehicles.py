from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from forms import CreateVehicleForm
from models.profile import Profile
from models.vehicle import Vehicle

vehicles = Blueprint('vehicles', __name__, template_folder='templates')


@vehicles.route('/vehicles')
@login_required
def vehicles_template():
    all_vehicles = Vehicle.get_all_vehicles()
    form = CreateVehicleForm()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('vehicle.html', vehicles=all_vehicles, page='Vehicles', form=form, profile=profile)


@vehicles.route('/createVehicle', methods=['POST'])
@login_required
def createVehicle():
    form = request.form
    Vehicle.create_vehicle_admin(id=form.get('id'), user_id=form.get('user_id'), brand=form.get('brand'), model=form.get('model'),
                                 color=form.get('color'), license_plate=form.get('license_plate'), is_deleted=form.get('is_deleted'),
                                 created_at=form.get('created_at'), updated_at=form.get('updated_at'))
    return redirect('/vehicles')


@vehicles.route('/editVehicle/<vehicle_id>', methods=['POST'])
@login_required
def update_vehicle(vehicle_id):
    form = request.form
    vehicle = Vehicle.get_vehicle_by_id_admin(vehicle_id)
    Vehicle.edit_vehicle(vehicle, form.get('id'), form.get('user_id'), form.get('license_plate'), form.get('brand'), form.get('model'), form.get('color'), form.get('is_deleted'), form.get('created_at'), form.get('updated_at'))
    return redirect('/vehicles')


@vehicles.route('/deletevehicle/<vehicle_id>', methods=['DELETE'])
@login_required
def delete_vehicle(vehicle_id):
    Vehicle.delete_vehicle_admin(vehicle_id)
    return redirect('/vehicles')


@vehicles.route('/getDeleteVehicleModal/<vehicle_id>', methods=['GET'])
@login_required
def get_delete_vehicle_modal(vehicle_id):
    vehicle = Vehicle.get_vehicle_by_id_admin(vehicle_id)
    return render_template('delete-vehicle-modal.html', vehicle=vehicle)

@vehicles.route('/getEditVehicleModal/<vehicle_id>', methods=['GET'])
@login_required
def get_edit_profile_modal(vehicle_id):
    vehicle = Vehicle.get_vehicle_by_id_admin(vehicle_id)
    form = CreateVehicleForm(id=vehicle.id, user_id=vehicle.user_id, license_plate=vehicle.license_plate, brand=vehicle.brand, model=vehicle.model, color=vehicle.color, is_deleted=vehicle.is_deleted, created_at=vehicle.created_at, updated_at=vehicle.updated_at)

    return render_template('edit-vehicle-modal.html', vehicle=vehicle, form=form)