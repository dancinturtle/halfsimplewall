from wall import app
from wall.config.mysqlconnection import connectToMySQL



class Message:

    def index(self):
        result = mysql.query_db("SELECT message, messages.id, messages.created_at, first_name FROM messages JOIN users ON messages.user_id = users.id ORDER BY created_at DESC;")
        comments = mysql.query_db("SELECT comment, comments.created_at, first_name, message_id, comments.id from comments JOIN users ON comments.user_id = users.id ORDER BY created_at DESC;")
        return (result, comments)

    def create(self, newmessage, userid):
        if len(newmessage['message']) > 3:
            query = "INSERT INTO messages (user_id, message, created_at) VALUES (%(user_id)s, %(message)s, NOW());"
            data = {"user_id" : userid, "message" : newmessage['message'] }
            result = mysql.query_db(query, data)
            if result:
                return (True, result)
            else:
                return (False, "error")
        return (False, "length")
    
    def comment(self, newcomment, userid):
        if len(newcomment['comment']) > 3:
            query = "INSERT INTO comments (message_id, user_id, created_at, comment) VALUES (%(message_id)s, %(user_id)s, NOW(), %(comment)s);"
            data = {"message_id" : newcomment['messageid'], "user_id" : userid, "comment" : newcomment['comment']}
            result = mysql.query_db(query, data)
            if result:
                return (True, result)
            else:
                return (False, "error")
        return False("length")