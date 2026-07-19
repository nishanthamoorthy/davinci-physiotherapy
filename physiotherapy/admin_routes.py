import os
import uuid
from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, current_app
)
from werkzeug.utils import secure_filename
from extensions import db
from models import Admin, Service, Appointment, ContactMessage, Testimonial, Setting
from forms import LoginForm, ServiceForm, TestimonialForm, SettingsForm

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


def save_upload(file_storage):
    if not file_storage or file_storage.filename == '':
        return None
    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in current_app.config['ALLOWED_EXTENSIONS']:
        return None
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name))
    return unique_name


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data.strip()).first()
        if admin and admin.check_password(form.password.data):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash(f'Welcome back, {admin.username}!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Invalid username or password.', 'danger')

    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_appointments': Appointment.query.count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'total_services': Service.query.count(),
        'total_messages': ContactMessage.query.count(),
        'total_testimonials': Testimonial.query.count(),
    }
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats,
                            recent_appointments=recent_appointments,
                            recent_messages=recent_messages)


# ---------------- Appointments ----------------

@admin_bp.route('/appointments')
@login_required
def appointments():
    status_filter = request.args.get('status', 'all')
    query = Appointment.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    all_appts = query.order_by(Appointment.created_at.desc()).all()
    return render_template('admin/appointments.html', appointments=all_appts, status_filter=status_filter)


@admin_bp.route('/appointments/<int:appt_id>/status/<string:new_status>')
@login_required
def update_appointment_status(appt_id, new_status):
    valid = {'pending', 'confirmed', 'completed', 'cancelled'}
    appt = Appointment.query.get_or_404(appt_id)
    if new_status in valid:
        appt.status = new_status
        db.session.commit()
        flash(f'Appointment marked as {new_status}.', 'success')
    return redirect(url_for('admin.appointments'))


@admin_bp.route('/appointments/<int:appt_id>/delete', methods=['POST'])
@login_required
def delete_appointment(appt_id):
    appt = Appointment.query.get_or_404(appt_id)
    db.session.delete(appt)
    db.session.commit()
    flash('Appointment deleted.', 'success')
    return redirect(url_for('admin.appointments'))


# ---------------- Services ----------------

@admin_bp.route('/services')
@login_required
def services():
    all_services = Service.query.order_by(Service.id).all()
    return render_template('admin/services.html', services=all_services)


@admin_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    form = ServiceForm()
    if form.validate_on_submit():
        image_name = save_upload(form.image.data)
        service = Service(
            title=form.title.data,
            description=form.description.data,
            icon=form.icon.data or 'fa-solid fa-hand-holding-medical',
            image=image_name,
            status=form.status.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service added successfully.', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html', form=form, mode='Add')


@admin_bp.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.title = form.title.data
        service.description = form.description.data
        service.icon = form.icon.data
        service.status = form.status.data
        image_name = save_upload(form.image.data)
        if image_name:
            service.image = image_name
        db.session.commit()
        flash('Service updated successfully.', 'success')
        return redirect(url_for('admin.services'))
    return render_template('admin/service_form.html', form=form, mode='Edit', service=service)


@admin_bp.route('/services/<int:service_id>/delete', methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted.', 'success')
    return redirect(url_for('admin.services'))


# ---------------- Testimonials ----------------

@admin_bp.route('/testimonials')
@login_required
def testimonials():
    all_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=all_testimonials)


@admin_bp.route('/testimonials/add', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        image_name = save_upload(form.image.data)
        testimonial = Testimonial(
            patient_name=form.patient_name.data,
            designation=form.designation.data,
            review=form.review.data,
            rating=form.rating.data,
            image=image_name,
            status=form.status.data
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully.', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', form=form, mode='Add')


@admin_bp.route('/testimonials/<int:t_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(t_id):
    testimonial = Testimonial.query.get_or_404(t_id)
    form = TestimonialForm(obj=testimonial)
    if form.validate_on_submit():
        testimonial.patient_name = form.patient_name.data
        testimonial.designation = form.designation.data
        testimonial.review = form.review.data
        testimonial.rating = form.rating.data
        testimonial.status = form.status.data
        image_name = save_upload(form.image.data)
        if image_name:
            testimonial.image = image_name
        db.session.commit()
        flash('Testimonial updated successfully.', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonial_form.html', form=form, mode='Edit', testimonial=testimonial)


@admin_bp.route('/testimonials/<int:t_id>/delete', methods=['POST'])
@login_required
def delete_testimonial(t_id):
    testimonial = Testimonial.query.get_or_404(t_id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Testimonial deleted.', 'success')
    return redirect(url_for('admin.testimonials'))


# ---------------- Contact Messages ----------------

@admin_bp.route('/contacts')
@login_required
def contacts():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/contacts.html', messages=all_messages)


@admin_bp.route('/contacts/<int:msg_id>/delete', methods=['POST'])
@login_required
def delete_contact(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.contacts'))


# ---------------- Settings ----------------

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    setting = Setting.query.first()
    if not setting:
        setting = Setting()
        db.session.add(setting)
        db.session.commit()

    form = SettingsForm(obj=setting)
    if form.validate_on_submit():
        setting.clinic_name = form.clinic_name.data
        setting.phone = form.phone.data
        setting.email = form.email.data
        setting.address = form.address.data
        setting.google_map = form.google_map.data
        setting.facebook = form.facebook.data
        setting.instagram = form.instagram.data
        setting.whatsapp = form.whatsapp.data
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html', form=form)
