## Item Catalog 
     Item Catalog project is python based web application  that allows the user to login, create their own catalog, and add item to their catalogs. It also allows the user to navigate other users catalogs.  
     The project also provides Apis to serve the data in json format.
### Get Started
    These instructions will help on how to run the code of this project.
### Prerequistes
    The code is written in **Python 3.6**.
    You need to create facebook and google applications. and have their credentials saved in fb_client_secrets.json and client_secrets.json respectively.Those two files should be located in the same path as application.py.
    appId for facebook and client_id for google should be placed in the tempaltes/login.html file to replace the existing ones
### What does this submission contain
    This project consists of the follows: 
        application.py : which contains the python code, and runs the server.
        database_setup.py : Which contains the required database schema.
        tempates : dirctory contains html files
## How to run the code
    First run database_setup.py to setup the database
      python database_setup.py
    You need to run the server at application.py as follow
        python application.py
    the server runs on localhost:5000.


    
