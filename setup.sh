#!/bin/sh
export AUTH0_DOMAIN="dev-mx9a4fvz.us.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="casting"

export DATABASE_URL="postgresql://postgres:0613@localhost:5432/fsndcapstone"
export FLASK_APP=app.py
export FLASK_ENVIRONMENT=debug
