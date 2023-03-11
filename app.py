from flask import Flask, render_template
from blueprints import bp_register
import config
from exts import db, mail
from flask_migrate import Migrate
from model import *


app = Flask(__name__)
bp_register(app)
app.config.from_object(config)
app.config['DATABASE'] = 'travelAgency'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\\SQLite\\travelAgency.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
mail.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    # return render_template("ProductsDetail.html")
    return render_template("SignInUp.html")
    # return render_template("Homepage.html")


if __name__ == '__main__':
    app.run()
