from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def new():
    return "Hello"

@app.route('/home')
def getEmployee():
    return "This is a home page"

from controller import user_controller