from flask import Flask
from flaskext.mysql import MySQL
from os import getenv
from dotenv import load_dotenv
import cloudinary

load_dotenv()

cloudinary.config(
            cloud_name=getenv("CLOUD_NAME"),
            api_key=getenv("API_KEY"),
            api_secret=getenv("API_SECRET"),
            secure=getenv("API_SECRET"))

application = Flask(__name__)

my_sql = MySQL()
application.config["SECRET_KEY"] = getenv("SECRET_KEY")
application.config["MYSQL_DATABASE_HOST"] = getenv("MYSQL_DATABASE_HOST")
application.config["MYSQL_DATABASE_USER"] = getenv("MYSQL_DATABASE_USER")
application.config["MYSQL_DATABASE_PASSWORD"] = getenv("MYSQL_DATABASE_PASSWORD")
application.config["MYSQL_DATABASE_DB"] = getenv("MYSQL_DATABASE_DB")

my_sql.init_app(application)

from crud import routes
