from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/catalogs')
def listCatalog():
    return render_template('catalog-list.html')


@app.route('/catalogs/new')
def createCatalog():
    return render_template('catalog-new.html')  


@app.route('/catalogs/<int:catalog_id>/view')
def viewCatalog(catalog_id):
    return render_template('catalog-view.html') 


@app.route('/catalogs/<int:catalog_id>/edit')
def editCatalog(catalog_id):
    return render_template('catalog-edit.html') 


@app.route('/catalogs/<int:catalog_id>/delete')
def deleteCatalog(catalog_id):
    return render_template('catalog-delete.html') 



if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)