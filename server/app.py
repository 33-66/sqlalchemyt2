#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet,Owner

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    respone = make_response("<h1>Welcome to the pet/owner directory!</h1>", 200)
    return respone


@app.route("/pets/<int:id>")
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
   
    if not pet:
        response_body= "<h1>404 pet not found</h1>"
        response = make_response(response_body,404)
        return response
    
    response_body = f"""
                <h2>Information for {pet.name}</h2>
                <h2>pet species is {pet.species}</h2>
                <h2>pet owner is{pet.owner.name} </h2>
                """

    response = make_response(response_body,200)

    return response

@app.route('/owner/<int:id>')
def owners_pets(id):
    owner = Owner.query.filter(Owner.id == id).first()
    if not owner:
        response_body =f"<h1>404 OWNER NOT FOUND</h1>"
        response = make_response(response_body,404)
        return response
    response_body = f'<h1>Information for {owner.name}</h1>'
    pets = [pet for pet in owner.pets]
    if not pets:
        response_body += f'<h2>Has no pets at the moment</h2>'
    else:
        for pet in pets:
            response_body+=f"<h2>Has pet {pet.species} named {pet.name}.</h2>"
    response = make_response(response_body,200)
    return response
if __name__ == "__main__":
    app.run(port=5555, debug=True)
