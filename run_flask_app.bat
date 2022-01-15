@echo off
set FLASK_APP=app.py
set FLASK_ENVIRONMENT=debug
flask run
echo "app run successfully!"