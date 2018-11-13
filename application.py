from flask import Flask, render_template, url_for, redirect, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


catalogList=[{'id':1,'name':'Sports','description':'Items that relate to sports including'},
{'id':2,'name':'Technology','description':'Items that relate to high technology including'},
{'id':3,'name':'Books','description':'Items that books'}]

app = Flask(__name__)



@app.route('/')
@app.route('/catalogs')
def listCatalog():
    session = DBSession()
    catalogList = session.query(Catalog)
    return render_template('catalog-list.html', catalog_list=catalogList )


@app.route('/catalogs/new', methods=['POST', 'GET'])
def createCatalog():
    if request.method == 'POST':
        session = DBSession()
        catalog= Catalog(name = request.form['name'], description= request.form['description'])
        session.add(catalog)
        session.commit()
        return redirect(url_for('listCatalog'))
    else:
        return render_template('catalog-new.html')  


@app.route('/catalogs/<int:catalog_id>/view')
def viewCatalog(catalog_id):
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    return render_template('catalog-view.html', catalog = catalog ) 


@app.route('/catalogs/<int:catalog_id>/edit', methods=['POST', 'GET'])
def editCatalog(catalog_id):
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            catalog.name=request.form['name']
        if request.form['description']:
            catalog.description= request.form['description']
        session.add(catalog)
        session.commit()
        return redirect(url_for('listCatalog'))
    else:
        return render_template('catalog-edit.html' , catalog = catalog ) 


@app.route('/catalogs/<int:catalog_id>/delete' , methods=['POST', 'GET'])
def deleteCatalog(catalog_id):
    session = DBSession()
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        session.delete(catalog)
        session.commit()
        return redirect(url_for('listCatalog'))
    else:
        return render_template('catalog-delete.html', catalog = catalog) 



if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)