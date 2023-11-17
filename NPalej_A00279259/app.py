import os
from flask import Flask, request, flash, url_for, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, func

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

    @classmethod
    def count_users(cls):
        return cls.query.count()


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

    @classmethod
    def count_dogs(cls):
        return cls.query.count()


def create_tables():
    db.create_all()


def add_initial_data():
    # Create initial users and dogs
    natalia = User(user='Natalia', user_email='natalia@gmail.com', user_password='natalia')
    monika = User(user='Monika', user_email='monika@gmail.com', user_password='monika')
    dominik = User(user='Dominik', user_email='dominik@gmail.com', user_password='dominik')
    kasia = User(user='Kasia', user_email='kasia@gmail.com', user_password='kasia')
    adrian = User(user='Adrian', user_email='adrian@gmail.com', user_password='adrian')
    john = User(user='John', user_email='john@gmail.com', user_password='john')
    anna = User(user='Anna', user_email='anna@gmail.com', user_password='anna')
    michael = User(user='Michael', user_email='michael@gmail.com', user_password='michael')
    sophie = User(user='Sophie', user_email='sophie@gmail.com', user_password='sophie')
    david = User(user='David', user_email='david@gmail.com', user_password='david')
    users = [natalia, monika, dominik, kasia, adrian, john, anna, michael, sophie, david]
    db.session.add_all(users)
    db.session.commit()

    dogs = [
        Dog(user_id=natalia.id, name='Lilly', age=3, sex='Female', breed='Yorkshire Terrier', colour='Tan-Silver',
            activity='High', maintenance='High', competitions=2, disqualified='No'),
        Dog(user_id=monika.id, name='Gizmo', age=9, sex='Male', breed='Shi Tzu', colour='Black-White',
            activity='Low', maintenance='Medium', competitions=4, disqualified='Yes'),
        Dog(user_id=dominik.id, name='Luna', age=3, sex='Female', breed='Cavapoo', colour='Light-Brown',
            activity='Medium', maintenance='Medium', competitions=1, disqualified='No'),
        Dog(user_id=kasia.id, name='Coco', age=3, sex='Male', breed='Cockapoo', colour='Dark-Brown',
            activity='High', maintenance='Medium', competitions=2, disqualified='Yes'),
        Dog(user_id=adrian.id, name='Lola', age=1, sex='Female', breed='Yorkshire Terrier', colour='Silver-Tan',
            activity='High', maintenance='Very High', competitions=0, disqualified='No'),
        Dog(user_id=natalia.id, name='Saba', age=13, sex='Female', breed='Boxer', colour='Black-Brown',
            activity='Low', maintenance='Low', competitions=0, disqualified='No'),
        Dog(user_id=john.id, name='Max', age=3, sex='Male', breed='Poodle', colour='White', activity='High',
            maintenance='Medium', competitions=2, disqualified='Yes'),
        Dog(user_id=anna.id, name='Rocky', age=7, sex='Male', breed='Bulldog', colour='Brindle', activity='Low',
            maintenance='High', competitions=0, disqualified='No'),
        Dog(user_id=michael.id, name='Mia', age=1, sex='Female', breed='Dachshund', colour='Red', activity='Medium',
            maintenance='Low', competitions=1, disqualified='No'),
        Dog(user_id=sophie.id, name='Charlie', age=4, sex='Male', breed='Shiba Inu', colour='Red-Sesame',
            activity='High', maintenance='Medium', competitions=3, disqualified='No'),
        Dog(user_id=david.id, name='Sophie', age=5, sex='Female', breed='Cocker Spaniel', colour='Buff',
            activity='Medium', maintenance='High', competitions=2, disqualified='No'),
        Dog(user_id=monika.id, name='Buddy', age=5, sex='Male', breed='Golden Retriever', colour='Golden',
            activity='High', maintenance='Medium', competitions=3, disqualified='No'),
        Dog(user_id=dominik.id, name='Oscar', age=2, sex='Male', breed='Labrador Retriever', colour='Chocolate',
            activity='Medium', maintenance='High', competitions=1, disqualified='No'),
        Dog(user_id=kasia.id, name='Milo', age=4, sex='Male', breed='Beagle', colour='Tricolor', activity='Medium',
            maintenance='Low', competitions=2, disqualified='Yes'),
        Dog(user_id=adrian.id, name='Lucy', age=6, sex='Female', breed='German Shepherd', colour='Black-Tan',
            activity='High', maintenance='High', competitions=4, disqualified='No')
    ]
    db.session.add_all(dogs)
    db.session.commit()


