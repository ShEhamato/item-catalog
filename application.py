from flask import Flask, render_template, url_for

catalogList=[{'id':1,'name':'Sports','description':'Items that relate to sports including'},
{'id':2,'name':'Technology','description':'Items that relate to high technology including'},
{'id':3,'name':'Books','description':'Items that books'}]

app = Flask(__name__)


@app.route('/')
@app.route('/catalogs')
def listCatalog():
    return render_template('catalog-list.html', catalog_list=catalogList )


@app.route('/catalogs/new')
def createCatalog():
    return render_template('catalog-new.html')  


@app.route('/catalogs/<int:catalog_id>/view')
def viewCatalog(catalog_id):
    return render_template('catalog-view.html', catalog = catalogList[catalog_id-1] ) 


@app.route('/catalogs/<int:catalog_id>/edit')
def editCatalog(catalog_id):
    return render_template('catalog-edit.html' , catalog = catalogList[catalog_id-1] ) 


@app.route('/catalogs/<int:catalog_id>/delete')
def deleteCatalog(catalog_id):
    return render_template('catalog-delete.html', catalog = catalogList[catalog_id-1] ) 



if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)