import os
from flask import Flask, request, flash, url_for, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dog_manager.sqlite3'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)

    dogs = db.relationship('Dog', back_populates='user')

    def __init__(self, user, user_email, user_password):
        self.user = user
        self.user_email = user_email
        self.user_password = user_password


class Dog(db.Model):
    __tablename__ = 'dog_table'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user_table.id"))
    name = db.Column(db.String(25))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(25))
    breed = db.Column(db.String(15))
    colour = db.Column(db.String(25))
    activity = db.Column(db.String(25))
    maintenance = db.Column(db.String(25))
    competitions = db.Column(db.Integer)
    disqualified = db.Column(db.String(50))

    user = db.relationship('User', back_populates='dogs')

    def __init__(self, user_id, name, age, sex, breed, colour, activity, maintenance, competitions, disqualified):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sex = sex
        self.breed = breed
        self.colour = colour
        self.activity = activity
        self.maintenance = maintenance
        self.competitions = competitions
        self.disqualified = disqualified


def create_tables():
    db.create_all()


def add_initial_data():
    # Check if the users already exist
    natalia = User.query.filter_by(user_email='natalia@gmail.com').first()
    if not natalia:
        # Creating Users
        natalia = User(user='Natalia', user_email='natalia@gmail.com', user_password='natalia')
        monika = User(user='Monika', user_email='monika@gmail.com', user_password='monika')
        dominik = User(user='Dominik', user_email='dominik@gmail.com', user_password='dominik')
        kasia = User(user='Kasia', user_email='kasia@gmail.com', user_password='kasia')
        adrian = User(user='Adrian', user_email='adrian@gmail.com', user_password='adrian')

        db.session.add_all([natalia, monika, dominik, kasia, adrian])
        db.session.commit()

        # Check if the dogs already exist
        lilly = Dog.query.filter_by(name='Lilly').first()
        if not lilly:
            # Creating Dogs
            db.session.add(Dog(user_id=natalia.id, name='Lilly', age=3, sex='Female', breed='Yorkshire Terrier',
                               colour='Tan-Silver', activity='High', maintenance='High', competitions=2,
                               disqualified='No'))
            db.session.add(Dog(user_id=monika.id, name='Gizmo', age=9, sex='Male', breed='Shi Tzu',
                               colour='Black-White', activity='Low', maintenance='Medium', competitions=0,
                               disqualified='No'))
            db.session.add(Dog(user_id=dominik.id, name='Luna', age=3, sex='Female', breed='Cavapoo',
                               colour='Light-Brown', activity='Medium', maintenance='Medium', competitions=1,
                               disqualified='No'))
            db.session.add(Dog(user_id=kasia.id, name='Coco', age=3, sex='Male', breed='Cockpoo',
                               colour='Dark-Brown', activity='High', maintenance='Medium', competitions=2,
                               disqualified='No'))
            db.session.add(Dog(user_id=adrian.id, name='Lola', age=1, sex='Female', breed='Yorkshire Terrier',
                               colour='Silver-Tan', activity='High', maintenance='Very High', competitions=0,
                               disqualified='No'))
            db.session.commit()


###################################################
#                GET METHODS                      #
###################################################

def get_dog_by_name(name):
    dog = db.session.query(Dog).join(User).filter(Dog.name == name).first()
    if not dog:
        # Dog not found, return a 404 error
        print('get_dog_by_name() error: dog not found')
        os.abort()
    else:
        print("get_dog_by_name(): ", dog)
    return dog


def get_dog_by_user(user):
    dog = db.session.query(Dog).join(User).filter(User.user == user).first()
    if not dog:
        print('get_dog_by_user() error: dog not found')
        os.abort()
    else:
        print("get_dog_by_user(): ", dog)
    return dog


###################################################
#             OWNERS AND DOGS METHODS             #
###################################################
def users_count():
    # Count the number of users in the User table
    count = User.query.count()
    return count


def dogs_count():
    # Count the number of dogs in the Dog table
    count = Dog.query.count()
    return count


