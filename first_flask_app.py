#
#
#
# FILE NEEDS TO BE RENAME app.py BEFORE IT CAN BE RUN WITH FLASK!!
#

from flask import Flask

# Create a new Python file called app.py. You should create this file in VS Code.

# Add the following to your code to create a new Flask instance called app
# This __name__ variable denotes the name of the current function.
# Variables with underscores before and after them are called magic methods in Python.
app = Flask(__name__)

# Create Flask Routes
# First, we need to define the starting point, also known as the root.
# The forward slash inside of the app.route denotes that we want to put our data at the root of our routes.
# The forward slash is commonly known as the highest level of hierarchy in any computer system.
@app.route('/')

# Whenever you make a route in Flask, you put the code you want in that specific route below @app.route()
def hello_world():
    return 'Hello world'

    a = range(100)
    for number in a:
        if number % 2 is 0:
            print(number)
        else:
            pass


'''
To run the app, we're first going to need to use the command line to navigate to the folder where we've saved our code.

If you are on a Windows computer, you will need to do the same thing, but in a slightly different way.
Start by opening up Anaconda Powershell. Once you've done that, enter this command.

set FLASK_APP=app.py

Now let's run our Flask app.
To do this, type the following command in your command line and press Enter:

flask run

When you run this command, you'll notice a line that says "Running on" followed by an address.
This should be your localhost address and a port number.
Any Flask application you create can have whatever port number you would like, but the most common is 5000.

Copy and paste your localhost address into your web browser.
Generally, a localhost will look something like this, for context.

localhost:5000
'''