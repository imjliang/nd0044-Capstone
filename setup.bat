@echo off

set AUTH0_DOMAIN=dev-mx9a4fvz.us.auth0.com
set ALGORITHMS=RS256
set API_AUDIENCE=casting

set DATABASE_URL=postgresql://postgres:0613@localhost:5432/fsndcapstone
set FLASK_APP=app.py
set FLASK_ENVIRONMENT=debug
echo "setup app completed!"