from flask import Flask
from os import environ

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def say_hi(): # does it matter what these functions that are returning views are named?
    return "Hello World"

@app.route("/hello/<name>") # what is the term for whats inside < > ? its not interpolation...
def hi_person(name):
    html = """
        <h1>
            Hello {}!
        </h1>
        <p>
            Here's a picture of a kitten.  Awww...
        </p>
        <img src="http://placekitten.com/g/200/300">
    """
    return html.format(name.title())
    # return "Hello {}!".format(name.title()) :: default behavior is to return html and 200

@app.route("/jedi/<first>/<last>")
def some_test(first, last):
    ending = last[:3]
    beginning = first[:2]
    return "{}".format(ending + beginning)

if __name__ == "__main__":
    app.debug = True
    app.run('0.0.0.0')