###################################################
#                    ROUTES                       #
###################################################
@app.route('/', methods=['GET', 'POST'])
def login():  # login page route
    if 'Login' in request.form:
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        # Query the database to find the user with the provided email and password
        user = db.session.query(User).filter_by(user_email=user_email, user_password=user_password).first()
        if user:
            # Set the user session for session management
            session['user_id'] = user.id
            print("User {0} logged in successfully.".format(user.user))
            flash('Login successful !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    elif 'Register' in request.form:
        return redirect(url_for('register'))
    return render_template('login.html')


# Route to display the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Validate that all required form fields are present
        required_fields = ['user', 'user_email', 'user_password']
        for field in required_fields:
            if not request.form.get(field):
                print("register() error, all fields must be filled")
                flash(f'Flash register() error\nPlease enter {field}', 'error')
                return redirect(url_for('register'))

        # Check if the user with the given email already exists
        user_exists = db.session.query(User).filter_by(user_email=request.form['user_email']).first()
        if user_exists:
            flash('User with this email already exists. Please log in.', 'error')
            return redirect(url_for('login'))

        # Create a new user instance and add it to the database
        new_user = User(
            user=request.form['user'],
            user_email=request.form['user_email'],
            user_password=request.form['user_password']
        )

        db.session.add(new_user)
        db.session.commit()

        # print("Registration successful. Welcome {0} and your doggie {1}".format(new_user.user, new_dog.name))
        # flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login', success_message='200'))

    return render_template('register.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id')

    if user_id:
        user = db.session.query(User).get(user_id)
        if user:
            dogs_list = db.session.query(Dog).filter(Dog.user_id == user_id).all()
            return render_template('index.html', user=user, dogs_list=dogs_list)

    # If user is not logged in redirect to login page
    flash('You need to log in to access this page', 'error')
    return redirect(url_for('login'))


@app.route('/selected_dog', methods=['POST'])
def selected_dog():
    selected_dog_name = request.form.get('selected_dog_name')
    user_choice = request.form.get('userChoice')

    # Fetch user details
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)

    if user_choice == 'Update':
        return redirect(url_for('update_dog', user=user, dog_name=selected_dog_name))
    elif user_choice == 'Delete':
        return redirect(url_for('delete_dog', user=user, dog_name=selected_dog_name))
    else:
        flash('Invalid action selected', 'error')
        return redirect(url_for('index'))


###################################################
#                DELETE METHOD                    #
###################################################
@app.route('/delete_dog/<dog_name>', methods=['GET', 'POST'])
def delete_dog(dog_name):
    # Fetch the dog from the database based on the provided name
    dog = db.session.query(Dog).filter(Dog.name == dog_name).first()
    # Fetch user details
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)

    if request.method == 'POST':
        try:
            db.session.delete(dog)
            db.session.commit()
            flash('Dog deleted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error deleting dog {0}: {1}'.format(dog_name, str(e)), 'error')

    return render_template('delete.html', user=user, dog=dog)


