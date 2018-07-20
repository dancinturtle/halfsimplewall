from flask import render_template, redirect, flash, session
from simpleWall import app
app.secret_key = "rainbowswithapotofgold"
from simpleWall.models.message import Message
from simpleWall.models.user import User
message = Message()
user = User()

class Messages:
    def checklogin(self):
        if 'userid' not in session:
            flash("You must be logged in to enter this website", "register")
            return False
        return True
    def index(self):
        if self.checklogin() == False:    
            return redirect('/')
        sentMessages = user.getUser(session['userid'])
        count = message.totalMessages(session['userid'])
        messages = message.getMessages(session['userid'])
        result = message.getUsers(session['userid'])
        print("sent messages", sentMessages)
        print("count", count)
        print("messages", messages)
        print("result", result)
        return render_template("wall.html", array = [1,2,3,4,5], users = result, messages = messages, count = count[0], sent = sentMessages[0]['sent'])
    def create(self, data):
        if self.checklogin() == False:
            return redirect('/')
        result = message.create(data, session['userid'])
        if result[0]==True:
            message.addSent(session['userid'])
            flash("Your message was sent", "success")
        else: 
            for error in result[1]:
                flash(error[0], error[1])
        return redirect("/success")

    def delete(self, id):
        result = message.delete(id, session['userid'])
        if result == True:
            return redirect("/success")
        return render_template("boo.html")
