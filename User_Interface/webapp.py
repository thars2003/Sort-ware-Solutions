import os
from flask import Flask, render_template
from flask import send_from_directory

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    # Pass data to template
    title = "Welcome to Flask"
    message = "Hello, this is your starting template!"
    return render_template("home.html", title=title, message=message)

if __name__ == "__main__":
    app.run(debug=True)