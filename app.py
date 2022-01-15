import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor

from auth.auth import AuthError, requires_auth

from datetime import datetime

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app)

  # CORS Headers
  @app.after_request
  def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization,true')
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,PUT,POST,DELETE,OPTIONS')
      return response


  @app.route('/')
  def get_greeting():
    return jsonify({
              "success": True,
              "message": 'welcome'
          })

  @app.route('/movies', methods=['GET'])
  @requires_auth('view:movies')
  def retrieve_movies(payload):
      try:
          movies = Movie.query.all()
          movies = [movie.format() for movie in movies]
          return jsonify({
              "success": True,
              "movies": movies
          })
      except:
          abort(422)

  @app.route('/actors', methods=['GET'])
  @requires_auth('view:actors')
  def retrieve_actors(payload):
      try:
          actors = Actor.query.all()
          actors = [actor.format() for actor in actors]
          return jsonify({
              "success": True,
              "actors": actors
          })
      except:
          abort(422)

  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movie(payload):
      try:
          body = request.get_json()

          if body is None:
              abort(400)

          title = body.get('title', None)
          release_date = body.get('release_date', None)

          if title is None or release_date is None:
              abort(422)

          movie = Movie(title=title,
                        release_date=release_date)

          movie.insert()

          return jsonify({
              "success": True,
              "id": movie.id
          })
      except:
          abort(422)

  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(payload):
      try:
          body = request.get_json()

          if body is None:
              abort(400)

          name = body.get('name', None)
          age = body.get('age', None)
          gender = body.get('gender', None)
          movie_id = body.get('movie_id', None)

          if name is None or age is None or gender is None or movie_id is None:
              abort(422)

          actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)

          actor.insert()

          return jsonify({
              "success": True,
              "id": actor.id
          })
      except:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

          if movie is None:
              abort(422)

          movie.delete()

          return jsonify({
              'success': True,
              'deleted': movie_id
          })
      except:
        abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

          if actor is None:
              abort(422)

          actor.delete()

          return jsonify({
              'success': True,
              'deleted': actor_id
          })
      except:
          abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('update:movies')
  def update_movie(payload, movie_id):
      try:
          updated_movie = Movie.query.get(movie_id)

          if not updated_movie:
              abort(422)

          body = request.get_json()

          title = body.get('title', None)
          release_date = body.get('release_date', None)

          if title:
              updated_movie.title = title
          if release_date:
              updated_movie.release_date = release_date

          updated_movie.update()

          return jsonify({
              "success": True,
              "updated": updated_movie.format()
          })
      except:
          abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('update:actors')
  def update_actor(payload, actor_id):
      try:
          actor = Actor.query.get(actor_id)

          if not actor:
              abort(422)

          body = request.get_json()

          name = body.get('name', None)
          age = body.get('age', None)
          gender = body.get('gender', None)
          movie_id = body.get('movie_id', None)

          if name:
              actor.name = name
          if age:
              actor.age = age
          if gender:
              actor.gender = gender
          if movie_id:
              actor.movie_id = movie_id

          try:
              actor.update()
          except BaseException:
              abort(422)

          return jsonify({
              "success": True,
              'id': actor.id
          })
      except:
          abort(422)

  # Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable",
      }), 422

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(AuthError)
  def auth_error(auth_error):
      return jsonify({
          "success": False,
          "error": auth_error.status_code,
          "message": auth_error.error['description']
      }), auth_error.status_code



  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)