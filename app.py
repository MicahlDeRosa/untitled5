from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from wtforms_fields import *
from models import *

app = Flask(__name__)
app.secret_key = "replace later"

# database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://ncgvwymqybskap:24400b07680a2084e377cc83e33716019e0379d37d7da11473b36b2363e3ea5b@ec2-54-147-126-202.compute-1.amazonaws.com:5432/db1epk59ao59ps'
db = SQLAlchemy(app)

# flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(id):
    User.query.get(int(id))
    return User.query.get(int(id))




@app.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)

        # add user to DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # allow login if validated
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        return "Please login before using chat"


    return "chat with me"


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return "logged out using flask-login "


if __name__ == '__main__':
    app.run()
