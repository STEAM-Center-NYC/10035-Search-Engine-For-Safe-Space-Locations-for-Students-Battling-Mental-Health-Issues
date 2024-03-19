from flask import Flask, render_template
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_file = ['settings.toml'])

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html.jinja')

if __name__ == '__main__':
    app.run(debug=True)

