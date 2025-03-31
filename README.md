# Vet-Clinic

## Project Description
Vet-Clinic is an application designed for veterinary clinic receptionists. Its main goal is to simplify scheduling appointments for clients and managing data about animals and their owners.

### Current Features:
- Logging into the system to access the application's functionalities.
- Adding animal owners.
- Adding animals to the system and assigning them to their owners.
- Adding veterinarians.
- Scheduling appointments by selecting the owner, animal, veterinarian, and setting the date and time.
- Viewing the list of animals.
- Viewing the list of appointments.

### Planned Features:
In the future, the application will be expanded to include:
- The ability to create accounts for clients.
- Clients' access to information about their animals, such as test results and visit history.
- Notifications for upcoming appointments.
- An advanced clinic data management system.

## Technologies
The project is built with Python. The technologies and libraries used include:
- Flask 
- Flask-SQLAlchemy 
- Flask-WTF 
- Flask-Login 
- Flask-Migrate 
- SQLite 
- Bootstrap
- HTML

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/loncdaria/vet-clinic.git
   ```
2. Navigate to the project directory:
   ```bash
   cd vet-clinic
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Initialize the database by running the following route once:
   ```bash
   http://localhost:5005/init
   ```
6. Run the application:
   ```bash
   python app.py
   ```

## Author
Project developed by [loncdaria](https://github.com/loncdaria).
