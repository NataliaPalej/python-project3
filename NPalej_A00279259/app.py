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
    sex = db.Column(db.String(25))
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


###################################################
##               INDEX2 METHOD                   ##
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
                return render_template('get_all.html', message='Test', Dog=dogsList)

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
##               SEARCH METHOD                   ##
###################################################

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

###################################################
##               DELETE METHOD                   ##
###################################################
@app.route('/delete2', methods=['GET', 'POST'])
def delete2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            print("delete2() error")
            flash('Flash delete2() error\nPlease enter dogs name', 'error')
        else:
            searchName = request.form['name']
            dog = db.session.query(Dog).filter(Dog.name == searchName).first()
            db.session.delete(dog)
            db.session.commit()
            return redirect(url_for('get_all'))

    searchDog = global_dog
    return render_template('delete2.html', dog=searchDog)


###################################################
##               UPDATE METHOD                   ##
###################################################
@app.route('/update2', methods=['GET', 'POST'])
def update2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            print("update2() error")
            flash('Flash update2() error\nPlease enter dogs name to update', 'error')
        else:
            updateName = request.form['name']
            dog = db.session.query(Dog).filter(Dog.name == updateName).first()
            dog.owner = request.form['owner']
            dog.name = request.form['name']
            dog.breed = request.form['breed']
            dog.colour = request.form['colour']
            dog.activity = request.form['activity']
            dog.maintenance = request.form['maintenance']
            dog.competitions = request.form['competitions']
            dog.disqualified = request.form['disqualified']
            db.session.commit()

            print('Dog {0} was successfully updated'.format(dog.name))
            return redirect(url_for('get_all'))
    searchDog = global_dog

    return render_template('update2.html', dog=searchDog)

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
##            INCREMENT AGE METHOD               ##
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
            return redirect(url_for('get_all'))

        try:
            dog = get_dog_by_name(dog_name)
            increment(dog, 'age')
            return redirect(url_for('get_all'))
        except Exception as e:
            print(f"increment_age() error: {str(e)}")
            flash('Flash increment_age() error', 'error')
            return redirect(url_for('get_all'))

    searchDog = global_dog
    return render_template('increment_age2.html', dog=searchDog)


###################################################
##       INCREMENT COMPETITIONS METHOD           ##
###################################################
@app.route('/increment_competitions', methods=['GET', 'POST'])
def increment_competitions():
    searchName = 'abc'
    if request.method == 'POST':
        dog_name = request.form.get('name')
        if not dog_name:
            print("increment_competitions() error")
            flash('Flash increment_competitions() error\n'
                  'Please enter the dog\'s name to increment competitions', 'error')
            return redirect(url_for('get_all'))

        try:
            dog = get_dog_by_name(dog_name)
            increment(dog, 'competitions')
            return redirect(url_for('get_all'))
        except Exception as e:
            print(f"increment_competitions() error: {str(e)}")
            flash('Flash increment_competitions() error', 'error')
            return redirect(url_for('get_all'))

    searchDog = global_dog
    return render_template('increment_competitions2.html', dog=searchDog)


###################################################
##                GET ALL METHOD                 ##
###################################################
@app.route('/get_all', methods=['GET', 'POST'])
def get_all():
    all_data3 = db.session.query(Dog).all()
    return render_template('get_all.html', message='test', Dog=all_data3)


###################################################
##         INITIAL TABLE DATA METHOD             ##
###################################################
@app.route('/initial_table_data', methods=['GET', 'POST'])
def initial_table_data():
    if request.method == 'POST':
        print('here')
        db.session.add(Dog('Natalia', 'Lilly', 3, "Female", 'Yorkshire Terrier', 'Tan-Silver', 'High', 'High', 2, 'No'))
        db.session.add(Dog('Monika', 'Gizmo', 9, 'Male', 'Shith Tzu', 'Black-White', 'Low', 'Medium', 0, 'No')),
        db.session.add(Dog('Dominik', 'Luna', 3, 'Female', 'Cavapoo', 'Light-Brown', 'Medium', 'Medium', 1, 'No'))
        db.session.add(Dog('Kasia', 'Coco', 3, 'Male', 'Cockpoo', 'Dark-Brown', 'High', 'Medium', 2, 'No'))
        db.session.add(Dog('Adrian', 'Lola', 1, 'Female', 'Yorkshire Terrier', 'Silver-Tan', 'High', 'Very High', 0, 'No'))
        db.session.commit()
        flash('Initial Table Data Added')

    return render_template('initial_table_data.html')


###################################################
##              ADD NEW DOG METHOD               ##
###################################################
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Validate that all required form fields are present
        try:
            # Validate that all required form fields are present
            required_fields = ['owner', 'name', 'age', 'sex', 'breed', 'colour', 'activity', 'maintenance',
                               'competitions', 'disqualified']
            for field in required_fields:
                if not request.form.get(field):
                    print("add() error, all fields must be filled")
                    flash(f'Flash add() error\nPlease enter {field}', 'error')
                    return redirect(url_for('add'))

            # Convert age and competitions to integers
            try:
                age = int(request.form['age'])
                competitions = int(request.form['competitions'])
            except ValueError:
                flash('Age and Competitions must be positive numbers', 'error')
                return redirect(url_for('add'))

            # Check if age and competitions positive
            if age < 0 or competitions < 0:
                flash('Age and Competitions must be positive numbers', 'error')
                return redirect(url_for('add'))

            # Create new Dog instance
            dog = Dog(
                owner=request.form['owner'],
                name=request.form['name'],
                age=age,
                sex=request.form['sex'],
                breed=request.form['breed'],
                color=request.form['colour'],
                activity=request.form['activity'],
                maintenance=request.form['maintenance'],
                competitions=competitions,
                disqualified=request.form['disqualified']
            )

            # Add new dog to the database
            db.session.add(dog)
            db.session.commit()

            flash('Dog {0} added successfully!'.format(dog.name))
            return redirect(url_for('get_all'))
        except Exception as e:
            # Print error message
            print(f"add() error: {str(e)}")
            flash('flash add() error:', 'error')
            return redirect(url_for('add'))

    return render_template('add.html')


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')