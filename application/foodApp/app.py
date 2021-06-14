from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template, make_response
from sqlalchemy import or_, and_
import os
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


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
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'HungryGators-19'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

db = SQLAlchemy(app)

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer())
    user_name = db.Column(db.String(45))
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(45))
    mode = db.Column(db.String(45))
    total = db.Column(db.Float())
    items = db.Column(db.JSON())
    active = db.Column(db.Boolean())
    driver_id = db.Column(db.Integer())
    restaurant_name = db.Column(db.String(45))

    def __init__(self, user_id, user_name, address, phone_number, mode, total, items, active, driver_id, restaurant_name):
        self.user_id = user_id
        self.user_name = user_name
        self.address = address
        self.phone_number = phone_number
        self.mode = mode
        self.total = total
        self.items = items
        self.active = active
        self.driver_id = driver_id
        self.restaurant_name = restaurant_name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Integer(), nullable=False)

    def __init__(self, name, email, password, user_type):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type

    def __repr__(self):
        return "<{}:{}>".format(self.name, self.email)


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A restaurant has a name, address, phone, zip, image, cuisine style, and description:
    owner_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(45), nullable=False)
    zip_code = db.Column(db.String(45), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price_tag = db.Column(db.String(5))


    # constructor for creating a restaurant
    def __init__(self, owner_id, name, address, phone_number, zip_code, image, cuisine, description, price_tag):
        self.owner_id = owner_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.image = image
        self.cuisine = cuisine
        self.description = description
        self.price_tag = price_tag


class Menu(db.Model):
    __tablename__ = 'menu'

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A menu item (entry) has a name, price, and quantity:
    restaurant_id = db.Column(db.Integer, ForeignKey("restaurant.id"), nullable=False)
    name = db.Column(db.String(45))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    # Constructor for creating a menu item (entry)
    def __init__(self, name, price, quantity, restaurant_id, active):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.restaurant_id = restaurant_id
        self.active = active


# method for adding a restaurant
def create_restaurant(owner_id, new_name, new_address, new_phone, new_zip, new_image, cuisine, description, price_tag):
    # Create a restaurant with the provided input.
    # At first, we will trust the user.

    # This line maps to (the Restaurant.__init__ method)
    restaurant = Restaurant(owner_id, new_name, new_address, new_phone, new_zip, new_image, cuisine, description, price_tag)

    # Actually add this restaurant to the database
    db.session.add(restaurant)

    # Save all pending changes to the database
    db.session.commit()

    return restaurant


# method for adding an entry
def create_entry(new_name, new_price, new_quantity, restaurant_id, active):
    # Create an entry with the provided input.
    # At first, we will trust the user.

    # This line maps to (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity, restaurant_id, active)

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
        user_id = request.form['user_id']
        user_name = request.form['user_name']
        result = Menu.query.filter_by(restaurant_id=restaurant_id).all()
        menus = [{
            "id": row.id,
            "name": row.name,
            "price": row.price,
            "quantity": row.quantity,
        } for row in result if row.active]
        return render_template('menu_for_user.html', name=restaurant_name, id=restaurant_id, user_name=user_name, user_id=user_id, menus=menus)

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
        search_query = request.form['restaurant']
        cuisine = request.form['cuisine']
        user_name = request.form['user_name']
        user_id = request.form['user_id']
        if search_query:
            query = '%{}%'.format(search_query)
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
            "description": row.description,
            "price_tag": row.price_tag
        } for row in result]

        # disabling cache
        r = make_response(render_template('index.html', query=search_query, restaurants=restaurants, user_name=user_name, user_id=user_id))
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


