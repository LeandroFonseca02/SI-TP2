from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from forms import CreateUserForm, EditUserForm
from models.user import User

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/users')
def users_template():
    form = CreateUserForm()
    all_users = User.get_all_users()
    return render_template('user.html', users=all_users, page='Users', form=form)


@users.route('/createUser', methods=['POST'])
def create_user():
    form = CreateUserForm()
    if form.is_submitted():
        User.create_user_admin(form.id.data, form.email.data,
                               generate_password_hash(form.password.data, method='sha256'), form.active.data)
    return redirect('/users')



@users.route('/getDeleteUserModal/<user_id>', methods=['GET'])
def get_delete_user_modal(user_id):
    user = User.get_user_by_id(user_id)
    return render_template('delete-user-modal.html', user=user)

@users.route('/getEditUserModal/<user_id>', methods=['GET'])
def get_edit_user_modal(user_id):
    user = User.get_user_by_id(user_id)
    form = EditUserForm(id=user.id, email=user.email, password=user.password, active=user.active)

    return render_template('edit-user-modal.html', user=user, form=form)

@users.route('/deleteuser/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.delete_user(user_id)
    return redirect('/users')

@users.route('/updateuserstable')
def update_users():
    all_users = User.get_all_users()
    return render_template('tables.html', users=all_users, page='Users')


@users.route('/editUser/<user_id>', methods=['POST'])
def update_user(user_id):
    form = request.form
    user = User.get_user_by_id(user_id)
    User.edit_user(user, form.get('id'), form.get('email'), generate_password_hash(form.get('password'), method='sha256') , form.get('active'))
    all_users = User.get_all_users()
    return redirect('/users')

@users.route('/updatePassword', methods=['POST'])
@login_required
def updatePassword():
    if request.method == 'POST':
        password = request.form.get('password')
        newPassword = request.form.get('newPassword')
        passwordConfirmation = request.form.get('passwordConfirmation')
        user = User.get_user_by_id(current_user.id)

        if check_password_hash(user.password, password):
            if newPassword == passwordConfirmation:
                User.update_password(current_user.id, generate_password_hash(newPassword, method='sha256'))
                return redirect("/profile")
            else:
                return "password desigual"
        else:
            return "password incorreta"
