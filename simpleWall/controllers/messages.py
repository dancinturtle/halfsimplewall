from flask import render_template, redirect, flash, session
from simpleWall import app
app.secret_key = "rainbowswithapotofgold"
from simpleWall.models.message import Message
message = Message()

class Messages:
    def checklogin(self):
        if 'userid' not in session:
            flash("You must be logged in to enter this website", "register")
            return False
        return True
    def index(self):
        if self.checklogin() == False:    
            return redirect('/')
        result = message.getUsers(session['userid'])
        return render_template("wall.html", users = result)
    def create(self, data):
        if self.checklogin() == False:
            return redirect('/')
        result = message.create(data, session['userid'])
        if result[0]==True:
            flash("Your message was sent", "success")
        else: 
            for error in result[1]:
                flash(error[0], error[1])
        return redirect("/success")
