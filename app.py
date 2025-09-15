from flask import Flask, render_template, request, url_for
from models import User, Book, Rentals

app = Flask(__name__)

@app.route('/', methods=["GET"])
def landing_page():
    return render_template("landing.html")

@app.route('/librarian', methods=["GET", "POST"])
def librarian():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.get(user_id)
        if user and user.get('password') == password and user.get('role') == 'Teacher':
            return render_template("librarian/dashboard.html", name=user.get('name'))
        return f"Invalid credentials"
    else:
        return render_template("librarian/login.html")

fetch_name = lambda x: [x, ''][x==None]
@app.route('/user', methods=["GET", "POST"])
def user():
    if request.method == "POST":
        search_query = request.form.get('query', 'ALL')
        books = Book.all()
        if search_query == "ALL":
            user_id = request.form.get('user_id')
            password = request.form.get('password')
            user = User.get(user_id)
            if user and user.get('password') == password and user.get('role') == 'Student':
                return render_template("student/dashboard.html", name=user.get('name'), books=books)
        else:
            books = [book for book in books if search_query.lower() in fetch_name(book.get('book_name', '')).lower()]
            return render_template("student/dashboard.html", books=books)
        return f"Invalid credentials"
    else:
        return render_template("student/login.html")

@app.route('/librarian/users', methods=["GET"])
def librarian_users():
    users = User.all()
    return render_template("librarian/users.html", users=users)

@app.route('/user/book', methods=["GET"])
def user_book():    
    books = Book.all()
    return render_template("student/book.html", books=books)

@app.route('/librarian/books', methods=["GET"])
def librarian_books():    
    books = Book.all()
    return render_template("librarian/books.html", books=books)

@app.route('/librarian/books/addpopup', methods=["GET", "POST"])
def librarian_add_book():
    if request.method == "POST":
        book_id = request.form.get('book_id')
        book_name = request.form.get('book_name')
        author = request.form.get('author')
        Book.add({
            'book_id': book_id,
            'book_name': book_name,
            'author': author
        })
        
        return render_template("librarian/books.html", books=Book.all())
    else:
        return render_template("librarian/addpopup.html")
    
@app.route('/librarian/books/removepopup', methods=["GET", "POST"])
def librarian_remove_book():
    if request.method == "POST":
        book_id = request.form.get('book_id')
        book = Book.get(book_id)
        if book:
            Book.remove(book)
            return render_template("librarian/books.html", books=Book.all())
        return f"Book with ID {book_id} not found."
    else:
        return render_template("librarian/removepopup.html")
    
@app.route('/librarian/rentals', methods=["GET"])
def librarian_rentals():    
    rentals = Rentals.all()
    return render_template("librarian/rentals.html", rentals=rentals)

@app.route('/librarian/rentals/viewRentals', methods=["GET", "POST"])
def librarian_view_rentals():    
    rentals = Rentals.all()
    return render_template("librarian/viewRentals.html", rentals=rentals)

@app.route('/librarian/rentals/setcomplete/<user_id>-<book_id>', methods=["GET", "POST"])
def librarian_set_complete(user_id, book_id):
    Rentals.update_rental_status(book_id, user_id, 'True')
    rentals = Rentals.all()
    return render_template("librarian/viewRentals.html", rentals=rentals)


@app.route('/librarian/rentals/addRental', methods=["GET", "POST"])
def librarian_add_rental():
    if request.method == "POST":
        book_id = request.form.get('book_id')
        user_id = request.form.get('user_id')
        rental_date = request.form.get('rental_date')
        for_how_long = request.form.get('for_how_long')
        Rentals.add({
            'book_id': book_id,
            'user_id': user_id,
            'rental_date': rental_date,
            'estimated_return_date': for_how_long,
            'return_status': 'False'
        })
        
        return render_template("librarian/rentals.html", rentals=Rentals.all())
    else:
        return render_template("librarian/addRental.html")

app.run(debug=True, host='0.0.0.0')

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


# import random
# import string

# def gen_ran_str(n, incno=False):
#     to_choose = string.ascii_lowercase
#     if incno:
#         to_choose += string.digits
#     return ''.join(random.choices(to_choose, k=n))

# for i in range(10):
#     Book.add({
#         'book_id':gen_ran_str(5, True),
#         'book_name':gen_ran_str(7+i),
#         'author':gen_ran_str(5+i)
#     })