from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=True)


with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return jsonify({"message": "Backend radi!"})



@app.route('/artists', methods=['GET'])
def get_artists():
    artists = Artist.query.all()
    return jsonify([
        {
            "id": a.id,
            "name": a.name,
            "album": a.album,
            "year": a.year
        }
        for a in artists
    ])



@app.route('/artists', methods=['POST'])
def add_artist():
    data = request.get_json()

    new_artist = Artist(
        name=data['name'],
        album=data.get('album'),
        year=data.get('year')
    )

    db.session.add(new_artist)
    db.session.commit()

    return jsonify({"message": "Artist added"})



@app.route('/artists/<int:id>', methods=['PUT'])
def update_artist(id):
    data = request.json

    artist = Artist.query.get(id)

    if not artist:
        return jsonify({"message": "not found"}), 404

    artist.name = data['name']
    artist.album = data.get('album')
    artist.year = data.get('year')

    db.session.commit()

    return jsonify({"message": "updated"})


@app.route('/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.get(id)

    if not artist:
        return jsonify({"message": "not found"}), 404

    db.session.delete(artist)
    db.session.commit()

    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True)