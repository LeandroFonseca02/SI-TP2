from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from forms import CreateRoleForm, CreateUserRoleForm
from models.profile import Profile
from models.role import Role
from models.user import User

roles = Blueprint('roles', __name__, template_folder='templates')


@roles.route('/roles')
@login_required
def roles_template():
    form = CreateRoleForm()
    all_roles = Role.get_all_roles()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('role.html', roles=all_roles, page='Roles', form=form, profile=profile)


@roles.route('/role_user')
@login_required
def role_user_template():
    form = CreateUserRoleForm()
    all_users_roles = Role.get_all_users_roles()
    profile = Profile.get_profile_by_id(current_user.id)
    return render_template('role-user.html', user_roles=all_users_roles, page='User Roles', form=form, profile=profile)

@roles.route('/createRole', methods=['POST'])
@login_required
def createRole():
    form = request.form
    Role.create_role_admin(id=form.get('id'), name=form.get('name'),
                           description=form.get('description'),)
    return redirect('/roles')


@roles.route('/editRole/<role_id>', methods=['POST'])
@login_required
def update_role(role_id):
    form = request.form
    role = Role.get_role_by_id(role_id)
    Role.edit_role_admin(role=role, id=form.get('id'), name=form.get('name'), description=form.get('description'))
    return redirect('/roles')


@roles.route('/deleterole/<role_id>', methods=['DELETE'])
@login_required
def delete_role(role_id):
    Role.delete_role_admin(role_id)
    return redirect('/roles')


@roles.route('/getDeleteRoleModal/<role_id>', methods=['GET'])
@login_required
def get_delete_role_modal(role_id):
    role = Role.get_role_by_id(role_id)
    return render_template('delete-role-modal.html', role=role)


@roles.route('/getEditRoleModal/<role_id>', methods=['GET'])
@login_required
def get_edit_role_modal(role_id):
    role = Role.get_role_by_id(role_id)
    form = CreateRoleForm(id=role.id, name=role.name, description=role.description)

    return render_template('edit-role-modal.html', role=role, form=form)


@roles.route('/createRoleUser', methods=['POST'])
@login_required
def createRoleUser():
    form = request.form
    User.add_role(user_id=form.get('user_id'), role_id=form.get('role_id'))
    return redirect('/role_user')


@roles.route('/editRoleUser/<user_id>/<role_id>', methods=['POST'])
@login_required
def update_roleuser(user_id, role_id):
    form = request.form
    User.delete_role_to_user(user_id, role_id)
    User.add_role(form.get('user_id'), form.get('role_id'))
    return redirect('/role_user')


@roles.route('/deleteroleuser/<user_id>/<role_id>', methods=['DELETE'])
@login_required
def delete_roleuser(user_id, role_id):
    User.delete_role_to_user(user_id, role_id)
    return redirect('/role_user')


@roles.route('/getDeleteRoleUserModal/<user_id>/<role_id>', methods=['GET'])
@login_required
def get_delete_roleuser_modal(user_id, role_id):
    return render_template('delete-roleuser-modal.html', role_id=role_id, user_id=user_id)


@roles.route('/getEditRoleUserModal/<user_id>/<role_id>', methods=['GET'])
@login_required
def get_edit_roleuser_modal(user_id, role_id):
    form = CreateUserRoleForm(user_id=user_id, role_id=role_id)

    return render_template('edit-roleuser-modal.html', role_id=role_id, user_id=user_id, form=form)