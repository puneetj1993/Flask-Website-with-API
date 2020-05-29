""" Implementing the various routes """

from flask import render_template, request, redirect, url_for, flash, make_response, jsonify
from project import app,db
from project.models import User, Author, Book
from project.forms import Registration, LoginForm
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from functools import wraps
import json
import requests
import jwt
import datetime

def check_token(func):
    @wraps(func)
    def wrapped(*args,**kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'message':'Missing Token'}),403
        try:
            data = jwd.decode(token,app.config['SECRET_KEY'])
            print(data)
        except:
            return jsonify({'message':'Invalid Token'}),403
        return func(*args,**kwargs)
    return wrapped 


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/register',methods=['GET','POST'])
def register():
    
    form = Registration()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,password=User.create_password(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Registartion successful")
        return redirect(url_for('login'))
    elif form.errors:
        flash("There are some errors in form submission. Please try again")
        return redirect(url_for('register'))

    return render_template('register.html',form=form,title='Sign Up')

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            token = jwt.encode({
                'user':user.username,
                'exp':datetime.datetime.utcnow() + datetime.timedelta(seconds=180)},app.config['SECRET_KEY'])
            #return jsonify({'token':token.decode('utf-8')})
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page=url_for('profile',username = user.username)
            return redirect(next_page)
        elif not user.check_password(form.password.data):
           flash('Incorrect Password. Please try again with valid password')
    elif form.errors:
        flash('Login Failed.Please try again')
        return redirect(url_for('login'))
    
    return render_template('login.html',form=form,title='Sign In')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html',username=username)


@app.route('/myprofile',methods=['GET'])
def get_profile(): 
    '''
        To GET the user profile
    '''
    if current_user.is_authenticated: 
        return render_template('myprofile.html',username=current_user.username, vfname =current_user.first_name,\
                                vlname=current_user.last_name,vphone=current_user.phone,vabout_me=current_user.about_me)
    else:
        flash ("You need to login to access you profile")
        return redirect(url_for('login'))


@app.route('/myprofile',methods=['POST'])
def create_profile():
    '''
        To complete/fill in the user profile
    '''
    if current_user.is_authenticated :
        if request.method=='POST' :
            user = User.query.get_or_404(current_user.id)
            if user:
                user.first_name = request.form['fname']
                user.last_name = request.form['lname']
                user.about_me = request.form['profile']
                user.phone = request.form['number']
                db.session.add(user)
                db.session.commit()
                return render_template('myprofile.html',username=current_user.username, vfname =user.first_name,\
                                         vlname=user.last_name,vphone=user.phone,vabout_me=user.about_me)
            else:
                abort(403)
    else:
        flash ("You need to login to access you profile")
        return redirect(url_for('login'))

@app.route('/myprofile/update',methods=['GET','POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        password_n = request.form['password']
        user = User.query.get_or_404(current_user.id)
        if user:
            if password_n:
                user.password = User.create_password(password_n)
                flash("Password is updated successfully")
                db.session.commit()
            else:
                flash("It seems you haven't entered the password in the form. Please try again.")
    return render_template("update_profile.html")

            

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User , 'Book':Book, 'Author':Author}

#------------------------ External API calling ------------------------------------------------------------


@app.route('/api/movies',methods=['GET','POST'])
def movies():
    if request.method == 'POST':
        title = request.form['movie_name']
        params = {'apikey':'d9383c96', 't' : title}
        r = requests.get("http://www.omdbapi.com",params)
        #print(r.headers)
        #print(r.cookies)
        return render_template("movies.html", res=json.loads(r.text))
    else:
        return render_template("movies.html",res=None)
    
@app.route('/api/cocktails',methods=['GET','POST'])
def cocktails():
    if request.method == 'POST':
        title = request.form['cocktail_name']
        params={'i':title}
        req = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php',params)
        return render_template("cocktail.html", res=json.loads(req.text))
    else:
        return render_template("cocktail.html", res=None)

#--------------------API Creation -----------------------------------------

@app.route('/books')
def get_books():
    books = Book.query.all()
    return render_template("books.html",books=books)

@app.route('/books/<int:id>/')
@check_token
def get_book_by_id(id):
    print(id)
    book = Book.query.filter_by(book_id=id).first_or_404()
    #if not book:
    #    return make_response("Book id not found in db",404)
    return jsonify(book_name=book.book_name,Author=book.author.author_name,Price=book.book_price)
    

@app.route('/books/<int:id>',methods=['POST'])
def add_book_by_id(id):
    data = request.get_json()
    book = Book(book_name=data["name"],book_price=data["price"],book_id=data["id"],author_id=data["author_id"])
    db.session.add(book)
    db.session.commit()
    return jsonify(book_name=data["name"],book_price=data["price"],book_id=data["id"],author_id=data["author_id"])
    

