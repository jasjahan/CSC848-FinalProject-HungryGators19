from models import Restaurant, create_restaurant, delete_restaurant, Menu, create_entry
from flask import Blueprint, request, render_template
from sqlalchemy import or_, and_
from app_old import db
import os


route_app = Blueprint('route_app', __name__)


# endpoint for searching the menu
@route_app.route('/menu', methods=['GET', 'POST'])
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


# endpoint for deleting the entries
@route_app.route('/menu_delete', methods=['POST'])
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


# endpoint for searching restaurants
@route_app.route('/', methods=['GET', 'POST'])
def search_restaurant():
    if request.method == "POST":
        query = request.form['restaurant']
        cuisine = request.form['cuisine']
        if query:
            query = '%{}%'.format(query)
            result = db.session.query(Restaurant).filter(
                and_(
                    Restaurant.cuisine == cuisine,
                    or_(
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
            )
        else:
            result = db.session.query(Restaurant)

        restaurants = [{
            "id": row.id,
            "name": row.name,
            "address": row.address,
            "phone_number": row.phone_number,
            "zip_code": row.zip_code,
            "image": row.image,
            "cuisine": row.cuisine
        } for row in result]

        return render_template('index.html', restaurants=restaurants)
    return render_template('index.html')


# endpoint for adding restaurants
@route_app.route('/add', methods=['GET', 'POST'])
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
    restaurant_cuisine = request.form.get('cuisine')

    restaurant = create_restaurant(restaurant_name, restaurant_address, restaurant_phone,
                                   restaurant_zip, file_path, restaurant_cuisine)
    return render_template('add_restaurant.html', restaurant=restaurant)


# endpoint for deleting restaurants
@route_app.route('/delete', methods=['GET', 'POST'])
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
    # Menu.query.filter_by(name=restaurant_name).delete()
    # db.session.commit()

    restaurant = Restaurant.query.filter_by(name=restaurant_name).first()
    db.session.delete(restaurant)
    db.session.commit()

    file_path = os.path.join(route_app.config['UPLOAD_FOLDER'], restaurant.image)
    if os.path.exists(file_path):
        os.remove(file_path)

    restaurant = Restaurant.query.all()
    return render_template('delete_restaurant.html', restaurant=restaurant)


# endpoint for adding entries
@route_app.route('/add_entry', methods=['GET', 'POST'])
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

