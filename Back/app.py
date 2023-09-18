#aimports
import logging
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime, timedelta
import json
import random

#end imports


#flask routes

app = Flask(__name__, template_folder='../Front/templates')



login_manager = LoginManager()  # Create a LoginManager instance
login_manager.login_view = "login"  # Set the view to redirect to for login
login_manager.init_app(app)  # Initialize Flask-Login with your Flask app

# Create a custom logger
logger = logging.getLogger(__name__)

# Configure the logger
logging.basicConfig(filename='library.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable Flask's built-in logger
app.logger.disabled = True


@app.route('/')
def index():
    # Check if the user is logged in before accessing their username
    if current_user.is_authenticated:
        username = current_user.username  # Replace 'username' with the actual attribute name of the username in your User model
        return render_template('index.html', username=username)
    else:
        # Handle the case when the user is not logged in
        return render_template('index.html', username=None)  # You can pass None or an empty string as the username



#register route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid registration data'}), 400

    username = data['username']
    password = data['password']

    # Load existing user data from the JSON file
    with open('users.json', 'r') as users_file:
        users = json.load(users_file)

    # Check if the username is already taken
    if any(user['username'] == username for user in users):
        return jsonify({'message': 'Username already taken. Please choose a different one'}), 400
    else:
        # Create a new user object and save it to the JSON file
        new_user = {'username': username, 'password': password}
        users.append(new_user)

        with open('users.json', 'w') as users_file:
            json.dump(users, users_file)

        return jsonify({'message': 'Registration successful'}), 201

#login route    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid login data'}), 400

    username = data['username']
    password = data['password']

    # Load user data from the JSON file
    with open('users.json', 'r') as users_file:
        users = json.load(users_file)

    # Find the user by username
    user = next((user for user in users if user['username'] == username), None)

    if user and user['password'] == password:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Login failed. Please check your credentials'}), 401


#flask routes end


#classes

class User(UserMixin):
    def __init__(self, id):
        self.id = id

#id managers make sure there are no duplicates

class CustomerFilter(logging.Filter):
    def filter(self, record):
        # Add the customer_id to the log record if it's present in the current user context
        record.customer_id = getattr(current_user, 'id', 'N/A')
        return True


class CostumerIDManager:
    def __init__(self):
        self.used_ids = set()

    def generate_unique_id(self):
        while True:
            new_id = random.randint(1000000, 9999999)
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id

    def to_dict(self):
        return {
            'used_ids': list(self.used_ids)
        }

    @classmethod
    def from_dict(cls, data):
        manager = cls()
        manager.used_ids = set(data['used_ids'])
        return manager


class BookIDManager:
    def __init__(self):
        self.used_ids = set()

    def generate_unique_id(self):
        while True:
            new_id = random.randint(1000000, 9999999)
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id

    def to_dict(self):
        return {
            'used_ids': list(self.used_ids)
        }

    @classmethod
    def from_dict(cls, data):
        manager = cls()
        manager.used_ids = set(data['used_ids'])
        return manager

# a Costumer can loan a book and return it in function and he 
#has 5 properties age, firstname, gender, id, lastname,

class Customer:
    def __init__(self, first_name, last_name, age, gender, city):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.id_manager = CostumerIDManager()
        self.id = self.id_manager.generate_unique_id()
        self.city = city

    def to_dict(self,):
        return {
            'age': self.age,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'costumerid': self.id,
            'city': self.city
        }




#the book class has 7 properties bookname, production_year, auther,

class Book:
    def __init__(self, bookname, author, production_year, agelimit, loaned, stock, bookid):
        self.bookname = bookname
        self.author = author
        self.production_year = production_year
        self.agelimit = agelimit
        self.loaned = loaned
        self.bookid = bookid
        self.stock = stock

    def to_dict(self):
        return {
            'bookname': self.bookname,
            'author': self.author,
            'production_year': self.production_year,
            'agelimit': self.agelimit,
            'loaned': self.loaned,
            'bookid': self.bookid,
            'stock': self.stock
        }





#loan class id's have only 6 digits unlike the costumer id(7 digits) and has 4 properties
class Loan:
    def __init__(self, costumerid, bookid, loandate, returndate):
        self.costumerid = costumerid
        self.bookid = bookid
        self.loandate = loandate
        self.returndate = returndate

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (Book, Customer)):
            return obj.to_dict()
        return super().default(obj)
 

