from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def landing_page():
    return render_template("landing.html")

@app.route('/Librarian-Login', methods=["GET"])
def librarian_login():
    return render_template("librarian/login.html")

@app.route('/User-Login', methods=["GET"])
def User_login():
    return render_template("student/Ulogin.html")

app.run(debug=True)