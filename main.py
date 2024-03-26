from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def aboutus():
    return render_template('aboutus.html.jinja')

if __name__ == '__main__':
    app.run()