# this piece of code deals with the form from flask for the website
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm): # the class for the registration form
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]) # username field, the string type, it is required and has a minimum and max length

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters')]) # password fields are automatically not shown but in the html page the hidden_tag allows for this functionality to properly show
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
                                     
    course_selection = SelectField(u'Course', choices=[('General Science', 'General Science'),
    ('General Arts', 'General Arts'), ('Visual Arts', 'Visual Arts'), ('Technical', 'Technical'),
    ('Home Economics', 'Home Economics'), ('Business', 'Business')], validators=[DataRequired()])
    
    submit = SubmitField('Sign Up') 


    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is not available')

    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken.')





class LoginForm(FlaskForm): # the class for the login
    
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')


class  RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That email doesn\'t exist. Please register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters')]) # password fields are automatically not shown but in the html page the hidden_tag allows for this functionality to properly show
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
