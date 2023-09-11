from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def received_data():
    if request.method == "POST":
        return f"Name: {request.form['username']} and Password: {request.form['password']}"


if __name__ == '__main__':
    app.run(debug=True)
