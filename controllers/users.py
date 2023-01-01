from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from forms import CreateUserForm, EditUserForm
from models.profile import Profile
from models.user import User

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/users')
@login_required
def users_template():
    form = CreateUserForm()
    all_users = User.get_all_users()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('user.html', users=all_users, page='Users', form=form, profile=profile)


@users.route('/createUser', methods=['POST'])
@login_required
def create_user():
    form = CreateUserForm()
    if form.is_submitted():
        User.create_user_admin(form.id.data, form.email.data,
                               generate_password_hash(form.password.data, method='sha256'), form.active.data)
    return redirect('/users')



@users.route('/getDeleteUserModal/<user_id>', methods=['GET'])
@login_required
def get_delete_user_modal(user_id):
    user = User.get_user_by_id(user_id)
    return render_template('delete-user-modal.html', user=user)

@users.route('/getEditUserModal/<user_id>', methods=['GET'])
@login_required
def get_edit_user_modal(user_id):
    user = User.get_user_by_id(user_id)
    form = EditUserForm(id=user.id, email=user.email, password=user.password, active=user.active)

    return render_template('edit-user-modal.html', user=user, form=form)

@users.route('/deleteuser/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    User.delete_user(user_id)
    return redirect('/users')

@users.route('/updateuserstable')
@login_required
def update_users():
    all_users = User.get_all_users()
    return render_template('tables.html', users=all_users, page='Users')


@users.route('/editUser/<user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    form = request.form
    user = User.get_user_by_id(user_id)
    User.edit_user(user, form.get('id'), form.get('email'), generate_password_hash(form.get('password'), method='sha256') , form.get('active'))
    return redirect('/users')
