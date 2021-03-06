from flask import Flask, render_template, url_for, redirect, jsonify
from database_setup import Base,  User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import session as login_session, request, flash, make_response
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


from database_setup import Catalog, Base, CatalogItem

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# facebook login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?'\
        + 'grant_type=fb_exchange_token&client_id='+app_id+'&'\
        + 'client_secret='+app_secret+'&fb_exchange_token'\
        + '='+access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we
        have to split the token first on commas and select the first index
        which gives us the key : value for the server access token then we
        split it on colons to pull out the actual token value and replace
        the remaining quotes with nothing so that it can be used directly
        in the graph api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token='\
        + token + '=&fields=name,id,email'
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'facebook'

    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    flash("Now logged in as %s" % login_session['username'])
    return output


# Facebook logout
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/'+facebook_id\
        + '/permissions?access_token='+access_token
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Google log in
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
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
        print login_session['access_token']
        print login_session['provider']
        response = make_response(
            json.dumps(
                'Current user is already connected.'
            ), 200
            )
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['email']
    # login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'
    print login_session['access_token']

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['email']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400)
            )
        response.headers['Content-Type'] = 'application/json'
        return response


# Log out from the app
@app.route('/disconnect')
def disconnect():
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
        # del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('listCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('listCatalog'))


# User Helper Functions
def createUser(login_session):
    session = DBSession()
    newUser = User(
                name=login_session['username'],
                email=login_session['email']
            )
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        session = DBSession()
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view Catalog Information
@app.route('/catalog/<int:catalog_id>/item/JSON')
def CatalogCatalogJSON(catalog_id):
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog_id).all()
    return jsonify(catalogItems=[i.serialize for i in items])


@app.route('/catalog/<int:catalog_id>/item/<int:item_id>/JSON')
def catalogItemJSON(catalog_id, item_id):
    session = DBSession()
    item = session.query(CatalogItem).filter_by(id=item_id).one()
    return jsonify(catalog_Item=item.serialize)


@app.route('/catalog/JSON')
def catalogsJSON():
    session = DBSession()
    catalogs = session.query(Catalog).all()
    return jsonify(catalogs=[r.serialize for r in catalogs])


# Get all Catalogs
@app.route('/')
@app.route('/catalogs')
def listCatalog():
    session = DBSession()
    catalogList = session.query(Catalog)
    if 'user_id' not in login_session:
        return render_template(
            'catalog-list-not-loggedin.html',
            catalog_list=catalogList
            )
    return render_template(
        'catalog-list.html', catalog_list=catalogList,
        user=login_session['email']
        )


# Create New catalog
@app.route('/catalogs/new', methods=['POST', 'GET'])
def createCatalog():
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        session = DBSession()
        catalog = Catalog(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id']
            )
        session.add(catalog)
        session.commit()
        return redirect(url_for('listCatalog'))
    else:
        return render_template(
            'catalog-new.html', user=login_session['email']
            )


# Edit Catalog
@app.route('/catalogs/<int:catalog_id>/edit', methods=['POST', 'GET'])
def editCatalog(catalog_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).first()
    if catalog is None:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    if login_session['user_id'] != catalog.user_id:
        return render_template(
            'permission-denied.html',
            catalog_id=catalog_id
            )
    if request.method == 'POST':
        if request.form['name']:
            catalog.name = request.form['name']
        if request.form['description']:
            catalog.description = request.form['description']
        session.add(catalog)
        session.commit()
        return redirect(url_for('listCatalog'))
    else:
        return render_template(
            'catalog-edit.html', catalog=catalog,
            user=login_session['email']
            )


# Delete catalog
@app.route('/catalogs/<int:catalog_id>/delete', methods=['POST', 'GET'])
def deleteCatalog(catalog_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).first()
    if catalog is None:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    if login_session['user_id'] != catalog.user_id:
        return render_template(
            'permission-denied.html',
            catalog_id=catalog_id
            )

    if request.method == 'POST':
        session.delete(catalog)
        session.commit()
        return redirect(url_for('listCatalog'))
    else:
        return render_template(
            'catalog-delete.html', catalog=catalog,
            user=login_session['email']
            )


# Show Item List for a catalog
@app.route('/catalogs/<int:catalog_id>/item-list')
def showItemList(catalog_id):
    session = DBSession()
    itemList = session.query(CatalogItem).filter_by(catalog_id=catalog_id)
    catalog = session.query(Catalog).filter_by(id=catalog_id)
    if 'user_id' not in login_session:
        return render_template(
            'item-list-not-loggedin.html', item_list=itemList,
            catalog_id=catalog_id
            )
    if catalog.count() == 0:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    return render_template(
            'item-list.html', item_list=itemList, catalog_id=catalog_id,
            user=login_session['email']
            )


# Create new Item
@app.route('/catalogs/<int:catalog_id>/items/new', methods=['POST', 'GET'])
def createItem(catalog_id):
    if 'user_id' not in login_session:
        return redirect(url_for('showLogin'))
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).first()
    if catalog is None:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    if login_session['user_id'] != catalog.user_id:
        return render_template(
            'permission-denied.html',
            catalog_id=catalog_id
            )
    if request.method == 'POST':
        session = DBSession()
        item = CatalogItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            duration=request.form['duration'],
            catalog_id=catalog_id,
            user_id=login_session['user_id']
            )
        session.add(item)
        session.commit()
        return redirect(url_for('showItemList', catalog_id=catalog_id))
    else:
        return render_template(
            'item-new.html', catalog_id=catalog_id,
            user=login_session['email']
            )


# Show Item
@app.route('/catalogs/<int:catalog_id>/items/<int:item_id>/view')
def viewItem(catalog_id, item_id):
    session = DBSession()
    item = session.query(CatalogItem).filter_by(id=item_id).first()
    if item is None:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    return render_template('item-view.html', item=item, catalog_id=catalog_id)


# edit item
@app.route(
            '/catalogs/<int:catalog_id>/items/<int:item_id>/edit',
            methods=['POST', 'GET']
            )
def editItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    session = DBSession()
    item = session.query(CatalogItem).filter_by(id=item_id).first()
    if item is None:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    if login_session['user_id'] != item.user_id:
        return render_template(
            'permission-denied.html',
            catalog_id=catalog_id
            )
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['price']:
            item.price = request.form['price']
        if request.form['duration']:
            item.duration = request.form['duration']
        session.add(item)
        session.commit()
        return redirect(url_for('showItemList', catalog_id=catalog_id))
    else:
        return render_template(
            'item-edit.html', item=item, catalog_id=catalog_id,
            user=login_session['email']
        )


# Delete item
@app.route(
            '/catalogs/<int:catalog_id>/items/<int:item_id>/delete',
            methods=['POST', 'GET']
            )
def deleteItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    session = DBSession()
    item = session.query(CatalogItem).filter_by(id=item_id).first()
    if item is None:
        return render_template(
            'no-page.html',
            user=login_session['email']
            )
    if login_session['user_id'] != item.user_id:
        return render_template(
            'permission-denied.html',
            catalog_id=catalog_id
            )
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItemList', catalog_id=catalog_id))
    else:
        return render_template(
            'item-delete.html', item=item, catalog_id=catalog_id,
            user=login_session['email']
            )


if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