#end of classes

#loanoptions

LOAN_OPTIONS = {
    '2 days': 2,
    '5 days': 5,
    '10 days': 10
}

#loanoptions end

#lists

costumers_list = []

library = []

loaned = []

lateloans = []

#end lists

# File paths for JSON data
COSTUMERS_JSON_PATH = 'costumers.json'
BOOK_JSON_PATH = 'book.json'
BORROWED_JSON_PATH = 'borrowed.json'
LATELOANS_JSON_PATH = 'lateloans.json'


#Functions

# allows to add a costumer to the costumer to costumers.json
def addcostumer(customer):
    costumers_list.append(customer)
    logger.info('Customer "%s %s" (ID: %s) has been added.', customer.first_name, customer.last_name, customer.id)
    save_data_to_json()  # Save data after adding a customer

# Function to add a book and save to JSON
def addbook(book):
    library.append(book)
    logger.info('Book "%s" (ID: %s) has been added to the library.', book.bookname, book.bookid)
    save_data_to_json()  # Save data after adding a book

#allows the loaning of a book there are 3 diffrent types of loans
def loanbook(costumer, book, loan_option):
    if book in library:
        loandate = datetime.now()
        returndate = loandate + timedelta(days=LOAN_OPTIONS.get(loan_option, 2))
        loan = Loan(costumer.id, book.bookid, loandate, returndate)
        loaned.append(loan)
        book.loaned = True

        # Log the loan action
        logger.info('Book "%s" (ID: %s) has been loaned by %s %s (ID: %s) until %s',
                    book.bookname, book.bookid, costumer.first_name, costumer.last_name, costumer.id,
                    returndate.strftime("%Y-%m-%d %H:%M:%S"))
        
        return f'Book "{book.bookname}" has been loaned by {costumer.first_name} {costumer.last_name} until {returndate.strftime("%Y-%m-%d %H:%M:%S")}'
    else:
        logger.warning('Book "%s" not found in the library. Loan request failed.', book.bookname)
        return 'Book not found in the library.'


# function to display all books in the library
def display_all_books():
    for book in library:
        # Log the action of displaying books
        logger.info('Customer (ID: %s) is viewing book - Book ID: %s, Title: %s, Author: %s, Loaned: %s',
                    current_user.id, book.bookid, book.bookname, book.author, book.loaned)
        print(f'Book ID: {book.bookid}, Title: {book.bookname}, Author: {book.author}, Loaned: {book.loaned}')


# function to display all customers
def display_costumers():
    for customer in costumers_list:
        # Log the action of displaying customers
        logger.info('Customer (ID: %s) is viewing customer - Customer ID: %s, Name: %s %s, Age: %s',
                    current_user.id, customer.id, customer.first_name, customer.last_name, customer.age)
        print(f'Customer ID: {customer.id}, Name: {customer.first_name} {customer.last_name}, Age: {customer.age}')

# Function to display all loaned books
def display_loans():
    # Log the action of displaying loaned books
    logger.info('Customer (ID: %s) viewed the list of loaned books', current_user.id)
    
    # Iterate through the loaned list and print or return information about each loan
    for loan in loaned:
        # You can format the output as needed
        print(f'Loan ID: {loan.bookid}, Customer ID: {loan.costumerid}, Loan Date: {loan.loandate}, Return Date: {loan.returndate}')

