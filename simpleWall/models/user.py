from flask_bcrypt import Bcrypt
import re
from simpleWall import app
bcrypt = Bcrypt(app)
from simpleWall.config.mysqlconnection import connectToMySQL
mysql = connectToMySQL('simpleWall')

class User:
    def create(self, data):
        passRegex = re.compile(r'^(?=.{8,15}$)(?=.*[A-Z])(?=.*[0-9]).*$')
        emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        nameRegex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')
        errors = []
        for key, value in data.items():
            if len(value)<1:
                errors.append(("This field is required", key))
        if data['email'] and not emailRegex.match(data['email']):
            errors.append(("Invalid email address", "email"))
        if data['password'] and not passRegex.match(data['password']):
            errors.append(("Password must contain a number, a capital letter, and be between 8-15 characters", "password"))
        if data['first_name'] and not nameRegex.match(data['first_name']): 
            errors.append(("First name must contain at least two letters and contain only letters", "first_name"))
        if data['last_name'] and not nameRegex.match(data['last_name']):
            errors.append(("Last name must contain at least two letters and contain only letters", "last_name"))
        if data['confirm'] and data['password'] != data['confirm']:
            errors.append(("Passwords must match", "confirm"))
        if len(errors) == 0:
            unique = mysql.query_db("SELECT * FROM users WHERE email = %s;", data['email'])
            if unique:
                errors.append(("This email has already been taken", "email"))
            else:
                pw_hash = bcrypt.generate_password_hash(data['password'])
                query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s, NOW());"
                newuser = {"first_name" : data["first_name"],
                            "last_name" : data["last_name"],
                            "email" : data["email"],
                            "pw_hash" : pw_hash}
                created = mysql.query_db(query, newuser)
                if created:
                    return (True, created)
                else:
                    errors.append(("We're sorry, you could not be registered at this moment", "register"))
        return (False, errors)
    def login(self, form_data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {"email" : form_data['email']}
        result = mysql.query_db(query, data)
        if result:
            if bcrypt.check_password_hash(result[0]['pw_hash'], form_data['password']):
                return (True, result[0])
        return (False, "You could not be logged in")


