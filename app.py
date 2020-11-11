from flask import Flask, render_template, redirect, url_for
from wtforms_fields import *
from models import *

app = Flask(__name__)
app.secret_key = "replace later"

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ncgvwymqybskap:24400b07680a2084e377cc83e33716019e0379d37d7da11473b36b2363e3ea5b@ec2-54-147-126-202.compute-1.amazonaws.com:5432/db1epk59ao59ps'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))



    return render_template("index.html", form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():


    login_form = LoginForm()


    if login_form.validate_on_submit():
        return "logged in, Success!"

    return render_template("login.html", form=login_form)

if __name__ == '__main__':
    app.run()
