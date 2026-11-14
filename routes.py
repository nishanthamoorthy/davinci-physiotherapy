from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Service, Appointment, ContactMessage, Testimonial, Setting
from forms import AppointmentForm, ContactForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    services = Service.query.filter_by(status='active').order_by(Service.id).limit(5).all()
    testimonials = Testimonial.query.filter_by(status='active').order_by(Testimonial.created_at.desc()).limit(6).all()
    return render_template('index.html', services=services, testimonials=testimonials)


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/services')
def services():
    all_services = Service.query.filter_by(status='active').order_by(Service.id).all()
    return render_template('services.html', services=all_services)


@main_bp.route('/conditions')
def conditions():
    return render_template('conditions.html')


@main_bp.route('/benefits')
def benefits():
    return render_template('benefits.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thank you for reaching out! We will get back to you shortly.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)


@main_bp.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm()
    form.service_id.choices = [(s.id, s.title) for s in Service.query.filter_by(status='active').all()]

    if form.validate_on_submit():
        appt = Appointment(
            patient_name=form.patient_name.data,
            phone=form.phone.data,
            email=form.email.data,
            age=form.age.data,
            gender=form.gender.data,
            service_id=form.service_id.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            address=form.address.data,
            message=form.message.data,
            status='pending'
        )
        db.session.add(appt)
        db.session.commit()
        flash('Your appointment request has been submitted! We will confirm shortly by phone.', 'success')
        return redirect(url_for('main.appointment'))

    return render_template('appointment.html', form=form)
