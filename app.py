from flask import Flask, render_template, request, redirect, g
from dynaconf import Dynaconf
import pymysql
import pymysql.cursors
import flask_login
from flask_login import UserMixin, login_user, logout_user, login_required

settings = Dynaconf(settings_file=['settings.toml'])

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user=settings.db_user,
        password=str(settings.db_password),
        database=settings.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    @staticmethod
    def get(user_id):
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM `Users` WHERE id = {user_id}")
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return User(user_data['id'], user_data['username'], user_data['email'])
        else:
            return None


# Initialize Flask-Login
login_manager = flask_login.LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def landing():
    return render_template('landing.html.jinja')


@app.route('/locations')
def locations():
    connection = connect_db()
    with connection.cursor() as cursor:
        sql = "SELECT name, address, description FROM Locations"
        cursor.execute(sql)
        locations_data = cursor.fetchall()
    connection.close()
    return render_template('locations.html.jinja', locations=locations_data)


@app.route('/contact')
def contact():
    return render_template('contact.html.jinja')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html.jinja')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html.jinja')


@app.route('/questionnnaire')
def questionnnaire():
    return render_template('questionnnaire.html.jinja')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cursor = get_db().cursor()
        cursor.execute(
            f"INSERT INTO `Users` (email, username, password) VALUES ('{email}', '{username}', '{password}')")
        cursor.close()
        get_db().commit()

        return redirect('/signin')
    return render_template('signup.html.jinja')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute(f"SELECT * FROM `Users` WHERE username='{username}'")
        result = cursor.fetchone()
        cursor.close()
        if result and result['password'] == password:
            user = User(result['id'], result['username'], result['email'])
            login_user(user)
            return redirect('/')
        else:
            error = "Invalid username or password. Please try again."
            return render_template('signin.html.jinja', error=error)
    return render_template('signin.html.jinja')


if __name__ == '__main__':
    app.run(debug=True)
