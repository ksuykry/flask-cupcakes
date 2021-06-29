"""Flask app for Cupcakes"""
from flask import Flask, redirect, flash, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from forms import CupcakeForm

from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """ Routes to the Homepage /api/cupcakes """

    return render_template("index.html")


@app.route("/api/cupcakes")
def cupcake_data():

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]
    
    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]
    new_cupcake = Cupcake(flavor=flavor, size=size,
                          rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    serialized = new_cupcake.serialize()

    return(jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def show_cup_cake(cupcake_id):

    """ Return JSON obj {'cupcake': {id, flavor, size, rating, image}} """
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    # cup {flavor: "strawberry", size: "large", rating: "5", image: ""}
    
    db.session.add(cupcake)
    db.session.commit()
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)
    

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cake(cupcake_id):
    delete_cupcake = Cupcake.query.get(cupcake_id)
    db.session.delete(delete_cupcake)
    db.session.commit()
    return jsonify(message="Deleted")