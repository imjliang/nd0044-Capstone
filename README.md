## Casting Agency Specifications

## Full Stack Nano - Capstone 



- The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.
- Models:
  - Movies with attributes title and release date
  - Actors with attributes name, age and gender
- Endpoints:
  - GET /actors and /movies
  - DELETE /actors/ and /movies/
  - POST /actors and /movies and
  - PATCH /actors/ and /movies/
- Roles:
  - Casting Assistant
    - Can view actors and movies
  - Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
  - Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database
- Tests:
  - One test for success behavior of each endpoint
  - One test for error behavior of each endpoint
  - At least two tests of RBAC for each role





Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

You have been called on to demonstrate your newly learned skills to create a full stack drink menu application. The application must:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

### Main Files: Project Structure

```
├── backend
│   ├── src
│   │    ├── auth
│   │          ├── __init_.py
│   │          └── auth.py
│   │    ├── database
│   │          ├── __init_.py
│   │          ├── database.db
│   │          └── models.py    *** Database URLs and SQLAlchemy setup
│   │    ├── venv    *** virtual env directory
│   │    ├── __init_.py
│   │    └── api.py *** the main driver of the app. 
│   │                   Includes all endpoints "flask run" to run after installing dependencies
│   ├── README.md
│   └── udacity-fsnd-udaspicelatte.postman_collection.json
├── frontend
├── README.md
└── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
```

### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. 

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)

### Authors

Jinjin Liang authored the API (`api.py`), authorization handling (`auth.py`), and this README. All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/).

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.

## Roles

- Barista
  - can `get:drinks-detail`
- Manager
  - can perform all actions

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

#### GET '/drinks'

- Permission: None
  - Fetches all drinks from database
  - Return the status code and a list of drinks in short-format

- Sample: `curl http://127.0.0.1:5000/drinks`

```json
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 3
                }
            ],
            "title": "Water-"
        },
        {
            "id": 3,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 3
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```

#### GET '/drinks-detail'

- Permission: `get:drinks-detail`
  - Fetches all drinks from database
  - Return the status code and a list of drinks in long-format

- Sample: `curl http://127.0.0.1:5000/drinks`-detail

```json
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 3
                }
            ],
            "title": "Water-"
        },
        {
            "id": 3,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 3
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```

#### POST '/drinks'

- Permission: `post:drinks`
  - Create a new drink in the drink table
  - Return the status code and the created drinks in the long format

- Sample: `curl http://127.0.0.1:5000/drinks -X POST -H "Content-Type: application/json" -d "{"title": "Water66", "recipe": [{
          "name": "Water", "color": "red","parts": 1 }]}"`

```json
{
    "drinks": [
        {
            "id": 9,
            "recipe": [
                {
                    "color": "red",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water7"
        }
    ],
    "success": true
}
```

#### PATCH '/drinks/${drink_id}'

- Permission: `patch:drinks`
  - Update the drinks for id =  drink_id
  - Return the status code and the updated drinks in the long format

- Sample: `curl http://127.0.0.1:5000/drinks/2 -X PATCH -H "Content-Type: application/json" -d "{"title": "Water-"}"`

```json
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 3
                }
            ],
            "title": "Water-"
        }
    ],
    "success": true
}
```

#### DELETE '/drinks/${drink_id}'

- Permission: `delete:drinks`

  - Delete the drinks for id =  drink_id
  - Return the status code and the id of the delete record

- Sample: ``curl -X DELETE http://127.0.0.1:5000/drinks/9`"`

  ```json
  {
      "drinks": "9",
      "success": true
  }
  ```
