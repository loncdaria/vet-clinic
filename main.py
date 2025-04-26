from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from urllib.parse import urlparse, urljoin
from flask_jwt_extended import JWTManager
from api import api

from models import db, User, Owner, Pet, Vet, Appointment




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"# tu nie wiem czy utworzyć plik config.cfg czy w osobnym pliku
app.config['SECRET_KEY'] = 'Kiki'
app.config['JWT_SECRET_KEY'] = 'Kiki'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
migrate = Migrate(app, db)
jwt = JWTManager(app)
app.register_blueprint(api)

db.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

class LoginForm(FlaskForm):
    name=StringField('User name')
    password=PasswordField('Password')
    remember=BooleanField('Remember me')

@app.route('/init')
def init():
    db.create_all()
    
    admin=User.query.filter(User.name=='admin').first()
    if admin== None:
        admin = User(id=1, name='admin', password=User(password='admin').get_hash_password(), first_name='admin', last_name='admin')
        db.session.add(admin)
        db.session.commit()
    return 'OK'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.name == form.name.data).first()
        if user is not None and user.verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next = request.args.get('next')
            if next and is_safe_url(next):
                return redirect(next)
            else:
                return '<h1>Logged in successfully</h1>'
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return "<h1>Logged out successfully</h1>"
    


@app.route("/all/")
@login_required
def owners():
    owners = db.session.execute(db.select(Owner).order_by(Owner.name)).scalars()
    return render_template("Owners.html", owners=owners)


@app.route("/vets/")
@login_required
def vets():
    vets = db.session.execute(db.select(Vet).order_by(Vet.name)).scalars()
    return render_template("Vets.html", vets=vets)


@app.route("/all/Appointments/")
def appointments():
    appointments = [r for r in db.session.execute(db.select(Appointment).order_by(Appointment.id)).scalars()]
    owners = [b for b in db.session.execute(db.select(Owner).order_by(Owner.name)).scalars()]
    vets = [c for c in db.session.execute(db.select(Vet).order_by(Vet.name)).scalars()]
    return render_template("Appointments.html", appointments=appointments, vets=vets, owners=owners)


@app.route("/all/Add")
def addOwners():
    return render_template("AddOwner.html")

@app.route("/all/Pet")
def addPets():
    owners = [b for b in db.session.execute(db.select(Owner).order_by(Owner.name)).scalars()]
    return render_template("AddPet.html", owners=owners)

@app.route("/all/Pets/")
def pets():
    pets = [p for p in db.session.execute(db.select(Pet).order_by(Pet.id)).scalars()]
    owners = [o for o in db.session.execute(db.select(Owner).order_by(Owner.name)).scalars()]
    return render_template("Pets.html", pets=pets, owners=owners)

@app.route("/all/Appointment")
def addAppointment():
    owners = db.session.execute(db.select(Owner).order_by(Owner.name)).scalars()
    vets = db.session.execute(db.select(Vet).order_by(Vet.name)).scalars()
    return render_template("AddAppointment.html", vets=vets, owners=owners)


@app.route("/vets/Add")
def addVets():
    return render_template("AddVet.html")


@app.route("/add_owner", methods=["GET", "POST"])
def add_owner():
    if request.method == "POST":
        name = request.form['name']
        lastName = request.form['lastName']
        mail = request.form['mail']
        birthDate = request.form['birthDate']
        owner = Owner(
            name=name,
            lastName=lastName,
            mail=mail,
            birthDate=birthDate,
        )
        db.session.add(owner)
        db.session.commit()
        return redirect("/all")
    return redirect("/all")


@app.route('/delete', methods=['POST'])
def delete_owner():
    owner_id = request.form['owner_to_delete']
    Owner.query.filter_by(id=owner_id).delete()
    db.session.commit()
    return redirect('all')

@app.route("/add_pet", methods=["GET", "POST"])
def add_pet():
    if request.method == "POST":
        owner_id = request.form.get('owners_select')
        name = request.form['name']
        species = request.form['species']
        weight = request.form['weight']
        pet = Pet(
            ownerId=owner_id,
            name=name,
            species=species,
            weight=weight,
        )
        db.session.add(pet)
        db.session.commit()
        return redirect("/all/Pets")
    return redirect("/all/Pets")


@app.route('/delete2', methods=['POST'])
def delete_pet():
    pet_id = request.form['pet_to_delete']
    Pet.query.filter_by(id=pet_id).delete()
    db.session.commit()
    return redirect('all/Pets')



@app.route("/add_vet", methods=["GET", "POST"])
def add_vet():
    if request.method == "POST":
        name = request.form['name']
        lastName = request.form['lastName']
        mail = request.form['mail']
        birthDate = request.form['birthDate']
        vet = Vet(
            name=name,
            lastName=lastName,
            mail=mail,
            birthDate=birthDate,
        )
        db.session.add(vet)
        db.session.commit()
        return redirect("/vets")
    return redirect("/vets")


@app.route('/delete1', methods=['POST'])
def delete_vet():
    vet_id = request.form['vet_to_delete']
    Vet.query.filter_by(id=vet_id).delete()
    db.session.commit()
    return redirect('/vets')


@app.route("/add_appointment", methods=["GET", "POST"])
def add_appointment():
    if request.method == "POST":
        vet_id = request.form.get('vets_select')
        owner_id = request.form.get('owners_select')
        date = request.form['days']
        time = request.form['time']
        # Create appointment object
        appointment = Appointment(
            ownerId=owner_id,
            vetId=vet_id,
            date=date,
            time=time,
        )

        # Add appointment to the database
        db.session.add(appointment)
        db.session.commit()
        return redirect('/all')
    return redirect('/all')



if __name__ == "__main__":
    app.run(port=5005, debug=True)