# Function to display late loans
def display_late_loans():
    # Calculate the current date
    current_date = datetime.now()
    
    # Log the action of displaying late loans
    logger.info('Customer (ID: %s) viewed the list of late loans', current_user.id)

    # Iterate through the loaned list and check for late loans
    for loan in loaned:
        if current_date > loan.returndate:
            # This loan is late; you can print or return information about the late loan
            print(f'Late Loan - Book ID: {loan.bookid}, Customer ID: {loan.costumerid}, Loan Date: {loan.loandate}, Return Date: {loan.returndate}')

# Function to find a book by ID, name, or part of the name
def find_books(search_term):
    # Create a list to store matching books
    matching_books = []
    
    # Iterate through the library to find matching books
    for book in library:
        if search_term.lower() in book.bookname.lower() or search_term == str(book.bookid):
            matching_books.append(book)

    # Return the list of matching books
    return matching_books

# Function to find a customer by ID, name, or part of the name
def find_costumer(search_term):
    # Create a list to store matching customers
    matching_customers = []
    
    # Iterate through the costumers_list to find matching customers
    for customer in costumers_list:
        if search_term.lower() in customer.first_name.lower() or search_term.lower() in customer.last_name.lower() or search_term == str(customer.id):
            matching_customers.append(customer)

    # Return the list of matching customers
    return matching_customers

#remove book from library and books.json
def remove_book(book):
    if book in library:
        library.remove(book)

        # Log the action of removing a book
        logger.info('Customer (ID: %s) removed a book (ID: %s)', current_user.id, book.bookid)
        save_data_to_json()  # Save data after removing a book

        return f'Book "{book.bookname}" has been removed from the library.'
    else:
        return 'Book not found in the library.'


# Function to remove a customer from the costumers_list
def remove_costumer(customer):
    if customer in costumers_list:
        costumers_list.remove(customer)

        # Log the action of removing a customer
        logger.info('Customer (ID: %s) removed a customer (ID: %s)', current_user.id, customer.id)
        save_data_to_json()  # Save data after removing a customer

        return f'Customer "{customer.first_name} {customer.last_name}" has been removed.'
    else:
        return 'Customer not found.'
    
# Function to save data from arrays to JSON files
def save_data_to_json():
    with open(COSTUMERS_JSON_PATH, 'w') as costumers_file:
        json.dump([customer.to_dict() for customer in costumers_list], costumers_file)

    with open(BOOK_JSON_PATH, 'w') as book_file:
        json.dump([book.__dict__ for book in library], book_file)

    with open(BORROWED_JSON_PATH, 'w') as borrowed_file:
        json.dump([loan.__dict__ for loan in loaned], borrowed_file)

    with open(LATELOANS_JSON_PATH, 'w') as lateloans_file:
        json.dump([loan.__dict__ for loan in lateloans], lateloans_file)

def load_data_from_json():
    try:
        with open(COSTUMERS_JSON_PATH, 'r') as costumers_file:
            costumers_list.extend(json.load(costumers_file))
    except FileNotFoundError:
        pass  # The file doesn't exist initially

    try:
        with open(BOOK_JSON_PATH, 'r') as book_file:
            library.extend(json.load(book_file))
    except FileNotFoundError:
        pass

    try:
        with open(BORROWED_JSON_PATH, 'r') as borrowed_file:
            loaned.extend(json.load(borrowed_file))
    except FileNotFoundError:
        pass

    try:
        with open(LATELOANS_JSON_PATH, 'r') as lateloans_file:
            lateloans.extend(json.load(lateloans_file))
    except FileNotFoundError:
        pass

# Load data from JSON files

# Define a user_loader function to load a user by ID
@login_manager.user_loader
def load_user(user_id):
    # Load a user by their ID (replace with your actual user loading logic)
    return User(user_id)

#end of functions


#the main is where we run all our functions 
if __name__ == "__main__":
    app.run(debug=True, host = '192.168.56.1' ,port=7000)