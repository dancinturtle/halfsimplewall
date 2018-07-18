from flask import render_template, redirect, flash, session
from simpleWall import app
app.secret_key = "rainbowswithapotofgold"
from simpleWall.models.user import User
user = User()


class Users:
    def index(self):
        if 'userid' in session:
            print("The user's id:", session['userid'])
        return render_template("index.html")
    def create(self, data):
        result = user.create(data)
        if result[0] == True:
            session['username'] = data['first_name']
            session['userid'] = result[1]
            flash("You have been successfully registered!", "success")
            return redirect('/success')
        for error in result[1]:
            flash(error[0], error[1])
        flash(data['first_name'], "badfirst")
        flash(data['last_name'], "badlast")
        flash(data['email'], "bademail")
        return redirect("/")
    def login(self, form_data):
        result = user.login(form_data)
        if result[0] == True:
            session['userid'] = result[1]['id']
            session['username'] = result[1]['first_name']
            return redirect('/success')
        flash(result[1], "login")
        return redirect('/')
    def logout(self):
        session.clear()
        flash("You have been logged out", "register")
        return redirect('/')


