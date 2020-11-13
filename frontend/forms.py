from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from frontend.models import User, Project


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ProjectForm(FlaskForm):
    name = StringField('Name*',
                           validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Description')
    configFile = StringField('Config File*')
    inventoryFile = StringField('Inventory File*')
    submit = SubmitField('Save')
    def validate_name(self, name):
        name = Project.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That Project name is taken. Please choose a different one.')

    def validate_configFile(self, configFile):
        configFile = Project.query.filter_by(config_file=configFile.data).first()
        if configFile:
            raise ValidationError('Project with this config file is exist. Please choose a different one.')