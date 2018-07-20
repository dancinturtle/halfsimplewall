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
    def getMessages(self, user_id):
        query = "SELECT messages.id, content, first_name, messages.created_at FROM messages JOIN users ON sender_id = users.id WHERE recipient_id = %(recipient_id)s;"
        data = { "recipient_id" : user_id}
        result = mysql.query_db(query, data)
        return result
    def totalMessages(self, user_id):
        query = "SELECT COUNT(recipient_id) AS msgcount FROM messages WHERE recipient_id = %(recipient_id)s;"
        data = { "recipient_id" : user_id}
        result = mysql.query_db(query, data)
        return result
    def delete(self, id, user_id):
        findQuery = "SELECT * FROM messages WHERE id=%(message_id)s AND recipient_id=%(recipient_id)s;"
        data = {
            "message_id" : id,
            "recipient_id": user_id
        }
        found = mysql.query_db(findQuery, data)
        if found:
            query = "DELETE FROM messages WHERE id = %(message_id)s AND recipient_id = %(recipient_id)s;"
            mysql.query_db(query, data)
            return True
        return False
    def addSent(self, user_id):
        query = "UPDATE users SET sent = sent+1 WHERE id = %(user_id)s;"
        data = {
            "user_id" : user_id
        }
        mysql.query_db(query, data)
        return True

