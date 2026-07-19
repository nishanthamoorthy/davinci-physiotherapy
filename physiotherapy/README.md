# Davinci Physiotherapy — Full-Stack Flask + MySQL Website

A complete, production-ready physiotherapy management website with a public site and an admin panel, built with **Python Flask** and **MySQL**.

---

## 1. Tech Stack

- **Backend:** Python Flask, SQLAlchemy ORM, Flask-Migrate, Flask-WTF
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Jinja2
- **Database:** MySQL 8 (via PyMySQL)
- **Auth:** Werkzeug password hashing + server-side sessions
- **Icons:** Font Awesome 6
- **Fonts:** Playfair Display (headings), Poppins (body)
- **Animation:** AOS (Animate On Scroll)

---

## 2. Folder Structure

```
physiotherapy/
├── app.py                 # Application factory + entry point
├── config.py               # Configuration (reads .env)
├── extensions.py           # db, migrate, csrf instances
├── models.py                # SQLAlchemy models
├── forms.py                  # Flask-WTF forms
├── routes.py                  # Public site routes (blueprint: main)
├── admin_routes.py             # Admin panel routes (blueprint: admin)
├── create_admin.py              # CLI script to create the first admin user
├── requirements.txt
├── .env                            # Environment variables (DB credentials, secret key)
├── database/
│   └── schema.sql            # Full MySQL schema + seed data
├── templates/
│   ├── base.html            # Public site layout (navbar, footer, floating buttons)
│   ├── index.html, about.html, services.html, conditions.html,
│   │   benefits.html, contact.html, appointment.html, 404.html
│   └── admin/
│       ├── base_admin.html, login.html, dashboard.html,
│       │   appointments.html, services.html, service_form.html,
│       │   testimonials.html, testimonial_form.html,
│       │   contacts.html, settings.html
└── static/
    ├── css/style.css
    ├── js/script.js
    ├── images/logo.svg
    └── uploads/              # Uploaded service/testimonial images land here
```

---

## 3. Installation

### Step 1 — Clone / extract the project and enter the folder
```bash
cd physiotherapy
```

### Step 2 — Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables
Edit the `.env` file with your MySQL credentials and a strong secret key:
```
SECRET_KEY=replace-with-a-long-random-string
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=davinci_physiotherapy
```

### Step 5 — Set up MySQL and import the schema
Make sure MySQL 8 is running, then:
```bash
mysql -u root -p < database/schema.sql
```
This creates the `davinci_physiotherapy` database, all tables (with foreign keys, indexes, timestamps), and seeds default services and testimonials.

> Alternatively, Flask-Migrate can generate/manage the schema from `models.py`:
> ```bash
> flask db init
> flask db migrate -m "initial schema"
> flask db upgrade
> ```
> (Set `FLASK_APP=app.py` first, and create the empty `davinci_physiotherapy` database beforehand.)

### Step 6 — Create your first admin account
```bash
python create_admin.py
```
Follow the prompts to set a username, email, and password. Passwords are hashed with Werkzeug — never stored in plain text.

### Step 7 — Run the application
```bash
python app.py
```
Visit:
- Public site → http://localhost:5000/
- Admin panel → http://localhost:5000/admin/login

---

## 4. Features

**Public site**
- Home, About, Services, Conditions, Benefits, Book Appointment, Contact, custom 404
- Sticky navbar, hero section, feature highlights, dynamic services grid, "Why Choose Us", testimonials, contact CTA
- Appointment booking form (saved to MySQL, validated, flash messages)
- Contact form (saved to MySQL)
- WhatsApp + Call floating buttons, back-to-top button, loading spinner, smooth scroll, AOS scroll animations, Google Maps embed, SEO meta tags, favicon

**Admin panel** (`/admin`)
- Secure login (hashed passwords, session-based auth, `login_required` decorator on every protected route)
- Dashboard with live stats and recent activity
- Full CRUD: Appointments (status workflow: pending → confirmed → completed/cancelled), Services, Testimonials, Contact Messages, Settings (clinic info, social links, WhatsApp, map embed)
- Image uploads for services/testimonials (validated file types, stored in `static/uploads`)

**Security**
- CSRF protection on every form (Flask-WTF)
- SQLAlchemy ORM parameterized queries (no raw SQL string interpolation → SQL-injection safe)
- Werkzeug password hashing
- Server-side session-based admin auth guarding all `/admin/*` routes except login
- Server- and client-side input validation

---

## 5. Deployment

For production, run behind Gunicorn + Nginx (or similar):

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Checklist before going live:
- Set `SECRET_KEY` to a long random value in `.env` (never commit real secrets)
- Set `debug=False` in `app.py` (already the default when run via Gunicorn)
- Use a dedicated MySQL user with least-privilege access instead of `root`
- Put Nginx (or another reverse proxy) in front of Gunicorn and terminate HTTPS there
- Back up the `static/uploads/` folder and the MySQL database regularly

---

## 6. Notes

- The homepage design (navbar, hero, About, Services grid, Why Choose Us, footer, color palette `#5B3A1A` / `#3D2813` / `#F8F4EF`, Playfair Display + Poppins) was built to closely match the provided reference screenshot.
- Service icons and testimonial photos are manageable entirely from the admin panel — no code changes needed to add/update/remove them.
