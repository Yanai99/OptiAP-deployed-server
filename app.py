
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
<<<<<<< HEAD
    return 'Hello from Flask!'

=======
    return "<p>Hello World!</p>"

@app.route("/health")
def health():
    return "<p>everythings Great!</p>"
>>>>>>> dcb6dd9a3557f0cdc6621b16bc1f2cf302896e10
