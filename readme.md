# Create environment

python3 -m venv venv

# Enter environment

. venv/bin/activate

# export FLASK_APP

export FLASK_APP=<file python> ex: export FLASK_APP=main.py

# Run app

flask run

#

# Export packages

pip3 freeze > requirements.txt

# Install package from requirements.txt

pip3 install -r requirements.txt

# Packages

pip3 install flask
pip3 install passlib
pip3 install flask-marshmallow
pip3 install Flask-Mail

## Mysql

pip3 install flask flask-sqlalchemy
pip3 install pymysql

# Athour

pip3 install flask-jwt-extended

# swagger

pip3 install flask_swagger flask_swagger_ui

# Common Errors

Instance of 'SQLAlchemy' has no 'Column' member (no-member) : https://stackoverflow.com/questions/53975234/instance-of-sqlalchemy-has-no-column-member-no-member
