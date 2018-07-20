from flask import Flask, render_template, redirect, flash, session, request
from flask_bcrypt import Bcrypt
import re
from simpleWall import app
from simpleWall.controllers.users import Users
from simpleWall.controllers.messages import Messages
users = Users()
messages = Messages()
# app.secret_key = "rainbowswithapotofgold"
# bcrypt = Bcrypt(app)
# from simpleWall.config.mysqlconnection import connectToMySQL
# mysql = connectToMySQL('simpleWall')

@app.route("/")
def index():
    return users.index()

@app.route("/createUser", methods=['POST'])
def create():
    return users.create(request.form)

@app.route('/login', methods=['POST'])
def login():
    return users.login(request.form)

@app.route("/logout")
def logout():
    return users.logout()

@app.route('/success')
def wall():
    return messages.index()

@app.route('/message', methods=['POST'])
def createMessage():
    return messages.create(request.form)
@app.route('/messages/delete/<id>')
def delete(id):
    return messages.delete(id)
    