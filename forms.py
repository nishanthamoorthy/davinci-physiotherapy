from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SelectField, IntegerField,
    DateField, TimeField, PasswordField, IntegerRangeField
)
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class AppointmentForm(FlaskForm):
    patient_name = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=120)])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
    ], validators=[DataRequired()])
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    appointment_date = DateField('Preferred Date', validators=[DataRequired()])
    appointment_time = TimeField('Preferred Time', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    message = TextAreaField('Additional Message', validators=[Optional()])


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ServiceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    icon = StringField('Icon (Font Awesome class)', validators=[Optional(), Length(max=100)])
    image = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'])])
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')])


class TestimonialForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired(), Length(max=150)])
    designation = StringField('Designation', validators=[Optional(), Length(max=150)])
    review = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    image = FileField('Photo', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'])])
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')])


class SettingsForm(FlaskForm):
    clinic_name = StringField('Clinic Name', validators=[DataRequired(), Length(max=150)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    google_map = TextAreaField('Google Map Embed URL', validators=[Optional()])
    facebook = StringField('Facebook URL', validators=[Optional(), Length(max=255)])
    instagram = StringField('Instagram URL', validators=[Optional(), Length(max=255)])
    whatsapp = StringField('WhatsApp Number', validators=[Optional(), Length(max=20)])
