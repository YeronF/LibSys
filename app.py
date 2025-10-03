from flask import Flask, render_template, request, url_for, session, redirect
from models import User, Book, Rentals
import math

app = Flask(__name__)
app.secret_key = 'sgefwqvda53we2534jriewtdew39683cxe0487904654hgfj6ufr98'

def date_sort():
    rental_date = request.form.get('rental_date')
    data = [rental_date]
    data.sort()

@app.route('/', methods=["GET"])
def landing_page():
    return render_template("landing.html")

@app.route('/librarian/', methods=["GET", "POST"])
def librarian():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.get(user_id)
        if user and user.get('password') == password and user.get('role') == 'Teacher':
            session['user_id'] = user_id
            return render_template("librarian/dashboard.html", name=user.get('name'), role ='Teacher', user=user)
        return f"Invalid credentials"
    else:
        if session.get('user_id'):
            user = User.get(session.get('user_id'))
            if user.get('role') == "Teacher":
                return render_template("librarian/dashboard.html", name=user.get('name'), role ='Teacher', user=user)
        return render_template("librarian/login.html")

fetch_name = lambda x: [x, ''][x==None]
@app.route('/user/', methods=["GET", "POST"])
def user():
    if request.method == "POST":
        search_query = request.form.get('query', app.secret_key )
        books = Book.all()
        per_page = 10
        page = int(request.args.get('page', 1))
        books, total_pages = paginate_items(books, page, per_page)
        
        if search_query == app.secret_key :
            user_id = request.form.get('user_id')
            password = request.form.get('password')
            user = User.get(user_id)
            if user and user.get('password') == password and user.get('role') == 'Student':
                session['user_id'] = user_id
                return render_template("student/dashboard.html", name=user.get('name'), books=books, user=user, page=page, total_pages=total_pages, role ='Student')
        else:
            books = [book for book in books if search_query.lower() in fetch_name(book.get('book_name', '')).lower()]
            per_page = 10
            page = int(request.args.get('page', 1))
            books, total_pages = paginate_items(books, page, per_page)
            user = User.get(session['user_id'])
            return render_template("student/dashboard.html", name=user.get('name'), books=books, user=user, page=page, total_pages=total_pages, role ='Student')
            
        return f"Invalid credentials"
    else:
        search_query = request.form.get('query', app.secret_key ) 
        search_query = [search_query, ""][search_query == app.secret_key ]
        if session.get('user_id'):
            books = [book for book in Book.all() if search_query.lower() in fetch_name(book.get('book_name', '')).lower()]
            per_page = 10
            page = int(request.args.get('page', 1))
            books, total_pages = paginate_items(books, page, per_page)
            user = User.get(session['user_id'])
            return render_template("student/dashboard.html", name=user.get('name'), books=books, user=user, page=page, total_pages=total_pages, role ='Student')
        return render_template("student/login.html")

@app.route('/librarian/users/', methods=["GET"])
def librarian_users():
    if session.get('user_id'):
        users = User.all()
        per_page = 10
        page = int(request.args.get('page', 1))
        users, total_pages = paginate_items(users, page, per_page)
        return render_template("librarian/users.html", users=users, page=page, total_pages=total_pages, role ='Teacher')
    
    return "You need to log in"

def paginate_items(items, page, per_page):
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page
    if page < 1 or page > total_pages:
        return [], total_pages
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], total_pages

@app.route('/user/book/', methods=["GET"])
def user_book():
    if session.get('user_id'):
        books = Book.all()
        user = User.get(session['user_id'])
        per_page = 10
        page = int(request.args.get('page', 1))
        books, total_pages = paginate_items(books, page, per_page)
        return render_template("student/book.html", books=books, role ='Student')

    return "Please login"

@app.route('/librarian/books/', methods=["GET"])
def librarian_books():
    if session.get('user_id'):    
        books = Book.all()
        per_page = 10
        page = int(request.args.get('page', 1))
        books, total_pages = paginate_items(books, page, per_page)
        return render_template("librarian/books.html", books=books, page=page, total_pages=total_pages, role ='Teacher')
    
    return "Please login"

@app.route('/librarian/books/addpopup/', methods=["GET", "POST"])
def librarian_add_book():
    if session.get('user_id'):
        if request.method == "POST":
            book_id = request.form.get('book_id')
            book_name = request.form.get('book_name')
            author = request.form.get('author')
            Book.add({
                'book_id': book_id,
                'book_name': book_name,
                'author': author
            })
            
            return redirect(url_for('librarian_books'))
        else:
            return render_template("librarian/addpopup.html", role ='Teacher')
    
@app.route('/librarian/books/removepopup/', methods=["GET", "POST"])
def librarian_remove_book():
    if session.get('user_id'):
        if request.method == "POST":
                book_id = request.form.get('book_id')
                book = Book.get(book_id)
                if book:
                    Book.remove(book)
                    return redirect(url_for('librarian_books'))

                return f"Book with ID {book_id} not found."
        else:
            books = Book.all()
            return render_template("librarian/removepopup.html", books=books, role ='Teacher')
        
@app.route('/librarian/rentals/', methods=["GET"])
def librarian_rentals():  
    if session.get('user_id'):  
        rentals = Rentals.all()
        user = User.get(session.get('user_id'))
        return render_template("librarian/rentals.html", rentals=rentals, user=user, role ='Teacher')

@app.route('/librarian/rentals/viewRentals/', methods=["GET", "POST"])
def librarian_view_rentals():
    if session.get('user_id'):
        rentals = [r for r in Rentals.all() if r.get('return_status') in ['Returned', "Borrowed"]]
        rentals.sort(key=lambda x:x.get('rental_date'), reverse=True)
        per_page = 10
        page = int(request.args.get('page', 1))
        rentals, total_pages = paginate_items(rentals, page, per_page)    
        user = User.get(session.get('user_id'))
        return render_template("librarian/viewRentals.html", rentals=rentals, user=user, page=page, total_pages=total_pages, role ='Teacher')

