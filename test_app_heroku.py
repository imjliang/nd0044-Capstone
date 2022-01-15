import unittest
import json
import requests

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.heroku_url = "https://capstoneljj.herokuapp.com/"

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
        res = requests.get(self.heroku_url + '/')
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'welcome')


    def test_get_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_assistant"]
        }
        res = requests.get(self.heroku_url + '/movies', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(type(data['movies']) == list)

    def test_get_actors_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_assistant"]
        }
        res = requests.get(self.heroku_url + '/actors', headers=header_obj)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(type(data['actors']) == list)

    def test_get_movie_unauthorized_401(self):
        res = requests.get(self.heroku_url + '/movies')
        data = res.json()


        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_create_actor_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        res = requests.post(self.heroku_url + '/actors',
                                 json = {
                                      "name": "Gustavo Wolfe",
                                      "age": "25",
                                      "gender": "F",
                                      "movie_id": "2"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_actor_failed_unexpected_movieId(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        res = requests.post(self.heroku_url + '/actors',
                                 json = {
                                      "name": "Gustavo Wolfe",
                                      "age": "25",
                                      "gender": "F",
                                      "movie_id": "10000"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_actor_success(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        # create a actor to be deleted
        res = requests.post(self.heroku_url + '/actors',
                                 json = {
                                      "name": "Gustavo Wolfe",
                                      "age": "25",
                                      "gender": "F",
                                      "movie_id": "1"
                                    } , headers=header_obj)
        data = res.json()
        actor_id = data['id']

        # delete this new actor
        res = requests.delete(self.heroku_url + '/actors/%s'%actor_id, headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor_failed_unexpeced_id(self):
        header_obj = {
            "Authorization": self.auth_headers["casting_director"]
        }
        res = requests.delete(self.heroku_url + '/actors/10000', headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_actor_unauthorized_401(self):
        res = requests.get(self.heroku_url + '/actors')
        data = res.json()


        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


    def test_create_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.post(self.heroku_url + '/movies',
                                 json = {
                                  "title": "test",
                                  "release_date": "2018-01-13"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_movies_missing_field(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.post(self.heroku_url + '/movies',
                                 json = {
                                  "title": "test",
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['success'] == False)

    def test_delete_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }

        # create a new movie to be deleted
        res = requests.post(self.heroku_url + '/movies',
                                 json = {
                                  "title": "test",
                                  "release_date": "2018-01-13"
                                    } , headers=header_obj)
        data = res.json()
        movie_id = data['id']

        # delete this new movie
        res = requests.delete(self.heroku_url + '/movies/%s'%movie_id, headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movies_failed(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.delete(self.heroku_url + '/movies/10000', headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['success'] == False)

    def test_update_movies_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.patch(self.heroku_url + '/movies/1',
                                 json = {
                                  "title": "test_patch",
                                  "release_date": "2020-02-13"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movies_failed_unexpeted_id(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.patch(self.heroku_url + '/movies/1000',
                                 json = {
                                  "title": "test_patch",
                                  "release_date": "2020-02-13"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_update_actor_success(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.patch(self.heroku_url + '/actors/1',
                                 json = {
                                     "name": "Clara Becker",
                                     "age": "21"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor_failed_unexpected_id(self):
        header_obj = {
            "Authorization": self.auth_headers["executive_producer"]
        }
        res = requests.patch(self.heroku_url + '/actors/1000',
                                 json = {
                                     "name": "Clara Becker",
                                     "age": "21"
                                    } , headers=header_obj)
        data = res.json()
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()