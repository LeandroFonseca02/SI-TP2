import os
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from config.config import UPLOAD_FOLDER
from forms import CreateProfileForm
from models.profile import Profile


profiles = Blueprint('profiles', __name__, template_folder='templates')


@profiles.route('/profiles')
@login_required
def profiles_template():
    form = CreateProfileForm()
    all_profiles = Profile.get_all_profiles()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('profile.html', profiles=all_profiles, page='Profiles', form=form, profile=profile)


@profiles.route('/createProfile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = CreateProfileForm()
    if form.is_submitted():
        f = request.files['photo']
        if f.content_length != 0:
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            Profile.create_profile_admin(form.id.data, form.user_id.data, form.first_name.data, form.last_name.data,
                                         form.registration_date.data, UPLOAD_FOLDER + filename, form.phone.data,
                                         form.classification.data)
        else:
            Profile.create_profile_admin(id=form.id.data, user_id=form.user_id.data, first_name=form.first_name.data, last_name=form.last_name.data,
                                         registration_date=form.registration_date.data, phone_number=form.phone.data,
                                         classification=form.classification.data, photo='../static/images/icons/profile-icon.svg')
        return redirect('/profiles')
    return render_template('modal_create.html', form=form)


@profiles.route('/getDeleteProfileModal/<profile_id>', methods=['GET'])
@login_required
def get_delete_user_modal(profile_id):
    profile = Profile.get_profile_by_id(profile_id)
    return render_template('delete-profile-modal.html', profile=profile)


@profiles.route('/getEditProfileModal/<profile_id>', methods=['GET'])
@login_required
def get_edit_profile_modal(profile_id):
    profile = Profile.get_profile_by_id(profile_id)
    form = CreateProfileForm(id=profile.id, user_id=profile.user_id, first_name=profile.first_name, last_name=profile.last_name, registration_date=profile.registration_date, phone=profile.phone_number, photo=profile.photo, classification=profile.classification)

    return render_template('edit-profile-modal.html', profile=profile, form=form)


@profiles.route('/editProfile/<id>', methods=['POST'])
@login_required
def update_user(id):
    form = request.form
    profile = Profile.get_profile_by_id(id)
    f = request.files['photo']
    if f.filename != '':
        filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, filename))
        photo = UPLOAD_FOLDER + filename
    else:
        photo = None

    Profile.edit_profile(profile=profile, profile_id=form.get('id'), user_id=form.get('user_id'), first_name=form.get('first_name'),
                                 last_name=form.get('last_name'),
                                 registration_date=form.get('registration_date'), phone_number=form.get('phone'),
                                 classification=form.get('classification'),
                                 photo=photo)
    return redirect('/profiles')


@profiles.route('/deleteprofile/<profile_id>', methods=['DELETE'])
@login_required
def delete_profile(profile_id):
    Profile.delete_user(profile_id)
    return redirect('/users')