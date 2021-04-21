from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)


# for sqlalchemy
DB_USER = 'root'
DB_PASSWORD = 'sesame80'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'HungryGators-19'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

db = SQLAlchemy(app)


from route import route_app
app.register_blueprint(route_app)

if __name__ == '__main__':
    app.debug = True
    app.run()

