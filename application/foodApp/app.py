from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import request, render_template, make_response
from sqlalchemy import or_, and_
import os
from sqlalchemy import ForeignKey

import pymysql
pymysql.install_as_MySQLdb()



app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images'
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)

# for sqlalchemy
# DB_USER = 'team1'
# DB_PASSWORD = '12345678'
# DB_HOST = 'localhost'
# DB_PORT = 3306
# DB_NAME = 'restaurant_db'

# for sqlalchemy
DB_USER = 'root'
DB_PASSWORD = 'Tinthuzaraye92!'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'DatabaseDB'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

db = SQLAlchemy(app)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A restaurant has a name, address, phone, zip, image, cuisine style, and description:
    name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(45), nullable=False)
    zip_code = db.Column(db.String(45), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    # constructor for creating a restaurant
    def __init__(self, name, address, phone_number, zip_code, image, cuisine, description):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.image = image
        self.cuisine = cuisine
        self.description = description


class Menu(db.Model):
    __tablename__ = 'menu'

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A menu item (entry) has a name, price, and quantity:
    restaurant_id = db.Column(db.Integer, ForeignKey("restaurant.id"), nullable=False)
    name = db.Column(db.String(45))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)

    # Constructor for creating a menu item (entry)
    def __init__(self, name, price, quantity, restaurant_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.restaurant_id = restaurant_id


# method for adding a restaurant
def create_restaurant(new_name, new_address, new_phone, new_zip, new_image, cuisine, description):
    # Create a restaurant with the provided input.
    # At first, we will trust the user.

    # This line maps to (the Restaurant.__init__ method)
    restaurant = Restaurant(new_name, new_address, new_phone, new_zip, new_image, cuisine, description)

    # Actually add this restaurant to the database
    db.session.add(restaurant)

    # Save all pending changes to the database
    db.session.commit()

    return restaurant


# method for adding an entry
def create_entry(new_name, new_price, new_quantity, restaurant_id):
    # Create an entry with the provided input.
    # At first, we will trust the user.

    # This line maps to (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity, restaurant_id)

    # Actually add this entry to the database
    db.session.add(entry)

    # Save all pending changes to the database
    db.session.commit()

    return entry


# method for deleting an entry
def delete_entry(new_name, new_price, new_quantity):
    # Delete an entry with the provided input.
    # At first, we will trust the user.

    # This line maps to (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity)

    # Actually delete this entry from the database
    db.session.delete(entry)

    # Save all pending changes to the database
    db.session.commit()

    return entry


# endpoint for displaying the entries in a menu
@app.route('/menu', methods=['GET', 'POST'])
def search_menu():
    if request.method == "POST":
        restaurant_id = request.form['restaurant_id']
        restaurant_name = request.form['restaurant_name']
        result = Menu.query.filter_by(restaurant_id=restaurant_id).all()
        menus = [{
            "id": row.id,
            "name": row.name,
            "price": row.price,
            "quantity": row.quantity,
        } for row in result]
        return render_template('menu.html', name=restaurant_name, id=restaurant_id, menus=menus)

    elif request.method == "GET":
        restaurant_name, restaurant_id = request.args.get("name"), request.args.get("id", None)
        if restaurant_id is not None:
            result = Menu.query.filter_by(restaurant_id=restaurant_id).all()
            menus = [{
                "id": row.id,
                "name": row.name,
                "price": row.price,
                "quantity": row.quantity,
            } for row in result]
            return render_template('menu.html', name=restaurant_name, id=restaurant_id, menus=menus)
        else:
            return render_template('menu.html', name=restaurant_name, id=restaurant_id, menus=[])


# endpoint for deleting an entry in a menu
@app.route('/menu_delete', methods=['POST'])
def menu_delete():
    restaurant_id = request.form['restaurant_id']
    restaurant_name = request.form['restaurant_name']
    menu_id = request.form['menu_id']
    Menu.query.filter_by(id=menu_id).delete()
    db.session.commit()
    result = Menu.query.filter_by(restaurant_id=restaurant_id).all()
    menus = [{
        "id": row.id,
        "name": row.name,
        "price": row.price,
        "quantity": row.quantity,
    } for row in result]
    return render_template('menu.html', name=restaurant_name, id=restaurant_id, menus=menus)


# endpoint for searching a restaurant
@app.route('/', methods=['GET', 'POST'])
def search_restaurant():
    if request.method == "POST":
        query = request.form['restaurant']
        cuisine = request.form['cuisine']
        if query:
            query = '%{}%'.format(query)
            result = db.session.query(Restaurant).filter(
                and_(
                    Restaurant.cuisine == cuisine if cuisine != 'all cuisines' else True,
                    or_(
                        Restaurant.name.like(query),
                        or_(
                            Restaurant.address.like(query),
                            or_(
                                Restaurant.phone_number.like(query),
                                Restaurant.zip_code.like(query),
                                or_(
                                    Restaurant.description.like(query)
                                )
                            )
                        )
                    )
                )
            )
        else:
            result = db.session.query(Restaurant).filter(
                and_(
                    Restaurant.cuisine == cuisine if cuisine != 'all cuisines' else True,
                    True
                )
            )

        restaurants = [{
            "id": row.id,
            "name": row.name,
            "address": row.address,
            "phone_number": row.phone_number,
            "zip_code": row.zip_code,
            "image": row.image,
            "cuisine": row.cuisine,
            "description": row.description
        } for row in result]

        # disabling cache
        r = make_response(render_template('index.html', restaurants=restaurants))
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r
    r = make_response(render_template('index.html'))
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# endpoint for adding a restaurant
@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'GET':
        return render_template('add_restaurant.html')

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    # Get the incoming data from the request.form dictionary.
    # The values on the right, inside get(), correspond to the 'name'
    # values in the HTML form that was submitted.

    # create a file path for an image
    file_path = ""
    file = request.files["image"]
    if file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    # retrieve post form data by each field
    restaurant_name = request.form.get('name_field')
    restaurant_address = request.form.get('address_field')
    restaurant_phone = request.form.get('phone_field')
    restaurant_zip = request.form.get('zip_field')
    restaurant_cuisine = request.form.get('cuisine')
    restaurant_description = request.form.get('description')

    # create a restaurant to be added
    restaurant = create_restaurant(restaurant_name, restaurant_address, restaurant_phone,
                                   restaurant_zip, file_path, restaurant_cuisine, restaurant_description)
    return render_template('add_restaurant.html', restaurant=restaurant)


# endpoint for deleting a restaurant
@app.route('/delete', methods=['GET', 'POST'])
def remove_restaurant():
    if request.method == 'GET':
        # retrieve the list of restaurants to be deleted
        restaurants = Restaurant.query.all()
        return render_template('delete_restaurant.html', restaurants=restaurants)

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    # Get the incoming data from the request.form dictionary.
    # The values on the right, inside get(), correspond to the 'name'
    # values in the HTML form that was submitted.

    restaurant_name = request.form.get('name_field')
    # Menu.query.filter_by(name=restaurant_name).delete()
    # db.session.commit()

    # retrieve a restaurant by restaurant name
    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    db.session.delete(restaurant)
    db.session.commit()

    # delete the file path for an image
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], restaurant.image)
    if os.path.isfile(file_path):
        os.remove(file_path)

    # retrieve the list of restaurants to be deleted
    restaurants = Restaurant.query.all()
    return render_template('delete_restaurant.html', restaurants=restaurants, deleted=restaurant_name)


