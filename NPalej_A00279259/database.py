from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogs.sqlite3'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)

    def __init__(self, user, user_email, user_password):
        self.user = user
        self.user_email = user_email
        self.user_password = user_password


class Dog(db.Model):
    __tablename__ = 'dog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(25))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(25))
    breed = db.Column(db.String(15))
    colour = db.Column(db.String(25))
    activity = db.Column(db.String(25))
    maintenance = db.Column(db.String(25))
    competitions = db.Column(db.Integer)
    disqualified = db.Column(db.String(50))

    def __init__(self, name, age, sex, breed, colour, activity, maintenance, competitions, disqualified):
        self.name = name
        self.age = age
        self.sex = sex
        self.breed = breed
        self.colour = colour
        self.activity = activity
        self.maintenance = maintenance
        self.competitions = competitions
        self.disqualified = disqualified


# Order in which tables are created, user first and then dog
db.create_all()


@app.route('/initial_table_data', methods=['GET', 'POST'])
def initial_table_data():
    if request.method == 'POST':
        # Creating Users
        natalia = User(user='Natalia', user_email='natalia@gmail.com', user_password='natalia')
        monika = User(user='Monika', user_email='monika@gmail.com', user_password='monika')
        dominik = User(user='Dominik', user_email='dominik@gmail.com', user_password='dominik')
        kasia = User(user='Kasia', user_email='kasia@gmail.com', user_password='kasia')
        adrian = User(user='Adrian', user_email='adrian@gmail.com', user_password='adrian')

        db.session.add_all([natalia, monika, dominik, kasia, adrian])
        db.session.commit()

        # Creating Dogs
        db.session.add(Dog(name='Lilly', age=3, sex='Female', breed='Yorkshire Terrier',
                           colour='Tan-Silver', activity='High', maintenance='High', competitions=2,
                           disqualified='No'))
        db.session.add(Dog(name='Gizmo', age=9, sex='Male', breed='Shi Tzu',
                           colour='Black-White', activity='Low', maintenance='Medium', competitions=0,
                           disqualified='No'))
        db.session.add(Dog(name='Luna', age=3, sex='Female', breed='Cavapoo',
                           colour='Light-Brown', activity='Medium', maintenance='Medium', competitions=1,
                           disqualified='No'))
        db.session.add(Dog(name='Coco', age=3, sex='Male', breed='Cockpoo',
                           colour='Dark-Brown', activity='High', maintenance='Medium', competitions=2,
                           disqualified='No'))
        db.session.add(Dog(name='Lola', age=1, sex='Female', breed='Yorkshire Terrier',
                           colour='Silver-Tan', activity='High', maintenance='Very High', competitions=0,
                           disqualified='No'))
        db.session.commit()

    return render_template('initial_table_data.html')


@app.route('/view_database')
def view_database():
    # Query all records from the User and Dog tables using the SQLAlchemy ORM
    users = User.query.all()
    dogs = Dog.query.all()

    return render_template('view_database.html', users=users, dogs=dogs)