@app.route('/librarian/rentals/setcomplete/<user_id>-<book_id>/', methods=["GET", "POST"])
def librarian_set_complete(user_id, book_id):
    if session.get('user_id'):
        stat = Rentals.update_rental_status(book_id, user_id, 'Returned')
        rentals = [r for r in Rentals.all() if r.get('return_status') in ['Returned', "Borrowed"]]
        user = User.get(session.get('user_id'))
        if not stat:
            return f"Rental record for User ID {user_id} and Book ID {book_id} not found."
        return render_template("librarian/viewRentals.html", rentals=rentals, user=user)


@app.route('/librarian/rentals/addRental/', methods=["GET", "POST"])
def librarian_add_rental():
    if session.get('user_id'):
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
            user = User.get(session.get('user_id'))
            
            return render_template("librarian/rentals.html", rentals=Rentals.all(), user=user, role ='Teacher')
        else:
            books = [book['book_id'] for book in Book.all()]
            users = [user['user_id'] for user in User.all() if user['role'] == 'Student']
            return render_template('librarian/addRental.html', books=books, users=users, role ='Teacher') 

@app.route('/librarian/users/adduser/', methods=["GET", "POST"])
def librarian_add_user():
    if session.get('user_id'):
        if request.method == "POST":
            user_id = request.form.get('user_id')
            user_name = request.form.get('user_name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role')
            User.add({
                'user_id': user_id,
                'name': user_name,
                'email': email,
                'password': password,
                'role': role
            })

            users = User.all()
            per_page = 2
            page = int(request.args.get('page', 1))
            users, total_pages = paginate_items(users, page, per_page)
            return render_template("librarian/users.html", users=users, page=page, total_pages=total_pages, role ='Teacher'
                                   )
        else:
            return render_template("librarian/adduser.html")
        
@app.route('/librarian/users/removeuser/', methods=["GET", "POST"])
def librarian_remove_user():
    if session.get('user_id'):
        if request.method == "POST":
            user_id = request.form.get('user_id')
            user = User.get(user_id)
            if user:
                User.remove(user)
                users = User.all()
                per_page = 10
                page = int(request.args.get('page', 1))
                users, total_pages = paginate_items(users, page, per_page)
                
                return render_template("librarian/users.html", users=users, page=page, total_pages=total_pages)
            return f"User with ID {user_id} not found."
        else:
            users = User.all()
            return render_template("librarian/removeuser.html", users=users, role ='Teacher')


@app.route('/user/book/rent/<user_id>-<book_id>/', methods=["GET", "POST"])
def user_rent(user_id, book_id):
    if request.method == "POST":
        rental_date = request.form.get('rental_date')
        for_how_long = request.form.get('for_how_long')
        Rentals.add({
                'book_id': book_id,
                'user_id': user_id,
                'rental_date': rental_date,
                'estimated_return_date': for_how_long,
                'return_status': 'Created'
            })
      
        user = User.get(user_id)
        books = Book.all()
        per_page = 10
        page = int(request.args.get('page', 1))
        books, total_pages = paginate_items(books, page, per_page)
        return render_template("student/dashboard.html", name=user.get('name'), books=books, user=user, page=page, total_pages=total_pages)



    return render_template("student/rent.html", book_id=book_id, user_id=user_id, role ='Student')

@app.route('/librarian/logout/', methods=["GET", "POST"])

def librarian_logoutpop():
    del(session['user_id'])
    return redirect(url_for('landing_page'))

@app.route('/librarian/logout-popup/', methods=["GET", "POST"])

def librarian_logout():
    return render_template("librarian/logout.html")



@app.route('/user/logout/', methods=["GET", "POST"])

def user_logoutpop():
    del(session['user_id'])
    return redirect(url_for('landing_page'))

@app.route('/user/logout-popup/', methods=["GET", "POST"])

def user_logout():
    return render_template("student/logout.html")



@app.route('/librarian/books/requests/', methods=["GET", "POST"])

def manage_requests():
    if session.get('user_id'):
        user = User.get(session.get('user_id'))
        rentals = [r for r in Rentals.all() if r.get('return_status') == "Created"]
    return render_template("librarian/requests.html", user=user, rentals=rentals, role ='Teacher')


@app.route('/librarian/requests/accept/<user_id>-<book_id>/', methods=["GET", "POST"])

def accepted(user_id, book_id):
    if session.get('user_id'):
        user = User.get(session.get('user_id'))
        Rentals.update_rental_status(book_id, user_id, 'Approved')
        return render_template("librarian/requests.html", user=user, role ='Teacher')
    
@app.route('/librarian/requests/reject/<user_id>-<book_id>/', methods=["GET", "POST"])

def rejected(user_id, book_id):
    if session.get('user_id'):
        user = User.get(session.get('user_id'))
        Rentals.update_rental_status(book_id, user_id, 'Rejected')
        return render_template("librarian/requests.html", user=user, role ='Teacher')

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

# def gen_id(n):
#     return 'US' + ''.join(random.choices(string.digits, k=n))

# for i in range(20):
#     # Book.add({
#     #     'book_id':gen_ran_str(5, True),
#     #     'book_name':gen_ran_str(7+i),
#     #     'author':gen_ran_str(5+i)
#     # })
#     User.add({
#         'user_id':gen_id(3+i),
#         'name':gen_ran_str(5+i),
#         'email':gen_ran_str(5+i)+'@gmail.com',
#         'password':gen_ran_str(8, True),
#         'role':'Student' if i%2==0 else 'Teacher'
#     })