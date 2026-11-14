
import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

basedir = os.path.abspath(os.path.dirname(__file__))

# Load .env file
env_path = os.path.join(basedir, ".env")
load_dotenv(env_path, override=True)


def _database_url():

    raw_url = os.environ.get("DATABASE_URL", "").strip()

    if not raw_url:
        raise RuntimeError(
            "DATABASE_URL is missing. Check your .env file."
        )

    if raw_url.startswith("mysql://"):
        raw_url = raw_url.replace(
            "mysql://",
            "mysql+pymysql://",
            1
        )

    try:
        url = make_url(raw_url)

    except Exception as exc:
        raise RuntimeError(
            "Invalid DATABASE_URL. Check your database credentials."
        ) from exc

    if url.drivername not in ("mysql", "mysql+pymysql"):
        raise RuntimeError(
            "Only MySQL with PyMySQL is supported."
        )

    url = url.set(drivername="mysql+pymysql")

    query = dict(url.query)
    query["ssl_verify_cert"] = "true"
    query["ssl_verify_identity"] = "true"

    return url.set(query=query)


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY missing. Check .env file location."
        )

    SQLALCHEMY_DATABASE_URI = _database_url()

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 1,
        "max_overflow": 0,
        "pool_timeout": 10,
        "connect_args": {
            "connect_timeout": 10,
            "read_timeout": 20,
            "write_timeout": 20,
        },
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = (
        "/tmp/davinci-uploads"
        if os.environ.get("VERCEL")
        else os.path.join(basedir, "static", "uploads")
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png", "jpg", "jpeg", "gif", "webp"
    }

    WTF_CSRF_ENABLED = True

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = bool(os.environ.get("VERCEL"))

    CLINIC_NAME = "Davinci Physiotherapy"
    CLINIC_PHONE = "90251 00053"
    CLINIC_EMAIL = "davinciphysiotherapy@gmail.com"
    CLINIC_WHATSAPP = "919025100053"
