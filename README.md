## Casting Agency Specifications

#### Full Stack Nano - Capstone 

Heroku Link: [http://capstoneljj.herokuapp.com/](http://capstoneljj.herokuapp.com/)

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process. The application must:

1. Allow casting assistant view actors and movies
2. Allow casting director to add or delete actors, and modify actors or movies
3. Allow executive to add or delete movies



### Main Files: Project Structure

```
├── auth
│    ├── __init_.py
│    └── auth.py
├── migrations
├── venv    				*** virtual env directory
├── app.py              	*** the main driver of the app. 
│                    			Includes all endpoints "flask run" to run after installing dependencies
├── models.py    			*** Database URLs and SQLAlchemy setup
├── auth0_token.json    	*** jwt_token config
├── run_flask_app.bat  
├── run_test_heroku.bat 	*** test app on heroku
├── test_app_heroku.py
├── run_test_local.bat 		*** test app locally
├── test_app.py
├── setup.bat         		*** setup environments, global variables, etc.
├── README.md
└── requirements.txt 		*** The dependencies we need to install with "pip install -r requirements.txt"
```



## Getting Started

### Pre-requisites and Local Development

#### Python 3.8

Developers using this project should already have Python3.8, pip installed on their local machines.

#### Virtual Environment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.
- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways
- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.
- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment

##### Database Setup

In terminal, create a database: `fsndcapstone` using the following command.

```
createdb fsndcapstone
```

##### Running the app

To run the application locally, execute the following commands (windows):

```bash
set AUTH0_DOMAIN=dev-mx9a4fvz.us.auth0.com 								# choose the auth0 domain
set ALGORITHMS=RS256
set API_AUDIENCE=casting 												# setup an api in auth0

set DATABASE_URL=postgresql://postgres:0613@localhost:5432/fsndcapstone # local database url
set FLASK_APP=app.py
set FLASK_ENVIRONMENT=debug
flask run
```

Optionally, you can use `setup.bat` script.

```bash
setup.bat
flask run
```

These commands put the application in development and directs our application to use the `app.py` file in our project folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default.

##### Running the test

To test the application locally,  you can use `run_test_local.bat`script.

To test the hosted app on heroku, run the script `run_test_heroku`instead.



## API Reference

## Getting Started

Base URL: This application can be run locally. The hosted version is at http://capstoneljj.herokuapp.com/.

Authentication: This application requires authentication to perform various actions. All the endpoints require various permissions, except the root endpoint, that are passed via the `Bearer` token.

The application has three different types of roles:

- Casting Assistant
  - can only view the list of actors and movies
  - has `view:actors, view:movies` permissions
- Casting Director
  - can perform all the actions that `Casting Assistant` can
  - can also create or delete an actor and update respective information for an actor and movie 
  - has `delete:actors, post:actors, update:actors, update:movies` permissions in addition to all the permissions that `Casting Assistant` role has
- Executive Producer
  - can perform all the actions that `Casting Director` can
  - can also create or delete a movie
  - has `post:movies, delete:movies` permissions in addition to all the permissions that `Casting Director` role has

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

In general, the API will return two error types when requests fail:

- 404: Resource Not Found
- 422: Not Processable

Furthermore, the API will return the following error when authentication fails:

- 400: invalid claims
- 401: authorization_header_missing

- 401: invalid header
- 401: token expired
- 403: unauthorized

### Endpoints

#### URL

The application can be run locally, host = `http://127.0.0.1:5000`

The hosted version is at host = `http://capstoneljj.herokuapp.com/`

#### GET 'greetings'

- Permission: None
  - Test health of this application
  - Return status code and a greeting message

- Sample: `curl {{host}}/`

```json
{
    "message": "welcome",
    "success": true
}
```

#### GET '/movies'

- Permission: `view:movies`
  - Fetches all movies from database
  - Return the status code and a list of movies in format

- Sample: `curl {{host}}/movies`

```json
{
    "movies": [
        {
            "actors": [
                {
                    "age": 25,
                    "gender": "F",
                    "id": 6,
                    "movie_id": 2,
                    "name": "Gustavo Wolfe"
                },
                {
                    "age": 25,
                    "gender": "F",
                    "id": 9,
                    "movie_id": 2,
                    "name": "Gustavo Wolfe"
                }
            ],
            "id": 2,
            "release_date": "Sat, 13 Jan 2018 00:00:00 GMT",
            "title": "test"
        },
        {
            "actors": [
                {
                    "age": 25,
                    "gender": "F",
                    "id": 4,
                    "movie_id": 1,
                    "name": "Gustavo Wolfe"
                },
                {
                    "age": 21,
                    "gender": "M",
                    "id": 1,
                    "movie_id": 1,
                    "name": "Clara Becker"
                }
            ],
            "id": 1,
            "release_date": "Thu, 13 Feb 2020 00:00:00 GMT",
            "title": "test_patch"
        }
    ],
    "success": true
}
```

#### GET '/actors'

- Permission: `view:actors`
  - Fetches all actors from database
  - Return the status code and a list of actors in format

- Sample: `curl {{host}}/actors`

```json
{
    "actors": [
        {
            "age": 25,
            "gender": "F",
            "id": 4,
            "movie_id": 1,
            "name": "Gustavo Wolfe"
        },
        {
            "age": 21,
            "gender": "M",
            "id": 1,
            "movie_id": 1,
            "name": "Clara Becker"
        }
    ],
    "success": true
}
```

#### POST '/actors'

- Permission: `post:actors`
  - Create an actor
  - Return the status code and id of the new actor
- Sample: `curl {{host}}/actors -X POST -H "Content-Type: application/json" -d "{"name": "Itzel Ramon", "age": "29", "gender": "F", "movie_id": "1"}"`

```json
{
    "id": 11,
    "success": true
}
```

#### DELETE '/actors'

- Permission: `delete:actors`
  - Delete an actor
  - Return the status code and id of the deleted actor
- Sample: `curl -X DELETE {{host}}/actors/9`

```json
{
    "deleted": 9,
    "success": true
}
```

#### PATCH '/actors'

- Permission: `update:actors`
  - Update an actor
  - Return the status code and id of the updated actor
- Sample: `curl {{host}}/actors/1 -X PATCH -H "Content-Type: application/json" -d "{"name": "Clara Becker", "age": "21"}"`

```json
{
    "id": 1,
    "success": true
}
```

#### PATCH '/movies'

- Permission: `update:movies`
  - Update a movie
  - Return the status code and the updated movie in format
- Sample: `curl {{host}}/actors/1 -X PATCH -H "Content-Type: application/json" -d "{"title": "The Godfather"}"`

```json
{
    "success": true,
    "updated": {
        "actors": [
            {
                "age": 25,
                "gender": "F",
                "id": 4,
                "movie_id": 1,
                "name": "Gustavo Wolfe"
            },
            {
                "age": 28,
                "gender": "F",
                "id": 11,
                "movie_id": 1,
                "name": "Itzel Ramon"
            },
            {
                "age": 21,
                "gender": "M",
                "id": 1,
                "movie_id": 1,
                "name": "Clara Becker"
            }
        ],
        "id": 1,
        "release_date": "Thu, 13 Feb 2020 00:00:00 GMT",
        "title": "The Godfather"
    }
}
```

#### POST '/movies'

- Permission: `post:movies`
  - Create a movie
  - Return the status code and id of the new movie
- Sample: `curl {{host}}/actors -X POST -H "Content-Type: application/json" -d "{"title": "The Departed", "release_date": "2006-06-15"}"`

```json
{
    "id": 8,
    "success": true
}
```

#### DELETE '/movies'

- Permission: `delete:movies`
  - Delete a movie
  - Return the status code and id of the deleted movie
- Sample: `curl -X DELETE {{host}}/movies/8`

```json
{
    "deleted": 8,
    "success": true
}
```

