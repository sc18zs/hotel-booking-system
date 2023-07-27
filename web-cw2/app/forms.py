from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,ValidationError, SelectField, BooleanField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo
from app.models import users

class LoginForm(FlaskForm):
    log_name = StringField('Account', validators=[DataRequired()])
    log_password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep logged in')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8),EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Length(1,64),Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired(),Length(11)])
    submit = SubmitField('Register')

    def validate_email(self,field):
        if users.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,filed):
        if users.query.filter_by(user_name=filed.data).first():
            raise ValidationError('Username already in use.')

    def validate_phone(self, filed):
        if users.query.filter_by(phone=filed.data).first():
            raise ValidationError('Phone number already in use.')

class adminLoginForm(FlaskForm):
    admin_name = StringField('Admin', validators=[DataRequired()])
    admin_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class passwordChangeForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(),Length(8)])
    submit = SubmitField('Submit')