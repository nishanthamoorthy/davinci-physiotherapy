
import os
import pymysql
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

load_dotenv(".env", override=True)

url = make_url(os.getenv("DATABASE_URL"))

try:
    connection = pymysql.connect(
        host=url.host,
        port=url.port or 4000,
        user=url.username,
        password=url.password,
        database=url.database,
        ssl_verify_cert=True,
        ssl_verify_identity=True,
        connect_timeout=15,
        read_timeout=30,
        write_timeout=30
    )

    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("Database test:", cursor.fetchone())

        cursor.execute("SELECT DATABASE()")
        print("Database name:", cursor.fetchone())

    connection.close()
    print("TiDB connection successful!")

except Exception as error:
    print("Connection failed:", type(error).__name__)
    print("Error:", error)
