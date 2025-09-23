import json
import os
import datetime

DATA_DIR = "data/"

user_json_path = os.path.join(DATA_DIR, 'users.json')
book_json_path = os.path.join(DATA_DIR, 'books.json')
rental_json_path = os.path.join(DATA_DIR, 'rentals.json')
book_json_path = os.path.join(DATA_DIR, 'books.json')
request_json_path = os.path.join(DATA_DIR, 'request.json')

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def _read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.decoder.JSONDecodeError:
                return []
    else:
        return []

def _write_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)
        f.close()


class User:

    @staticmethod
    def all():
        return _read_json(user_json_path)
    
    @staticmethod
    def get(user_id):
        users = User.all()
        for user in users:
            if user.get('user_id') == user_id:
                return user
        return None

    @staticmethod
    def add(data):
        users = User.all()
        users.append(data)
        _write_json(user_json_path, users)

    @staticmethod
    def remove(data):
        users = User.all()
        if data in users:
            users.remove(data)
            _write_json(user_json_path, users)
            return True
        
        return False

    
class Book:
    
    @staticmethod
    def all():
        return _read_json(book_json_path)
    
    @staticmethod
    def get(book_id):
        books = Book.all()
        for book in books:
            if book.get('book_id') == book_id:
                return book
        return None

    @staticmethod
    def add(data):
        book = Book.all()
        book.append(data)
        _write_json(book_json_path, book)

    @staticmethod
    def remove(data):
        book = Book.all()
        if data in book:
            book.remove(data)
            _write_json(book_json_path, book)
            return True
        
        return False

class Rentals:
    
    @staticmethod
    def all():
        return _read_json(rental_json_path)
    
    @staticmethod
    def get_by_user_id(user_id):
        rentals = Rentals.all() 
        user_rentals = [rental for rental in rentals if rental.get('user_id') == user_id]
        return user_rentals if user_rentals else None

    @staticmethod
    def get_by_book_id(book_id):
        rentals = Rentals.all()
        book_rentals = [rental for rental in rentals if rental.get('book_id') == book_id]
        return book_rentals if book_rentals else None

    @staticmethod
    def update_rental_status(book_id, user_id, return_status):
        rentals = Rentals.all()
        for rental in rentals:
            if rental.get('book_id') == book_id and rental.get('user_id') == user_id:
                rental['return_status'] = return_status
                _write_json(rental_json_path, rentals)
                return True
        if return_status == "Created":
            rentals.append({
                'book_id': book_id,
                'user_id' : user_id,
                "rental_date": datetime.datetime.strftime("%Y-%m-%d"),
                "estimated_return_date": "3", # Default
                "return_status": return_status

            })
            return True

        return False

    @staticmethod
    def add(data):
        rentals = Rentals.all()
        rentals.append(data)
        _write_json(rental_json_path, rentals)

        return False