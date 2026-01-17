from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Movie

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        all_movies = Movie.query.all()
        return make_response(jsonify([movie.to_dict() for movie in all_movies]), 200)
    
    elif request.method == 'POST':
        data = request.get_json()
        if 'title' not in data or not data['title'].strip():
            return make_response(jsonify({"error": "Title is required"}), 400)
        
        movie = Movie(title=data['title'])
        db.session.add(movie)
        db.session.commit()
        return make_response(jsonify(movie.to_dict()), 201)

@app.route('/movies/<int:id>', methods=['PATCH', 'DELETE'])
def movie_by_id(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'PATCH':
        data = request.get_json()
        if 'title' in data and data['title'].strip():
            movie.title = data['title']
        db.session.commit()
        return make_response(jsonify(movie.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(movie)
        db.session.commit()
        return make_response(jsonify({"deleted": True}), 200)

if __name__ == "__main__":
    app.run(port=5555, debug=True)