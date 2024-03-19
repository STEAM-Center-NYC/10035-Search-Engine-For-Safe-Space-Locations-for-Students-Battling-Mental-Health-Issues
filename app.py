from flask import Flask, render_template, request, redirect, url_for, g
from dynaconf import Dynaconf
import pymysql
import pymysql.cursors

settings = Dynaconf(
    settings_file = ['settings.toml'])

app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user = settings.db_user,
        password=settings.db_password,
        database= settings.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


@app.route('/')
def landing():
    return render_template('landing.html.jinja')


@app.route('/locations')
def locations():
    connection = connect_db()
    with connection.cursor() as cursor:
        sql = "SELECT name, address FROM Locations"
        cursor.execute(sql)
        locations_data = cursor.fetchall()
    connection.close()

    return render_template('locations.html.jinja', locations=locations_data)


if __name__ == '__main__':
    app.run(debug=True)
