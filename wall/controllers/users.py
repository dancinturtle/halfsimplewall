from wall import app
from flask import render_template, redirect, flash, session

from wall.models.user import User
user = User()

class Users:
    def index(self):
        return render_template("index.html")
    def create(self, newuser):
        result = user.create(newuser)
        print("The response", result)
        if result[0]==False:
            for error in result[1]:
                flash(error, "register")
        else:
            flash("You've been successfully registered", "success")
            session['username']=newuser['first_name']
            session['userid'] = result[1]
            return redirect('/wall')
        return redirect("/")
    
    def logout(self):
       
