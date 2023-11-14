"""
A sample Hello World server.
"""
import os

from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.sqlite3'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class Dog(db.Model):
    id = db.Column('dogID', db.Integer, primary_key=True)
    owner = db.Column(db.String(25))
    name = db.Column(db.String(25))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(25))
    breed = db.Column(db.String(15))
    color = db.Column(db.String(25))
    activity = db.Column(db.String(25))
    maintenance = db.Column(db.String(25))
    competitions = db.Column(db.Integer)
    disqualified = db.Column(db.String(50))

    def __init__(self, owner, name, age, sex, breed, color, activity, maintenance, competitions,
                     disqualified):
        self.name = name
        self.owner = owner
        self.age = age
        self.sex = sex
        self.breed = breed
        self.color = color
        self.activity = activity
        self.maintenance = maintenance
        self.competitions = competitions
        self.disqualified = disqualified
db.create_all()

# Ensure index2, delete2 & update2 are referencing the same dog
global_dog = Dog('A', 'A', 0, "A", "A", "A", "A", 0, "A")


###################################################
##               GET METHODS                     ##
###################################################

        # GET dog by NAME
def get_dog_by_name(name):
    dog = db.session.query(Dog).filter(Dog.name == name).first()
    if not dog:
        # Dog not found, return a 404 error
        os.abort(404)
    return dog

        # GET dog by OWNER
def get_dog_by_owner(owner):
    dog = db.session.query(Dog).filter(Dog.owner == owner).first()
    if not dog:
        os.abort(404)
    return dog

###################################################
##               GET METHODS ENDS                ##
###################################################





if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')