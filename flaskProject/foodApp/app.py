from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import request, render_template
from sqlalchemy import or_
import os
from sqlalchemy import ForeignKey


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)


# for sqlalchemy
DB_USER = 'team1'
DB_PASSWORD = '12345678'
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'restaurant_db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

db = SQLAlchemy(app)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A restaurant has a name, address, phone, and zip:
    name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(45), nullable=False)
    phone_number = db.Column(db.String(45), nullable=False)
    zip_code = db.Column(db.String(45), nullable=False)
    image = db.Column(db.String(100), nullable=False)

    def __init__(self, name, address, phone_number, zip_code, image):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.image = image


class Menu(db.Model):
    __tablename__ = 'menu'
    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A menu item (entry) has a name, price, and quantity:
    restaurant_id = db.Column(db.Integer, ForeignKey("restaurant.id"), nullable=False)
    name = db.Column(db.String(45))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)
    # image = db.Column(db.Text, nullable=False)

    def __init__(self, name, price, quantity, restaurant_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.restaurant_id = restaurant_id


def create_restaurant(new_name, new_address, new_phone, new_zip, new_image):
    # Create a restaurant with the provided input.
    # At first, we will trust the user.

    # This line maps to line 14 above (the Restaurant.__init__ method)
    restaurant = Restaurant(new_name, new_address, new_phone, new_zip, new_image)

    # Actually add this restaurant to the database
    db.session.add(restaurant)

    # Save all pending changes to the database
    db.session.commit()

    return restaurant


def delete_restaurant(new_name, new_address, new_phone, new_zip):
    # Delete a restaurant with the provided name.
    # At first, we will trust the user.

    # This line filters the query by restaurant name
    restaurant = Restaurant(new_name, new_address, new_phone, new_zip).query.filter_by(name=new_name).first()

    # Actually delete this restaurant from the database
    db.session.delete(restaurant)

    # Save all pending changes to the database
    db.session.commit()

    return restaurant


def create_entry(new_name, new_price, new_quantity, restaurant_id):
    # Create an entry with the provided input.
    # At first, we will trust the user.

    # This line maps to line 34 above (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity, restaurant_id)

    # Actually add this entry to the database
    db.session.add(entry)

    # Save all pending changes to the database
    db.session.commit()

    return entry


def delete_entry(new_name, new_price, new_quantity):
    # Delete an entry with the provided input.
    # At first, we will trust the user.

    # This line maps to line 34 above (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity)

    # Actually delete this entry from the database
    db.session.delete(entry)

    # Save all pending changes to the database
    db.session.commit()

    return entry

# endpoint for searching the menu in the menu table in the database
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


# endpoint for deleting entries from the menu table in the database
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


# endpoint for searching restaurants in the restaurants table in the database
@app.route('/', methods=['GET', 'POST'])
def search_restaurant():
    if request.method == "POST":
        query = request.form['restaurant']
        query = '%{}%'.format(query)
        result = db.session.query(Restaurant).filter(or_(
            Restaurant.name.like(query),
            or_(
                Restaurant.address.like(query),
                or_(
                    Restaurant.phone_number.like(query),
                    Restaurant.zip_code.like(query)
                )
            )
        )
        )

        restaurants = [{
            "id": row.id,
            "name": row.name,
            "address": row.address,
            "phone_number": row.phone_number,
            "zip_code": row.zip_code,
            "image": row.image
        } for row in result]

        return render_template('index.html', restaurants=restaurants)
    return render_template('index.html')


# endpoint for adding restaurants to restaurant table in the database
@app.route('/add', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'GET':
        return render_template('add_restaurant.html')

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    # Get the incoming data from the request.form dictionary.
    # The values on the right, inside get(), correspond to the 'name'
    # values in the HTML form that was submitted.
    file_path = ""
    file = request.files["image"]
    if file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    restaurant_name = request.form.get('name_field')
    restaurant_address = request.form.get('address_field')
    restaurant_phone = request.form.get('phone_field')
    restaurant_zip = request.form.get('zip_field')

    restaurant = create_restaurant(restaurant_name, restaurant_address, restaurant_phone, restaurant_zip, file_path)
    return render_template('add_restaurant.html', restaurant=restaurant)


# endpoint for deleting restaurants from the restaurant table in the database
@app.route('/delete', methods=['GET', 'POST'])
def remove_restaurant():
    if request.method == 'GET':
        # Display the list of restaurants to delete from database upon rendering the page
        restaurants = Restaurant.query.all()
        return render_template('delete_restaurant.html', restaurants=restaurants)

    # Because we 'returned' for a 'GET', if we get to this next bit, we must
    # have received a POST

    # Get the incoming data from the request.form dictionary.
    # The values on the right, inside get(), correspond to the 'name'
    # values in the HTML form that was submitted.

    restaurant_name = request.form.get('name_field')
    restaurant_address = request.form.get('address_field')
    restaurant_phone = request.form.get('phone_field')
    restaurant_zip = request.form.get('zip_field')

    restaurant = delete_restaurant(restaurant_name, restaurant_address, restaurant_phone, restaurant_zip)
    return render_template('delete_restaurant.html', restaurant=restaurant)


# endpoint for adding entries to the menu table in the database
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

    entry_name = request.form.get('name_field')
    entry_price = request.form.get('price_field')
    entry_quantity = request.form.get('quantity_field')
    restaurant_id = request.form.get('restaurant_id')
    restaurant_name = request.form.get('restaurant_name')

    entry = create_entry(entry_name, entry_price, entry_quantity, restaurant_id)
    return render_template('add_entry.html', entry=entry, name=restaurant_name, id=restaurant_id)


if __name__ == '__main__':
    app.debug = True
    app.run()

