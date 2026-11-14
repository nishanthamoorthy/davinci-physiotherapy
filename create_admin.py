"""
Run this once after setting up the database to create your first admin account:

    python create_admin.py
"""
import getpass
from app import create_app
from extensions import db
from models import Admin

app = create_app()

with app.app_context():
    print("=== Create Davinci Physiotherapy Admin Account ===")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm Password: ")

    if password != confirm:
        print("Passwords do not match. Aborting.")
        exit(1)

    if Admin.query.filter_by(username=username).first():
        print("An admin with that username already exists. Aborting.")
        exit(1)

    admin = Admin(username=username, email=email, role='superadmin')
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin '{username}' created successfully!")
