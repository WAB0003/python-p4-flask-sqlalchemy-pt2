#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  #set up to point to our existing database of app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        #set to false to avoid buliding up too much unhelpful data in memory while app is running

migrate = Migrate(app, db)          #this creates a Migrate instance that configures thte app and modesl for Flask-Migrate

db.init_app(app)                    #connects our database to our application before it runs

#!Add to server
@app.route('/')                     #app.route determines which resources areavailable at which URLS. It then saves them to the applications URL map.
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response

#! Add a view for Pets
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    
    if not pet:
        resp_body = '<h1>404 pet not found</h1>'
        response = make_response(resp_body, 404)
        return response
        
    resp_body = f'''
        <h1>Information for {pet.name}</h1>
        <h2>Pet Species is{pet.species}</h2>
        <h2>Pet Owner is{pet.owner.name}</h2>
    '''
    
    response = make_response(resp_body, 200)
    return response

#! Add a view for Owners
@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).first()
    
    if not owner:
        resp_body = '<h1>404 owner not found</h1>'
        resp = make_response(resp_body, 404)
        return resp
    
    resp_body = f'<h1>Information for {owner.name}</h1>'
    
    pets = [pet for pet in owner.pets]
    
    if not pets:
        resp_body += f'<h2>Has no pets at this time.</h2>'
        
    else:
        for pet in pets:
            resp_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'
            
    response = make_response(resp_body, 200)
    
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
