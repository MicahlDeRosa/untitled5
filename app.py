from flask import Flask, render_template
from wtforms_fields import RegistrationForm
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

        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else has taken this username"

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted in DB"



    return render_template("index.html", form=reg_form)


if __name__ == '__main__':
    app.run()
