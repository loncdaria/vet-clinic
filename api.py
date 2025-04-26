from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

# Importuj bazę danych oraz modele z models.py
from models import db, User, Owner, Pet, Vet, Appointment

# Tworzymy blueprint o prefiksie /api
api = Blueprint('api', __name__, url_prefix='/api')

# ------------------------------------------------------------------------------
# Endpoint logowania - zwraca token JWT, jeśli dane logowania są poprawne
# ------------------------------------------------------------------------------
@api.route('/login_token', methods=['POST'])
def login_token():
    data = request.get_json()
    if not data or 'name' not in data or 'password' not in data:
        return jsonify({'msg': 'Brakuje danych logowania (name i password)'}), 400

    user = User.query.filter_by(name=data['name']).first()
    if user and user.verify_password(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Niepoprawne dane logowania'}), 401

# Przykładowy endpoint chroniony, który zwraca dane użytkownika z tokenu

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({'logged_in_as': current_user_id}), 200

# ------------------------------------------------------------------------------
# Endpointy dla zasobu Owner (Właściciel)
# ------------------------------------------------------------------------------

# Pobranie listy wszystkich właścicieli
@api.route('/owners', methods=['GET'])
@jwt_required()
def get_owners():
    owners = Owner.query.all()
    owners_list = []
    for owner in owners:
        owners_list.append({
            'id': owner.id,
            'name': owner.name,
            'lastName': owner.lastName,
            'mail': owner.mail,
            'birthDate': owner.birthDate
        })
    return jsonify(owners_list), 200

# Pobranie szczegółów właściciela po ID
@api.route('/owners/<int:owner_id>', methods=['GET'])
@jwt_required()
def get_owner(owner_id):
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404
    owner_data = {
        'id': owner.id,
        'name': owner.name,
        'lastName': owner.lastName,
        'mail': owner.mail,
        'birthDate': owner.birthDate
    }
    return jsonify(owner_data), 200

# Utworzenie nowego właściciela
@api.route('/owners', methods=['POST'])
@jwt_required()
def create_owner():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        owner = Owner(
            name=data['name'],
            lastName=data['lastName'],
            mail=data['mail'],
            birthDate=data['birthDate']
        )
        db.session.add(owner)
        db.session.commit()
        return jsonify({'message': 'Owner created', 'id': owner.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Aktualizacja właściciela
@api.route('/owners/<int:owner_id>', methods=['PUT'])
@jwt_required()
def update_owner(owner_id):
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        owner.name = data.get('name', owner.name)
        owner.lastName = data.get('lastName', owner.lastName)
        owner.mail = data.get('mail', owner.mail)
        owner.birthDate = data.get('birthDate', owner.birthDate)
        db.session.commit()
        return jsonify({'message': 'Owner updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Usunięcie właściciela
@api.route('/owners/<int:owner_id>', methods=['DELETE'])
@jwt_required()
def delete_owner(owner_id):
    owner = Owner.query.get(owner_id)
    if owner is None:
        return jsonify({'error': 'Owner not found'}), 404

    try:
        db.session.delete(owner)
        db.session.commit()
        return jsonify({'message': 'Owner deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------------------------------
# Endpointy dla zasobu Vet (Weterynarz)
# ------------------------------------------------------------------------------

# Pobranie listy wszystkich weterynarzy
@api.route('/vets', methods=['GET'])
@jwt_required()
def get_vets():
    vets = Vet.query.all()
    vets_list = []
    for vet in vets:
        vets_list.append({
            'id': vet.id,
            'name': vet.name,
            'lastName': vet.lastName,
            'mail': vet.mail,
            'birthDate': vet.birthDate
        })
    return jsonify(vets_list), 200

# Pobranie szczegółów weterynarza
@api.route('/vets/<int:vet_id>', methods=['GET'])
@jwt_required()
def get_vet(vet_id):
    vet = Vet.query.get(vet_id)
    if vet is None:
        return jsonify({'error': 'Vet not found'}), 404
    vet_data = {
        'id': vet.id,
        'name': vet.name,
        'lastName': vet.lastName,
        'mail': vet.mail,
        'birthDate': vet.birthDate
    }
    return jsonify(vet_data), 200

# Utworzenie nowego weterynarza
@api.route('/vets', methods=['POST'])
@jwt_required()
def create_vet():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        vet = Vet(
            name=data['name'],
            lastName=data['lastName'],
            mail=data['mail'],
            birthDate=data['birthDate']
        )
        db.session.add(vet)
        db.session.commit()
        return jsonify({'message': 'Vet created', 'id': vet.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Aktualizacja danych weterynarza
@api.route('/vets/<int:vet_id>', methods=['PUT'])
@jwt_required()
def update_vet(vet_id):
    vet = Vet.query.get(vet_id)
    if vet is None:
        return jsonify({'error': 'Vet not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        vet.name = data.get('name', vet.name)
        vet.lastName = data.get('lastName', vet.lastName)
        vet.mail = data.get('mail', vet.mail)
        vet.birthDate = data.get('birthDate', vet.birthDate)
        db.session.commit()
        return jsonify({'message': 'Vet updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Usunięcie weterynarza
@api.route('/vets/<int:vet_id>', methods=['DELETE'])
@jwt_required()
def delete_vet(vet_id):
    vet = Vet.query.get(vet_id)
    if vet is None:
        return jsonify({'error': 'Vet not found'}), 404

    try:
        db.session.delete(vet)
        db.session.commit()
        return jsonify({'message': 'Vet deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------------------------------
# Endpointy dla zasobu Pet (Zwierzę)
# ------------------------------------------------------------------------------

# Pobranie listy wszystkich zwierząt
@api.route('/pets', methods=['GET'])
@jwt_required()
def get_pets():
    pets = Pet.query.all()
    pets_list = []
    for pet in pets:
        pets_list.append({
            'id': pet.id,
            'ownerId': pet.ownerId,
            'name': pet.name,
            'species': pet.species,
            'weight': pet.weight
        })
    return jsonify(pets_list), 200

# Pobranie szczegółów konkretnego zwierzęcia
@api.route('/pets/<int:pet_id>', methods=['GET'])
@jwt_required()
def get_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404
    pet_data = {
        'id': pet.id,
        'ownerId': pet.ownerId,
        'name': pet.name,
        'species': pet.species,
        'weight': pet.weight
    }
    return jsonify(pet_data), 200

# Utworzenie nowego zwierzęcia
@api.route('/pets', methods=['POST'])
@jwt_required()
def create_pet():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        pet = Pet(
            ownerId=data['ownerId'],
            name=data['name'],
            species=data['species'],
            weight=data['weight']
        )
        db.session.add(pet)
        db.session.commit()
        return jsonify({'message': 'Pet created', 'id': pet.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Aktualizacja danych zwierzęcia
@api.route('/pets/<int:pet_id>', methods=['PUT'])
@jwt_required()
def update_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        pet.ownerId = data.get('ownerId', pet.ownerId)
        pet.name = data.get('name', pet.name)
        pet.species = data.get('species', pet.species)
        pet.weight = data.get('weight', pet.weight)
        db.session.commit()
        return jsonify({'message': 'Pet updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Usunięcie zwierzęcia
@api.route('/pets/<int:pet_id>', methods=['DELETE'])
@jwt_required()
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        return jsonify({'error': 'Pet not found'}), 404

    try:
        db.session.delete(pet)
        db.session.commit()
        return jsonify({'message': 'Pet deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------------------------------------------------
# Endpointy dla zasobu Appointment (Wizyta)
# ------------------------------------------------------------------------------

# Pobranie listy wszystkich wizyt
@api.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments = Appointment.query.all()
    appointments_list = []
    for app in appointments:
        appointments_list.append({
            'id': app.id,
            'ownerId': app.ownerId,
            'vetId': app.vetId,
            'date': app.date,
            'time': app.time
        })
    return jsonify(appointments_list), 200

# Pobranie szczegółów konkretnej wizyty
@api.route('/appointments/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404
    appointment_data = {
        'id': appointment.id,
        'ownerId': appointment.ownerId,
        'vetId': appointment.vetId,
        'date': appointment.date,
        'time': appointment.time
    }
    return jsonify(appointment_data), 200

# Utworzenie nowej wizyty
@api.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        appointment = Appointment(
            ownerId=data['ownerId'],
            vetId=data['vetId'],
            date=data['date'],
            time=data['time']
        )
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment created', 'id': appointment.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Aktualizacja danych wizyty
@api.route('/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        appointment.ownerId = data.get('ownerId', appointment.ownerId)
        appointment.vetId = data.get('vetId', appointment.vetId)
        appointment.date = data.get('date', appointment.date)
        appointment.time = data.get('time', appointment.time)
        db.session.commit()
        return jsonify({'message': 'Appointment updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Usunięcie wizyty
@api.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404

    try:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
