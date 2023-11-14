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


@app.route('/', methods=['GET', 'POST'])
def index2():
    global global_dog
    if request.method == 'POST':
        if 'Search_By_Owner' in request.form:
            if not request.form['owner']:
                print("index2() Search_By_Owner error")
                flash('Flash index2() Search_By_Owner error\n'
                      'Please enter owner name', 'error')
            else:
                searchOwner = request.form['owner']
                dogsList = db.session.query(Dog).filter(Dog.owner == searchOwner).all()
                return render_template('show_all.html', message='Test', Dog=dogsList)

        elif 'Search_By_Name' in request.form:
            if not request.form['name']:
                print("index2() Search_By_Name error")
                flash('Flash index2() Search_By_Name Error \n'
                      'Please enter dogs name', 'error')
            else:
                searchName = request.form['name']
                dog = db.session.query(Dog).filter(Dog.name == searchName).first()
                return render_template('search.html', message='Test', dog=dog)

        elif 'Delete_Dog' in request.form:
            if not request.form['name']:
                print("index2() Delete_Dog error")
                flash('Flash index2() Delete_Dog Error\n'
                      'Please enter dogs name to delete', 'error')
            else:
                searchName = request.form['name']
                dog = db.session.query(Dog).filter(Dog.name == searchName).first()
                global_dog = dog
                return redirect(url_for('delete2', dog=dog))

        elif 'Update_Dog' in request.form:
            if not request.form['name']:
                print("index2() Update_Dog error")
                flash('Flash index2() Update_Dog error\n'
                      'Please enter dogs name to update', 'error')
            else:
                searchName = request.form['name']
                dog = db.session.query(Dog).filter(Dog.name == searchName).first()
                global_dog = dog
                return redirect(url_for('update2', dog=dog))

        elif 'Increment_Dog_Age' in request.form:
            if not request.form['name']:
                print("index2() Increment_Dog_Age error")
                flash('Flash index2() Increment_Dog_Age error\n'
                      'Please enter all the name fields', 'error')
            else:
                searchName = request.form['name']
                dog = db.session.query(Dog).filter(Dog.name == searchName).first()
                global_dog = dog
                return redirect(url_for('increment_age', dog=dog))

        elif 'Increment_Competitions' in request.form:
            if not request.form['name']:
                print("index2() Increment_Competitions error")
                flash('Flash index2() Increment_Competitions error\n'
                      'Please enter dogs name to increment competitions', 'error')
            else:
                searchName = request.form['name']
                dog = db.session.query(Dog).filter(Dog.name == searchName).first()
                global_dog = dog
                return redirect(url_for('increment_competitions', dog=dog))

        elif 'Update_Disqualified' in request.form:
            if not request.form['name']:
                print("index2() Update_Disqualified error")
                flash('Flash index2() Update_Disqualified error\n'
                      'Please enter dogs name to update disqualified field', 'error')
            else:
                searchName = request.form['name']
                dog = db.session.query(Dog).filter(Dog.name == searchName).first()
                global_dog = dog
                return redirect(url_for('update_disqualified2', dog=dog))

    all_data3 = db.session.query(Dog).all()
    return render_template('index2.html', message='test', Dog=all_data3)


###################################################
##              INCREMENT METHOD                 ##
###################################################
def increment(dog, attribute):
    try:
        value = int(request.form[attribute])
        setattr(dog, attribute, value + 1)
        db.session.commit()
        flash(f'{attribute.capitalize()} incremented successfully for {dog.name}!')
    except Exception as e:
        print(f"increment() error: {str(e)}")
        flash(f'Flash increment() error\n'
              f'Error incrementing {attribute} for {dog.name}', 'error')
###################################################
##           INCREMENT METHOD ENDS               ##
###################################################

@app.route('/increment_age', methods=['GET', 'POST'])
def increment_age():
    searchName = 'abc'
    if request.method == 'POST':
        dog_name = request.form.get('name')
        if not dog_name:
            print("increment_age() error")
            flash('Flash increment_age() error\n'
                  'Please enter the dog\'s name to increment age', 'error')
            return redirect(url_for('show_all'))

        try:
            dog = get_dog_by_name(dog_name)
            increment(dog, 'age')
            return redirect(url_for('show_all'))
        except Exception as e:
            print(f"increment_age() error: {str(e)}")
            flash('Flash increment_age() error', 'error')
            return redirect(url_for('show_all'))

    searchDog = global_dog
    return render_template('increment_age2.html', dog=searchDog)

@app.route('/increment_competitions', methods=['GET', 'POST'])
def increment_competitions():
    searchName = 'abc'
    if request.method == 'POST':
        dog_name = request.form.get('name')
        if not dog_name:
            print("increment_competitions() error")
            flash('Flash increment_competitions() error\n'
                  'Please enter the dog\'s name to increment competitions', 'error')
            return redirect(url_for('show_all'))

        try:
            dog = get_dog_by_name(dog_name)
            increment(dog, 'competitions')
            return redirect(url_for('show_all'))
        except Exception as e:
            print(f"increment_competitions() error: {str(e)}")
            flash('Flash increment_competitions() error', 'error')
            return redirect(url_for('show_all'))

    searchDog = global_dog
    return render_template('increment_competitions2.html', dog=searchDog)


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')