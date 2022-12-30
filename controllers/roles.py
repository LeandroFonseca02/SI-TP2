from flask import Blueprint, render_template

from models.role import Role

roles = Blueprint('roles', __name__, template_folder='templates')


@roles.route('/roles')
def roles_template():
    all_roles = Role.get_all_roles()
    return render_template('role.html', roles=all_roles)


@roles.route('/role_user')
def role_user_template():
    all_users_roles = Role.get_all_users_roles()
    return render_template('role-user.html', user_roles=all_users_roles)