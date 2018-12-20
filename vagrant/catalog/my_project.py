from flask import Flask, render_template, request, url_for
from flask import redirect, flash, jsonify
from flask import session as login_session
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Bookshelf, Book, User
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import cgi
import random
import string

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
APPLICATION_NAME = "Book Catalog"

# Setting up database connections
engine = create_engine('sqlite:///booklibrary.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# User Helper Functions
def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# Creating anti-forgery state token for login to prevent CSRF attacks
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    # Render Login Template
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Function that establishes connection with Google when
    'Sign in using Google' button is selected.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorisation code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        # exchange the access code for google creds
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Get access token from the credentials and check if it is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
                150px;-webkit-border-radius: 150px;-moz-border-radius: \
                150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """
    Function that establishes connection with Facebook when
    'Sign in using FB' button is selected.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain access token (this is short-lived)
    access_token = request.data
    print "access token received %s " % access_token

    # Exchange short-lived token for long-lived server side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
            'web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
            'web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (  # noqa
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v3.2/me"

    """
        Due to the formatting for the result from the server token exchange
        we have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replaces
        the remaining quotes with nothing so that it can be used directly
        in the graph api calls.
    """
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v3.2/me?access_token=%s&fields=name,id,email' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    print data
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v3.2/me/picture?access_token=%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # Check if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
                150px;-webkit-border-radius: 150px;-moz-border-radius: \
                150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

# Disconnect functions


@app.route('/disconnect')
def disconnect():
    """
    Disconnect function that calls the subsequent google/ facebook
    disconnect functions. Additionally, the function also deletes the
    login_session values, thus terminating the session.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']

        flash("You have successfully been logged out!")
        return redirect(url_for("showBookshelf"))
    else:
        flash("You were not logged in!")
        return redirect(url_for("showBookshelf"))


# Google Disconnect function
@app.route('/gdisconnect')
def gdisconnect():
    """
    This function revokes a current user's token and resets their
    login_session.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % (
                                            login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps(
                                 'Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Facebook Disconnect function


@app.route('/fbdisconnect')
def fbdisconnect():
    """
    This function revokes a current user's access token from
    facebook's permissions.
    """
    facebook_id = login_session['facebook_id']
    # The access token must be included in the url request to successfully
    # logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


"""------------------------Code for API endpoints------------------------"""


@app.route('/bookshelves/JSON')
def allBookshelfJSON():
    """
    This endpoint returns all bookshelves
    """
    bookshelves = session.query(Bookshelf).all()
    return jsonify(Book=[i.serialize for i in bookshelves])


@app.route('/bookshelf/<int:bookshelf_id>/book/JSON')
def bookshelfJSON(bookshelf_id):
    """
    This endpoint returns all books on a bookshelf
    """
    bookshelf = session.query(Bookshelf).filter_by(id=bookshelf_id).one_or_none()
    books = session.query(Book).filter_by(bookshelf_id=bookshelf.id).all()
    return jsonify(Book=[i.serialize for i in books])


@app.route('/bookshelf/<int:bookshelf_id>/book/<int:book_id>/JSON')
def bookJSON(bookshelf_id, book_id):
    """
    This endpoint returns data for a particular book
    """
    book = session.query(Book).filter_by(
        bookshelf_id=bookshelf_id, id=book_id).one_or_none()
    return jsonify(Book=book.serialize)


"""--------------------Code for routes of all webpages--------------------"""


# Show all bookshelves
@app.route('/')
@app.route('/bookshelf/')
def showBookshelf():
    """
    This function shows all the bookshelves in the library.

    If the user is not logged in, the public bookshelf simply displays
    the bookshelves without any option to edit or delete them.

    If the user is logged in, then the user can add a new bookshelf or
    perform CRUD operations on the books created within their bookshelf.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    bookshelves = session.query(Bookshelf).all()
    if 'username' not in login_session:
        return render_template('public_bookshelf.html',
                               bookshelves=bookshelves)
    return render_template('bookshelf.html', bookshelves=bookshelves)


# Add a new bookshelf
@app.route('/bookshelf/new/', methods=['GET', 'POST'])
def newBookshelf():
    """
    This function presents the form for creating a new bookshelf,
    processes the form and inputs into the database.

    The user must be logged in to add a new bookshelf, else is redirected
    to login page.
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newBookshelf = Bookshelf(name=request.form['name'],
                                 user_id=login_session['user_id'])
        session.add(newBookshelf)
        session.commit()
        flash("New bookshelf: %s created!" % request.form['name'])
        return redirect(url_for('showBookshelf'))
    else:
        return render_template('new_bookshelf.html')


# Edit an existing bookshelf
@app.route('/bookshelf/<int:bookshelf_id>/edit/', methods=['GET', 'POST'])
def editBookshelf(bookshelf_id):
    """
    This function presents the form for editing an existing bookshelf,
    processes the form and inputs into the database.

    The user must be logged in to edit a bookshelf and must be the creator
    of the bookshelf to edit it.
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editBookshelf = session.query(Bookshelf).filter_by(id=bookshelf_id).one()
    if editBookshelf.user_id != login_session['user_id']:
        return "<script>function crossCheck() \
        {alert('You are not authorised to access this page.\
        Please create your own bookshelf in order to edit.');}</script>\
        <body onload='crossCheck()''>"
    if request.method == 'POST':
        if request.form['name']:
            editBookshelf.name = request.form['name']
            session.add(editBookshelf)
            session.commit()
            flash("Bookshelf edited!")
            return redirect(url_for('showBookshelf'))
    else:
        return render_template('edit_bookshelf.html',
                               bookshelf_id=bookshelf_id,
                               bookshelf=editBookshelf)


# Delete an existing bookshelf
@app.route('/bookshelf/<int:bookshelf_id>/delete/', methods=['GET', 'POST'])
def deleteBookshelf(bookshelf_id):
    """
    This function presents the form for deleting an existing bookshelf,
    processes the form and commits to the database.

    The user must be logged in to delete a bookshelf and must be the creator
    of the bookshelf to delete it.
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deleteBookshelf = session.query(Bookshelf).filter_by(id=bookshelf_id).one()
    if deleteBookshelf.user_id != login_session['user_id']:
        return "<script>function crossCheck() \
        {alert('You are not authorised to access this page.\
        Please create your own bookshelf in order to delete');}\
        </script><body onload='crossCheck()''>"
    if request.method == 'POST':
        session.delete(deleteBookshelf)
        session.commit()
        flash("Bookshelf deleted!")
        return redirect(url_for('showBookshelf', bookshelf_id=bookshelf_id))
    else:
        return render_template('delete_bookshelf.html',
                               bookshelf_id=bookshelf_id,
                               bookshelf=deleteBookshelf)


# Show books for an existing bookshelf
@app.route('/bookshelf/<int:bookshelf_id>/')
@app.route('/bookshelf/<int:bookshelf_id>/book/')
def showBooks(bookshelf_id):
    """
    This function shows all the books on a bookshelf.

    If the user is not logged in, the page only displays
    the books with their details without any option to edit or delete them.

    If the user is logged in, then the user can perform CRUD operations on
    the books within their own bookshelf.
    """
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    bookshelf = session.query(Bookshelf).filter_by(id=bookshelf_id).one()
    creator = getUserInfo(bookshelf.user_id)
    books = session.query(Book).filter_by(bookshelf_id=bookshelf.id).all()
    if ('username' not in login_session or
            creator.id != login_session['user_id']):
        return render_template('public_books.html', bookshelf=bookshelf,
                               books=books, creator=creator)
    else:
        return render_template('books.html', bookshelf=bookshelf,
                               books=books, creator=creator)


# Add book on a bookshelf
@app.route('/bookshelf/<int:bookshelf_id>/book/new/', methods=['GET', 'POST'])
def newBook(bookshelf_id):
    """
    This function presents the form for adding a new book to the bookshelf,
    processes the form and inputs into the database.

    The user must be logged in to add a new book to the shelf, else is
    redirected to login page. Also, a user can only add a book to the shelf
    created by him/her.
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    bookshelf = session.query(Bookshelf).filter_by(id=bookshelf_id).one()
    if login_session['user_id'] != bookshelf.user_id:
        return "<script>function crossCheck() \
        {alert('You are not authorized to add book books to this bookshelf.\
        Please create your own bookshelf in order to add books.');}</script>\
        <body onload='crossCheck()'>"
    if request.method == 'POST':
        newBook = Book(name=request.form['name'],
                       description=request.form['description'],
                       author=request.form['author'],
                       genre=request.form['genre'],
                       status=request.form['status'],
                       bookshelf_id=bookshelf_id,
                       user_id=login_session['user_id'])
        session.add(newBook)
        session.commit()
        flash("New book: %s created!" % newBook.name)
        return redirect(url_for('showBooks', bookshelf_id=bookshelf_id))
    else:
        return render_template('new_book.html', bookshelf_id=bookshelf_id)


# Edit book for a bookshelf
@app.route('/bookshelf/<int:bookshelf_id>/book/<int:book_id>/edit/',
           methods=['GET', 'POST'])
def editBook(bookshelf_id, book_id):
    """
    This function presents the form for editing an existing book,
    processes the form and inputs into the database.

    The user must be logged in to edit a book and must be the creator
    of the book to edit it.
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editBook = session.query(Book).filter_by(id=book_id).one()
    if editBook.user_id != login_session['user_id']:
        return "<script>function crossCheck() \
        {alert('You are not authorised to access this page.\
        Please create your own book in order to edit');}</script>\
        <body onload='crossCheck()''>"
    if request.method == 'POST':
        if request.form['name']:
            editBook.name = request.form['name']
        if request.form['description']:
            editBook.description = request.form['description']
        if request.form['author']:
            editBook.author = request.form['author']
        if request.form['genre']:
            editBook.author = request.form['genre']
        if request.form['status']:
            editBook.status = request.form['status']
        session.add(editBook)
        session.commit()
        flash("Book edited!")
        return redirect(url_for('showBooks', bookshelf_id=bookshelf_id))
    else:
        return render_template('edit_book.html',
                               bookshelf_id=bookshelf_id, book=editBook)


# Delete book from a bookshelf
@app.route('/bookshelf/<int:bookshelf_id>/book/<int:book_id>/delete/',
           methods=['GET', 'POST'])
def deleteBook(bookshelf_id, book_id):
    """
    This function presents the form for deleting an existing book,
    processes the form and commits into the database.

    The user must be logged in to delete a book and must be the creator
    of the book to delete it.
    """
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    delBook = session.query(Book).filter_by(id=book_id).one()
    if delBook.user_id != login_session['user_id']:
        return "<script>function crossCheck() \
        {alert('You are not authorised to access this page.\
        Please create your own book in order to delete');}</script>\
        <body onload='crossCheck()''>"
    if request.method == 'POST':
        session.delete(delBook)
        session.commit()
        flash("Book deleted!")
        return redirect(url_for('showBooks', bookshelf_id=bookshelf_id))
    else:
        return render_template('delete_book.html',
                               bookshelf_id=bookshelf_id, book=delBook)


if __name__ == '__main__':
    app.secret_key = 'booklibrary_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
