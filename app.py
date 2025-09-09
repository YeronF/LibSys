from flask import Flask, render_template, request, url_for
from models import User, Book, Rentals

app = Flask(__name__)

@app.route('/', methods=["GET"])
def landing_page():
    return render_template("landing.html")

@app.route('/librarian', methods=["GET", "POST"])
def librarian():
    return render_template("librarian/login.html")

@app.route('/user', methods=["GET", "POST"])
def user():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.get(user_id)
        if user and user.get('password') == password and user.get('role') == 'Student':
            return f"Welcome {user.get('name')}!"
        return f"Invalid credentials"
    else:
        return render_template("student/login.html")

app.run(debug=True)

'''
print(User.all())
User.add({
    'user_id' : 'US101',
    'name': 'Saron',
    'email': 'saron@gmail.com',
    'password': '12345678',
    'role': 'Student'
})
User.add({
    'user_id' : 'US102',
    'name': 'Atrfe',
    'email': 'atrfe@gmail.com',
    'password': '87654321',
    'role': 'Teacher'
})
print(User.all())

print('US102', User.get('US102'))
print('US103', User.get('US103'))
print(Book.all())
Book.add({
    'book_id':'su201',
    'book_name':'python',
    'auhtor':'unknown'
})
print(Book.all())
print(Rentals.all())
Rentals.add({
       'book_id':'su201',
       'user_id' : 'US102',
       'check-in date':'6/6/25',
       'check-out date':'6/7/25',
       'return status':'True'

})
print(Rentals.all())
'''