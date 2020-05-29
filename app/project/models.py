from project import db, login_manager
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    """
        Implementing User table for user management
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique =True, nullable = False)
    email = db.Column (db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.Integer)
    about_me = db.Column(db.String(150))
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    def __repr__(self): 
        ''' String representation of a class'''
        return "Username is {}".format(self.username)
    @staticmethod
    def create_password(value):
        ''' Stores password as hashed value due to security '''
        return generate_password_hash(value)
    
    def check_password(self,value):
        ''' Checks the hashed password against the password entered '''
        
        return check_password_hash(self.password,value)


    
    

class Author(db.Model):
    """
        Implementing Author table and One to many relationship between Author and Book tables
    """
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key = True)
    author_name = db.Column(db.String(20),nullable=False)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        ''' String representation of a class'''

        return "Author is {}".format(self.author_name)

class Book(db.Model):
    """
        Implementing Book table and Foreign key as author's id
    """
    __tablename__ = "book"

    book_id = db.Column(db.Integer,primary_key  = True)
    book_name = db.Column(db.String(50),nullable=False)
    book_price = db.Column( db.Float,nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('author.id'))

    def __repr__(self):
        ''' String representation of a class'''

        return "Book name is {}".format(self.book_name)

db.create_all()
db.session.commit()