# endpoint for displaying restaurants
@app.route('/show_restaurants', methods=['GET'])
def show_restaurant():
    owner_id = request.args.get('owner_id')
    owner_name = request.args.get('owner_name')
    result = db.session.query(Restaurant).filter(Restaurant.owner_id == owner_id)
    restaurants = [{
        "id": row.id,
        "name": row.name,
        "address": row.address,
        "phone_number": row.phone_number,
        "zip_code": row.zip_code,
        "image": row.image,
        "cuisine": row.cuisine,
        "description": row.description,
        "price_tag": row.price_tag
    } for row in result]
    return render_template('display_restaurant.html', restaurants=restaurants, owner_id=owner_id, owner=owner_name)

@app.route('/delete_restaurant', methods=['GET'])
def delete_restaurant():
    restaurant_id = request.args.get('id')
    owner_id = request.args.get('owner_id')
    owner_name = request.args.get('owner_name')
    restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
    db.session.delete(restaurant)
    db.session.commit()
    return render_template("add_restaurant.html", owner_id=owner_id, owner_name=owner_name)


# endpoint for adding a restaurant
@app.route('/add', methods=['POST'])
def add_restaurant():

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
    owner_id = request.form.get('owner_id')
    owner_name = request.form.get('owner_name')
    restaurant_name = request.form.get('name_field')
    restaurant_address = request.form.get('address_field')
    restaurant_phone = request.form.get('phone_field')
    restaurant_zip = request.form.get('zip_field')
    restaurant_cuisine = request.form.get('cuisine')
    restaurant_description = request.form.get('description')
    restaurant_price_tag = request.form.get('price_tag')

    # create a restaurant to be added
    restaurant = create_restaurant(owner_id, restaurant_name, restaurant_address, restaurant_phone,
                                   restaurant_zip, file_path, restaurant_cuisine, restaurant_description, restaurant_price_tag)
    return render_template('add_restaurant.html', restaurant=restaurant, owner_id=owner_id, owner_name=owner_name)


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

    entry = create_entry(entry_name, entry_price, entry_quantity, restaurant_id, False)
    return render_template('add_entry.html', entry=entry, name=restaurant_name, id=restaurant_id)



@app.route("/home.html")
def home():
    return render_template("home.html", content="Testing")

@app.route("/aboutus.html")
def about():
    return render_template("aboutus.html", content="Testing")

@app.route("/bran.html")
def bran():
    return render_template("bran.html", content="Testing")

@app.route("/jas.html")
def jas():
    return render_template("jas.html", content="Testing")

@app.route("/pan.html")
def pan():
    return render_template("pan.html", content="Testing")

@app.route("/rob.html")
def rob():
    return render_template("rob.html", content="Testing")

@app.route("/tin.html")
def tin():
    return render_template("tin.html", content="Testing")

@app.route("/gurjot.html")
def gurjot():
    return render_template("gurjot.html", content="Testing")

@app.route("/regowner.html")
def owner():
    return render_template("regowner.html", content="Testing")

@app.route("/loginowner.html")
def logowner():
    return render_template("loginowner.html", content="Testing")

@app.route("/regdriver.html")
def driver():
    return render_template("regdriver.html", content="Testing")

@app.route("/logindriver.html")
def logdriver():
    return render_template("logindriver.html", content="Testing")

@app.route("/regadmin.html")
def admin():
    return render_template("regadmin.html", content="Testing")

@app.route("/loginadmin.html")
def logadmin():
    return render_template("loginadmin.html", content="Testing")

@app.route("/regsf.html")
def regsf():
    return render_template("regsf.html", content="Testing")


# endpoint for registering as a SFSU member
@app.route("/register_sfsu", methods=['POST'])
def register():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password_repeat']

    if password != password_repeat:
        return render_template("regsf.html", failure="Passwords do not match")

    result = db.session.query(User).filter(User.email == email)
    user = [{
        "name": row.name,
        "email": row.email,
        "password": row.password
    } for row in result]

    if len(user) != 0:
        return render_template("regsf.html", failure="Email already registered")

    db.session.add(User(full_name, email, generate_password_hash(password), 0))
    db.session.commit()
    return render_template("loginsf.html", success="Registration Successful")


