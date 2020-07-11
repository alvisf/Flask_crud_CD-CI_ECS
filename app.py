from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Artist Class/Model
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    score = db.Column(db.Float)
    noOfMovie = db.Column(db.Integer)

    def __init__(self, name, description, score, noOfMovie):
        self.name = name
        self.description = description
        self.score = score
        self.noOfMovie = noOfMovie


# Artist Schema
class ArtistSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "score", "noOfMovie")


# Init schema
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)

# Create a Artist
@app.route("/artist", methods=["POST"])
def add_artist():
    name = request.json["name"]
    description = request.json["description"]
    score = request.json["score"]
    noOfMovie = request.json["noOfMovie"]

    new_artist = Artist(name, description, score, noOfMovie)

    db.session.add(new_artist)
    db.session.commit()

    return artist_schema.jsonify(new_artist)


# Get All Artists
@app.route("/artist", methods=["GET"])
def get_artists():
    all_artists = Artist.query.all()
    result = artists_schema.dump(all_artists)
    return jsonify(result)


# Get Single Artists
@app.route("/artist/<id>", methods=["GET"])
def get_artist(id):
    artist = Artist.query.get(id)
    return artist_schema.jsonify(artist)


# Update a Artist
@app.route("/artist/<id>", methods=["PUT"])
def update_artist(id):
    artist = Artist.query.get(id)

    name = request.json["name"]
    description = request.json["description"]
    score = request.json["score"]
    noOfMovie = request.json["noOfMovie"]

    artist.name = name
    artist.description = description
    artist.score = score
    artist.noOfMovie = noOfMovie

    db.session.commit()

    return artist_schema.jsonify(artist)


# Delete
@app.route("/artist/<id>", methods=["DELETE"])
def delete_artist(id):
    artist = Artist.query.get(id)
    db.session.delete(artist)
    db.session.commit()

    return artist_schema.jsonify(artist)


# Run Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

