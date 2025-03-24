from datetime import date, timedelta
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, nullable=False)
    vetId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)


class Owner(db.Model):
    __tablename__ = 'owner'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    birthDate = db.Column(db.Integer(), nullable=False)

class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    species = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)

class Vet(db.Model):
    __tablename__ = 'vet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    birthDate = db.Column(db.Integer(), nullable=False)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/all/")
def owners():
    owners = db.session.execute(db.select(Owner).order_by(Owner.name)).scalars()
    return render_template("Owners.html", owners=owners)


@app.route("/vets/")
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