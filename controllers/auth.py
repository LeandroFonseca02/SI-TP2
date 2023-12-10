from flask import render_template, Blueprint, redirect
from flask_login import login_required, current_user, logout_user, login_user, LoginManager
from werkzeug.security import check_password_hash

from forms import LoginForm
from models.role import Role
from models.user import User

auth = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(id):
    return User.get_user_by_id(id)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()

    if form.is_submitted():
        email = form.email.data
        password = form.password.data
        user = User.get_user_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                admin_id = Role.get_role_id_by_name('admin')
                if User.verify_user_has_role(user.id, admin_id):
                    login_user(user)
                    return redirect('/')
                else:
                    return "Sem Permissoes"
            else:
                return "Password Invalida"
        else:
            return "Este email nao pertence a nenhuma conta"
    else:
        return render_template('login.html',form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
