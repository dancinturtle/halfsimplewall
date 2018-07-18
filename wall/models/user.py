from wall import app
from wall.config.mysqlconnection import connectToMySQL
mysql = connectToMySQL()
import re
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:

    def create(self, data):
       
    
    def retrieveOneByEmail(self, data):
        print("using this data", data['password'])
        query = "SELECT * FROM users WHERE email = %(email)s"
        emaildata = {"email" : data['email']}
        result = mysql.query_db(query, emaildata)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], data['password']):
                print("checked out")
                return (True, result[0]['first_name'], result[0]['id'])
            else:
                print("nope")
                return (False, False)
        else: 
            return (False, False)
        return result