###################################################
#                UPDATE METHOD                    #
###################################################
@app.route('/update_dog/<dog_name>', methods=['GET', 'POST'])
def update_dog(dog_name):
    # Fetch user details
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    dog = db.session.query(Dog).filter(Dog.name == dog_name).first()

    if request.method == 'POST':
        updated_dog = db.session.query(Dog).filter(Dog.name == dog_name).first()
        try:
            # Validate form data
            age = int(request.form['age'])
            competitions = int(request.form['competitions'])

            updated_dog.name = request.form['name']
            updated_dog.age = age
            updated_dog.breed = request.form['breed']
            updated_dog.colour = request.form['colour']
            updated_dog.activity = request.form['activity']
            updated_dog.maintenance = request.form['maintenance']
            updated_dog.competitions = competitions
            updated_dog.disqualified = request.form['disqualified']
            db.session.commit()

            print('Dog {0} was successfully updated'.format(updated_dog.name))
            flash('Dog {0} was successfully updated'.format(updated_dog.name), 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error updating dog {0}: {1}'.format(dog_name, str(e)), 'error')

    return render_template('update.html', user=user, dog=dog)


@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    # Fetch user
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    if request.method == 'POST':
        try:
            user.user = request.form['user']
            user.user_email = request.form['user_email']
            user.user_password = request.form['user_password']
            db.session.commit()

            print('User {0} was successfully updated'.format(user.user))
            flash('User {0} was successfully updated'.format(user.user), 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error updating user {0}: {1}'.format(user.user, str(e)), 'error')

    return render_template('update_user.html', user=user)


###################################################
#               INCREMENT METHOD                  #
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
#             INCREMENT AGE METHOD                #
###################################################
# @app.route('/increment_age', methods=['GET', 'POST'])
# def increment_age():
#     if request.method == 'POST':
#         dog_name = request.form.get('name')
#         if not dog_name:
#             print("increment_age() error")
#             flash('Flash increment_age() error\n'
#                   'Please enter the dog\'s name to increment age', 'error')
#             return redirect(url_for('get_all'))
#
#         try:
#             dog = get_dog_by_name(dog_name)
#             increment(dog, 'age')
#             return redirect(url_for('get_all'))
#         except Exception as e:
#             print(f"increment_age() error: {str(e)}")
#             flash('Flash increment_age() error', 'error')
#             return redirect(url_for('get_all'))
#
#     return render_template('increment_age2.html', dog=)


###################################################
#        INCREMENT COMPETITIONS METHOD            #
###################################################
# @app.route('/increment_competitions', methods=['GET', 'POST'])
# def increment_competitions():
#     if request.method == 'POST':
#         dog_name = request.form.get('name')
#         if not dog_name:
#             print("increment_competitions() error")
#             flash('Flash increment_competitions() error\n'
#                   'Please enter the dog\'s name to increment competitions', 'error')
#             return redirect(url_for('get_all'))
#
#         try:
#             dog = get_dog_by_name(dog_name)
#             increment(dog, 'competitions')
#             return redirect(url_for('get_all'))
#         except Exception as e:
#             print(f"increment_competitions() error: {str(e)}")
#             flash('Flash increment_competitions() error', 'error')
#             return redirect(url_for('get_all'))
#
#     return render_template('increment_competitions2.html', dog=dog)


###################################################
#                 GET ALL DOGS                    #
###################################################
@app.route('/get_all', methods=['GET', 'POST'])
def get_all():
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    all_dogs = Dog.query.all()
    return render_template('get_all.html', user=user, dogs=all_dogs)


###################################################
#                  ADD NEW DOG                    #
###################################################
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Get the user ID from the session
    user_id = session.get('user_id')
    if not user_id:
        print("add() error: user not logged in")
        flash('add() error: User not logged in', 'error')
        return redirect(url_for('login'))

    # Retrieve user information for later use in rendering the template
    user = db.session.query(User).get(user_id)

    if request.method == 'POST':
        try:
            # Validate that all required form fields are present
            required_fields = ['name', 'age', 'sex', 'breed', 'colour', 'activity', 'maintenance',
                               'competitions', 'disqualified']
            for field in required_fields:
                if not request.form.get(field):
                    print("add() error, all fields must be filled")
                    flash(f'add() error\nPlease enter {field}', 'error')
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
            new_dog = Dog(
                user_id=user_id,
                name=request.form['name'],
                age=age,
                sex=request.form['sex'],
                breed=request.form['breed'],
                colour=request.form['colour'],
                activity=request.form['activity'],
                maintenance=request.form['maintenance'],
                competitions=competitions,
                disqualified=request.form['disqualified'],
            )

            # Add new dog to the database
            db.session.add(new_dog)
            db.session.commit()

            flash('Dog {0} added successfully!'.format(new_dog.name))
            return redirect(url_for('index'))
        except Exception as e:
            print(f"add() error: {str(e)}")
            flash('flash add() error:', 'error')
            return redirect(url_for('add'))
    return render_template('add.html', user=user)


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('logout.html')


if __name__ == '__main__':
    create_tables()
    add_initial_data()

    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