# endpoint for logging in as a SFSU member
@app.route("/login_sfsu", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("loginsf.html")

    email = request.form['email']
    password = request.form['password']
    result = db.session.query(User).filter(User.email == email)

    for row in result:
        print(row)
    user = [{
        "id": row.id,
        "name": row.name,
        "email": row.email,
        "password": row.password,
        "user_type": row.user_type
    } for row in result]

    if len(user) == 0:
        return render_template("loginsf.html", failure="No user found")
    elif not check_password_hash(user[0]['password'], password):
        return render_template("loginsf.html", failure="Incorrect password")
    else:
        if user[0]["user_type"] == 0:
            return render_template("index.html", user_id=user[0]['id'], user_name=user[0]['name'])
        elif user[0]["user_type"] == 1:
            return render_template("add_restaurant.html", owner_id=user[0]['id'], owner_name=user[0]['name'])
        elif user[0]["user_type"] == 2:
            active_orders = db.session.query(Orders).filter(Orders.active == True)
            orders = [{
                'restaurant_name': row.restaurant_name,
                "order_id": row.id,
                "user_id": row.user_id,
                "user_name": row.user_name,
                "address": row.address,
                "phone_number": row.phone_number,
                "mode": row.mode,
                "total": row.total,
                "items": row.items
            } for row in active_orders]
            return render_template("vieworder.html", orders=orders, driver_id=user[0]['id'], driver_name=user[0]['name'])
        elif user[0]["user_type"] == 3:
            menus = db.session.query(Menu, Restaurant).filter(Menu.restaurant_id == Restaurant.id)
            menus = [{
                'id': m.id,
                'name': m.name,
                'price': m.price,
                'quantity': m.quantity,
                'is_active': m.active,
                'restaurant_name': r.name,
                'cuisine': r.cuisine
            } for (m, r) in menus]
            return render_template("activate_menu.html", menus=menus, admin_id=user[0]['id'], admin_name=user[0]['name'])



# endpoint for registering as a restaurant owner
@app.route("/register_restaurant_owner", methods=['POST'])
def register_restaurant_owner():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password_repeat']

    if password != password_repeat:
        return render_template("regowner.html", failure="Passwords do not match")

    result = db.session.query(User).filter(User.email == email)
    user = [{
        "name": row.name,
        "email": row.email,
        "password": row.password
    } for row in result]

    if len(user) != 0:
        return render_template("regowner.html", failure="Email already registered")

    db.session.add(User(full_name, email, generate_password_hash(password), 1))
    db.session.commit()
    return render_template("loginsf.html", success="Registration Successful")


# endpoint for registering as a delivery driver
@app.route("/register_delivery_driver", methods=['POST'])
def register_delivery_driver():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password_repeat']

    if password != password_repeat:
        return render_template("regdriver.html", failure="Passwords do not match")

    result = db.session.query(User).filter(User.email == email)
    user = [{
        "name": row.name,
        "email": row.email,
        "password": row.password
    } for row in result]

    if len(user) != 0:
        return render_template("regdriver.html", failure="Email already registered")

    db.session.add(User(full_name, email, generate_password_hash(password), 2))
    db.session.commit()
    return render_template("loginsf.html", success="Registration Successful")

# endpoint for registering as the admin
@app.route("/register_admin", methods=['POST'])
def register_admin():
    full_name = request.form['full_name']
    email = request.form['email']
    password = request.form['password']
    password_repeat = request.form['password_repeat']

    if password != password_repeat:
        return render_template("regadmin.html", failure="Passwords do not match")

    result = db.session.query(User).filter(User.email == email)
    user = [{
        "name": row.name,
        "email": row.email,
        "password": row.password
    } for row in result]

    if len(user) != 0:
        return render_template("regadmin.html", failure="Email already registered")

    db.session.add(User(full_name, email, generate_password_hash(password), 3))
    db.session.commit()
    return render_template("loginadmin.html", success="Registration Successful")


# endpoint for adding menu items to cart
@app.route("/cart", methods=['POST'])
def cart():
    menu_ids = request.form.getlist("menu_id[]")
    menu_names = request.form.getlist("menu_name[]")
    menu_prices = request.form.getlist("menu_price[]")
    menu_quantities = request.form.getlist("menu_quantity[]")

    restaurant_id = request.form["restaurant_id"]
    restaurant_name = request.form["restaurant_name"]
    user_id = request.form["user_id"]
    user_name = request.form["user_name"]

    order = list(filter(lambda x: x[-1] > 0, map(lambda x: (x[0], float(x[1]), int(x[2])), zip(menu_names, menu_prices, menu_quantities))))
    total = 0 if len(order) == 0 else sum([p*q for n, p, q in order])
    cart = [{"name": n, "price": p * q} for n, p, q in order]

    return render_template("cart.html", restaurant_name=restaurant_name, cart=cart, total=total, user_id=user_id, user_name=user_name)


# endpoint for checkout after adding items to cart
@app.route("/checkout", methods=['POST'])
def checkout():
    menu_names = request.form.getlist("name[]")
    menu_prices = request.form.getlist("price[]")

    restaurant_name = request.form['restaurant_name']
    total = request.form['total']
    user_id = request.form['user_id']
    user_name = request.form['user_name']
    cart = list(map(lambda x: {'name': x[0], 'price': float(x[1])}, zip(menu_names, menu_prices)))
    total = float(total)

    return render_template("checkout.html", restaurant_name=restaurant_name, cart=cart, total=total, user_id=user_id, user_name=user_name)


# endpoint to deliver order
@app.route("/add_active_order", methods=['POST'])
def add_active_order():
    restaurant_name = request.form["restaurant_name"]
    user_name = request.form["user_name"]
    user_id = request.form["user_id"]
    address = request.form["address"]
    mode_of_delivery = request.form["mode_of_delivery"]
    phone_number = request.form["phone_number"]
    total = request.form["total"]

    menu_names = request.form.getlist("item_name[]")
    menu_prices = request.form.getlist("item_price[]")

    if not user_id:
        return redirect("/login_sfsu")

    items = list(map(lambda x: {'name': x[0], 'price': float(x[1])}, zip(menu_names, menu_prices)))
    order = Orders(user_id, user_name, address, phone_number, mode_of_delivery, float(total), items, True, -1, restaurant_name)

    db.session.add(order)
    db.session.commit()
    return render_template("index.html", user_name=user_name, user_id=user_id)


@app.route("/confirm_delivery", methods=['POST'])
def confirm_delivery():
    order_id = request.form["order_id"]
    restaurant_name = request.form["restaurant_name"]
    user_name = request.form["user_name"]
    user_id = request.form["user_id"]
    address = request.form["address"]
    mode = request.form["delivery_mode"]
    driver_id = request.form["driver_id"]
    driver_name = request.form["driver_name"]

    order = Orders.query.filter_by(id=order_id).first()
    order.active = False
    order.driver_id = driver_id
    db.session.commit()

    return render_template("delidriver.html", user_name=user_name, restaurant_name=restaurant_name, address=address, mode=mode, order_id=order_id)


@app.route("/activate_menu", methods=['POST'])
def activate_menu():
    menu_id = request.form["id"]
    menu = Menu.query.filter_by(id=menu_id).first()
    menu.active = True if 'is_active' in request.form else False
    db.session.commit()

    menus = db.session.query(Menu, Restaurant).filter(Menu.restaurant_id == Restaurant.id)
    menus = [{
        'id': m.id,
        'name': m.name,
        'price': m.price,
        'quantity': m.quantity,
        'is_active': m.active,
        'restaurant_name': r.name,
        'cuisine': r.cuisine
    } for (m, r) in menus]
    return render_template("activate_menu.html", menus=menus)


if __name__ == '__main__':
    app.debug = True
    app.run()
