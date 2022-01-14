import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db , Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "fsndcapstone_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '0613', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Set up authentication tokens i
        with open('auth0_token.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["casting_assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["casting_director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["executive_producer"]["jwt_token"]
        self.auth_headers = {
            "casting_assistant": "Bearer %s" % assistant_jwt,
            "casting_director": "Bearer %s" % director_jwt,
            "executive_producer": "Bearer %s" % producer_jwt
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_greeting_success(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'welcome')


    def test_get_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_assistant"]
        }
        res = self.client().get('/movies', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(type(data['movies']) == list)

    def test_get_actors_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_assistant"]
        }
        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(type(data['actors']) == list)

    def test_get_movie_unauthorized_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_actor_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        res = self.client().post('/actors',
                                 json = {
                                      "name": "Gustavo Wolfe",
                                      "age": "25",
                                      "gender": "F",
                                      "movie_id": "2"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_actor_failed_unexpected_movieId(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        res = self.client().post('/actors',
                                 json = {
                                      "name": "Gustavo Wolfe",
                                      "age": "25",
                                      "gender": "F",
                                      "movie_id": "10000"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_actor_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        # create a actor to be deleted
        res = self.client().post('/actors',
                                 json = {
                                      "name": "Gustavo Wolfe",
                                      "age": "25",
                                      "gender": "F",
                                      "movie_id": "1"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        actor_id = data['id']

        # delete this new actor
        res = self.client().delete('/actors/%s'%actor_id, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor_failed_unexpeced_id(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        res = self.client().delete('/actors/10000', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_actor_unauthorized_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


    def test_create_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().post('/movies',
                                 json = {
                                  "title": "test",
                                  "release_date": "2018-01-13"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_movies_missing_field(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().post('/movies',
                                 json = {
                                  "title": "test",
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['success'] == False)

    def test_delete_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }

        # create a new movie to be deleted
        res = self.client().post('/movies',
                                 json = {
                                  "title": "test",
                                  "release_date": "2018-01-13"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        movie_id = data['id']

        # delete this new movie
        res = self.client().delete('/movies/%s'%movie_id, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movies_failed(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().delete('/movies/10000', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['success'] == False)

    def test_update_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().patch('/movies/1',
                                 json = {
                                  "title": "test_patch",
                                  "release_date": "2020-02-13"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movies_failed_unexpeted_id(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().patch('/movies/1000',
                                 json = {
                                  "title": "test_patch",
                                  "release_date": "2020-02-13"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_update_actor_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().patch('/actors/1',
                                 json = {
                                     "name": "Clara Becker",
                                     "age": "21"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor_failed_unexpected_id(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = self.client().patch('/actors/1000',
                                 json = {
                                     "name": "Clara Becker",
                                     "age": "21"
                                    } , headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()