from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, EmailField, ValidationError, IntegerField, SelectField, DateTimeField, \
    FileField, DecimalField
from wtforms.validators import InputRequired, Length, Optional, NumberRange
from models.user import User


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    phone = StringField('Telemóvel', validators=[InputRequired(), Length(min=9, max=30)])
    first_name = StringField('Nome Próprio', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Apelido', validators=[InputRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])


class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])

    def validate_email(self, email):
        user = User.get_user_by_email(email)
        if user is None:
            raise ValidationError('Não existe nenhuma conta com este email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])


class CreateUserForm(FlaskForm):
    id = IntegerField('Id', validators=[Optional()])
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=255)])
    active = SelectField('Active', validators=[InputRequired()], choices=[('True', 'True'), ('False', 'False')])

class EditUserForm(FlaskForm):
    id = IntegerField('Id', validators=[Optional()])
    email = EmailField('Email', validators=[InputRequired(), Length(min=7, max=255)])
    password = PasswordField('Password', validators=[Length(min=8, max=255)])
    active = SelectField('Active', validators=[InputRequired()], choices=[('True', 'True'), ('False', 'False')])


class CreateProfileForm(FlaskForm):
    id = IntegerField('Id', validators=[Optional()])
    user_id = IntegerField('User Id', validators=[InputRequired()])
    first_name = StringField('Nome Próprio', validators=[InputRequired(), Length(min=1, max=50)])
    last_name = StringField('Apelido', validators=[InputRequired(), Length(min=1, max=50)])
    registration_date = DateTimeField('Registration Date', validators=[Optional()])
    photo = FileField('Photo', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'])])
    phone = StringField('Telemóvel', validators=[InputRequired(), Length(min=9, max=30)])
    classification = DecimalField('Classificação', validators=[Optional(), NumberRange(min=1, max=5, message='A classificação deve ser entre 1 e 5.')])


class CreateVehicleForm(FlaskForm):
    id = IntegerField('Id', validators=[Optional()])
    user_id = IntegerField('User Id', validators=[InputRequired()])
    license_plate = StringField('License Plate', validators=[InputRequired(), Length(min=8, max=8)])
    brand = StringField('Brand', validators=[InputRequired(), Length(min=1, max=50)])
    model = StringField('Model', validators=[InputRequired(), Length(min=1, max=50)])
    color = StringField('Color', validators=[InputRequired(), Length(min=1, max=20)])
    is_deleted = SelectField('Is Deleted', validators=[InputRequired()], choices=[('False', 'False'), ('True', 'True')])
    created_at = DateTimeField('Created at', validators=[Optional()])
    updated_at = DateTimeField('Updated at', validators=[Optional()])
