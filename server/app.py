# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(quakes)
    quake_data = [{"id": q.id, "location": q.location, "magnitude": q.magnitude, "year": q.year} for q in quakes]
    response = {"count": count, "quakes": quake_data}
    return jsonify(response)


@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    quake = Earthquake.query.get(id)
    if quake:
        response = {"id": quake.id, "location": quake.location, "magnitude": quake.magnitude, "year": quake.year}
    else:
        response = {"message": f"Earthquake {id} not found."}
        return make_response(response, 404)
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5555, debug=True)