# endpoint for adding an entry to a menu
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'GET':
        restaurant_name, restaurant_id = request.args.get("name"), request.args.get("id")
        return render_template('add_entry.html', name=restaurant_name, id=restaurant_id)

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    # Get the incoming data from the request.form dictionary.
    # The values on the right, inside get(), correspond to the 'name'
    # values in the HTML form that was submitted.

    # retrieve post form data by each field
    entry_name = request.form.get('name_field')
    entry_price = request.form.get('price_field')
    entry_quantity = request.form.get('quantity_field')
    restaurant_id = request.form.get('restaurant_id')
    restaurant_name = request.form.get('restaurant_name')

    entry = create_entry(entry_name, entry_price, entry_quantity, restaurant_id)
    return render_template('add_entry.html', entry=entry, name=restaurant_name, id=restaurant_id)

@app.route("/home.html")
def home():
    return render_template("home.html", content="Testing")

@app.route("/aboutus.html")
def about():
    return render_template("aboutus.html", content="Testing")

@app.route("/jas.html")
def jas():
    return render_template("jas.html", content="Testing")

@app.route("/bran.html")
def bran():
    return render_template("bran.html", content="Testing")

@app.route("/rob.html")
def rob():
    return render_template("rob.html", content="Testing")

@app.route("/gurjot.html")
def gur():
    return render_template("gurjot.html", content="Testing")

@app.route("/tin.html")
def tin():
    return render_template("tin.html", content="Testing")

@app.route("/pan.html")
def pan():
    return render_template("pan.html", content="Testing")

@app.route("/regowner.html")
def regowner():
    return render_template("regowner.html", content="Testing")

@app.route("/regdriver.html")
def regdriver():
    return render_template("regdriver.html", content="Testing")

@app.route("/logindriver.html")
def logindriver():
    return render_template("logindriver.html", content="Testing")

@app.route("/loginowner.html")
def loginowner():
    return render_template("loginowner.html", content="Testing")


@app.route("/regsf.html")
def regsf():
    return render_template("regsf.html", content="Testing")

@app.route("/loginsf.html")
def logsf():
    return render_template("loginsf.html", content="Testing")

@app.route("/delidriver.html")
def delidriver():
    return render_template("delidriver.html", content="Testing")






if __name__ == '__main__':
    app.debug = True
    app.run()
