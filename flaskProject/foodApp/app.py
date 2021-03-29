from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# for sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:sesame80@localhost:3306/HungryGators-19'
db = SQLAlchemy(app)


from route import route_app
app.register_blueprint(route_app)

if __name__ == '__main__':
    app.debug = True
    app.run()
