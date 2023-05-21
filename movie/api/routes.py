from flask import Blueprint, request, jsonify
from movie.helpers import token_required
from movie.models import db, movie_schema, movies_schema, Movie
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}

@api.route('/movies', methods=['POST'])
@token_required
def create_movie(our_user):
    title = request.json['title']
    imdb_id = request.json['imdb_id']
    release_year = request.json['release_year']
    genre = request.json['genre']
    m_type = request.json['m_type']
    image_url = request.json['image_url']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    movie = Movie(title=title, imdb_id=imdb_id, release_year=release_year, genre=genre,
                  m_type=m_type, image_url=image_url, user_token=user_token)

    db.session.add(movie)
    db.session.commit()

    response = movie_schema.dump(movie)

    return jsonify(response)


@api.route('/movies', methods=['GET'])
@token_required
def get_movies(our_user):
    owner = our_user.token
    movies = Movie.query.filter_by(user_token=owner).all()
    response = movies_schema.dump(movies)

    return jsonify(response)


@api.route('/movies/<id>', methods=['GET'])
@token_required
def get_movie(our_user, id):
    if id:
        movie = Movie.query.get(id)
        response = movie_schema.dump(movie)
        return jsonify(response)
    else:
        return jsonify({'message': 'Movie not found'}), 404


@api.route('/movies/<id>', methods=['PUT'])
@token_required
def update_movie(our_user, id):
    movie = Movie.query.get(id)
    if movie:
        movie.title = request.json['title']
        movie.imdb_id = request.json['imdb_id']
        movie.release_year = request.json['release_year']
        movie.genre = request.json['genre']
        movie.m_type = request.json['m_type']
        movie.image_url = request.json['image_url']
        movie.user_token = our_user.token

        db.session.commit()
        response = movie_schema.dump(movie)
        return jsonify(response)
    else:
        return jsonify({'message': 'Movie not found'}), 404


@api.route('/movies/<id>', methods=['DELETE'])
@token_required
def delete_movie(our_user, id):
    movie = Movie.query.get(id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        response = movie_schema.dump(movie)
        return jsonify(response)
    else:
        return jsonify({'message': 'Movie not found'}), 404
