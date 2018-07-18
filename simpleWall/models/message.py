from simpleWall import app
from simpleWall.config.mysqlconnection import connectToMySQL
mysql = connectToMySQL('simpleWall')

class Message:
    def create(self, form_data, user_id):
        errors = []
        if len(form_data['content']) < 1 or len(form_data['content']) > 140:
            errors.append(("Message can only be between 1 and 140 characters", "error"))
        if int(form_data['recipient']) == user_id:
            errors.append(("You may not send a message to yourself", "error"))
        if len(errors) == 0:
            query = "INSERT INTO messages (content, recipient_id, sender_id, created_at, updated_at) VALUES (%(content)s, %(r_id)s, %(s_id)s, NOW(), NOW());"
            data = {
                "content" : form_data["content"],
                "r_id": form_data["recipient"],
                "s_id": user_id
            }
            result = mysql.query_db(query, data)
            if result:
                return (True, result)
            errors.append(("We could not send this message at this time", "error"))
        return (False, errors)
    def getUsers(self, user_id):
        query = "SELECT * FROM users WHERE NOT id=%(user_id)s;"
        data = {
            'user_id' : user_id
        }
        result = mysql.query_db(query, data)
        return result

