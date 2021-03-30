from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField
from wtforms.validators import Length, EqualTo, Email, Regexp, DataRequired, ValidationError
from bank.models import User


class RegisterForm(FlaskForm):

    def validate_phone(self, phone_to_check):
        phone = User.query.filter_by(phone=phone_to_check.data).first()
        if phone:
            raise ValidationError('Phone number already exists! Please try a different number')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[
        DataRequired(), Length(1, 64)])
    # Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
    #        'Usernames must have only letters, numbers, dots or '
    #        'underscores')
    phone = StringField(label='Phone number:', validators=[Length(min=10, max=11), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', message='Passwords must match.'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# class PurchaseItemForm(FlaskForm):
#     submit = SubmitField(label='Purchase Item!')
#
# class SellItemForm(FlaskForm):
#     submit = SubmitField(label='Sell Item!')


class PayForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')