###################################################
#                    ROUTES                       #
###################################################
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'Login' in request.form:
        user_email = request.form['user_email']
        user_password = request.form['user_password']

        # Find user with the provided email and password
        user = db.session.query(User).filter_by(user_email=user_email, user_password=user_password).first()
        if user:
            # Set session
            session['user_id'] = user.id
            flash('Login successful !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    elif 'Register' in request.form:
        return redirect(url_for('register'))
    return render_template('login.html')


###################################################
#               REGISTER METHOD                   #
###################################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Calling class methods to get counts
    users_count_value = User.count_users()
    dogs_count_value = Dog.count_dogs()

    if request.method == 'POST':
        # Validate required fields are filled
        required_fields = ['user', 'user_email', 'user_password']
        for field in required_fields:
            if not request.form.get(field):
                flash(f'Flash register() error\nPlease enter {field}', 'error')
                return redirect(url_for('register'))

        # Check if the email already exists
        user_exists = db.session.query(User).filter_by(user_email=request.form['user_email']).first()
        if user_exists:
            flash('User with email "{0}" already exists. Please log in.'.format(user_exists), 'error')
            return redirect(url_for('login'))

        # Create a new user
        new_user = User(
            user=request.form['user'],
            user_email=request.form['user_email'],
            user_password=request.form['user_password']
        )
        # Add new user to the db
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login', success_message='200'))
    return render_template('register.html', users_count=users_count_value, dogs_count=dogs_count_value)


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

    try:
        if user_choice == 'Update':
            return redirect(url_for('update_dog', user=user, dog_name=selected_dog_name))
        elif user_choice == 'Delete':
            return redirect(url_for('delete_dog', user=user, dog_name=selected_dog_name))
    except Exception as e:
        flash('selected_dog() error: no dog selected {0}'.format(str(e)), 'error')
        return redirect(url_for('index'))


###################################################
#                DELETE METHOD                    #
###################################################
@app.route('/delete_dog/<dog_name>', methods=['GET', 'POST'])
def delete_dog(dog_name):
    # Fetch the dog based on name
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
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    dog = db.session.query(Dog).filter(Dog.name == dog_name).first()

    if request.method == 'POST':
        try:
            new_name = request.form.get('name')
            new_sex = request.form.get('sex')
            new_breed = request.form.get('breed')
            new_colour = request.form.get('colour')
            new_activity = request.form.get('activity')
            new_maintenance = request.form.get('maintenance')
            new_disqualified = request.form.get('disqualified')

            # Update fields only if they are not None
            if new_name is not None:
                dog.name = new_name
            if new_sex is not None:
                dog.sex = new_sex
            if new_breed is not None:
                dog.breed = new_breed
            if new_colour is not None:
                dog.colour = new_colour
            if new_activity is not None:
                dog.activity = new_activity
            if new_maintenance is not None:
                dog.maintenance = new_maintenance
            if new_disqualified is not None:
                dog.disqualified = new_disqualified
            db.session.commit()

            flash('Dog {0} was successfully updated'.format(dog.name), 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error updating dog {0}: {1}'.format(dog_name, str(e)), 'error')
    return render_template('update.html', user=user, dog=dog)


@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    if request.method == 'POST':
        try:
            user.user = request.form['user']
            user.user_email = request.form['user_email']
            user.user_password = request.form['user_password']
            db.session.commit()

            flash('User {0} was successfully updated'.format(user.user), 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash('Error updating user {0}: {1}'.format(user.user, str(e)), 'error')
    return render_template('update_user.html', user=user)


###################################################
#               INCREMENT METHOD                  #
###################################################
@app.route('/update_value/<int:dog_id>/<field>', methods=['POST'])
def update_value(dog_id, field):
    dog = db.session.query(Dog).filter(Dog.id == dog_id).first()
    user_choice = request.form.get('choice')

    if dog:
        if field == 'age':
            if user_choice == '+':
                dog.age += 1
                flash('{0}\' age was successfully stepped up'.format(dog.name), 'success')
            elif user_choice == '-' and dog.age > 0:
                dog.age -= 1
                flash('{0}\' age was successfully stepped down'.format(dog.name), 'success')
            else:
                flash('Age cannot be below zero.', 'error')

        if field == 'competitions':
            if user_choice == '+':
                dog.competitions += 1
                flash('{0}\' competitions number was successfully stepped up'.format(dog.name), 'success')
            elif user_choice == '-' and dog.competitions > 0:
                dog.competitions -= 1
                flash('{0}\' competitions number was successfully stepped down'.format(dog.name), 'success')
            else:
                flash('Competitions cannot be negative.', 'error')
        db.session.commit()
        return redirect(url_for('index'))
    else:
        flash('update_value() error dog {0} {1} doesnt exist'.format(dog_id, dog.name), 'error')


###################################################
#                   GET DOGS                      #
###################################################
@app.route('/get_all', methods=['GET', 'POST'])
def get_all():
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    all_dogs = Dog.query.all()
    return render_template('get_all.html', user=user, dogs=all_dogs)


@app.route('/get_by', methods=['GET', 'POST'])
def get_by():
    user_id = session.get('user_id')
    user = db.session.query(User).get(user_id)
    user_choice = request.form.get('choice')

    if request.method == 'POST':
        try:
            if user_choice == 'Search Dog':
                dog_name = request.form.get('name')
                get_dog = db.session.query(Dog).filter(func.lower(Dog.name) == func.lower(dog_name)).all()
                return render_template('get_all.html', get_dog=get_dog, user=user)
            elif user_choice == 'Search User':
                user_name = request.form.get('user')
                get_user = db.session.query(Dog).filter(Dog.user.has(func.lower(User.user) == func.lower(user_name))).all()
                return render_template('get_all.html', get_user=get_user, user=user)
        except Exception as e:
            flash('get_by() error: {0}'.format(str(e)), 'error')
            return redirect(url_for('index'))
    else:
        return render_template('get_all.html')


###################################################
#                  ADD NEW DOG                    #
###################################################
@app.route('/add', methods=['GET', 'POST'])
def add():
    user_id = session.get('user_id')
    if not user_id:
        flash('add() error: User not logged in', 'error')
        return redirect(url_for('login'))

    # Retrieve user info
    user = db.session.query(User).get(user_id)

    if request.method == 'POST':
        try:
            # Check that all required form fields are present
            required_fields = ['name', 'age', 'sex', 'breed', 'colour', 'activity', 'maintenance',
                               'competitions', 'disqualified']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'add() error\nPlease enter {field}', 'error')
                    return redirect(url_for('add'))

            try:
                age = int(request.form['age'])
                competitions = int(request.form['competitions'])
                if age < 0 or competitions < 0:
                    flash('Age and competitions must be positive numbers', 'error')
                    return redirect(url_for('add'))
            except ValueError:
                flash('ValueError: age and competitions must be numbers only', 'error')
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

            db.session.add(new_dog)
            db.session.commit()

            flash('Dog {0} added successfully!'.format(new_dog.name))
            return redirect(url_for('index'))
        except Exception as e:
            flash('flash add() error: {0}'.format(str(e)), 'error')
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
