from app_old import db
from sqlalchemy import ForeignKey


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
    cuisine = db.Column(db.String(45), nullable=False)

    def __init__(self, name, address, phone_number, zip_code, image, cuisine):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.image = image
        self.cuisine = cuisine


class Menu(db.Model):
    __tablename__ = 'menu'
    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A menu item (entry) has a name, price, and quantity:
    restaurant_id = db.Column(db.Integer, ForeignKey("restaurant.id"), nullable=False)
    name = db.Column(db.String(45))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, name, price, quantity, restaurant_id):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.restaurant_id = restaurant_id


def create_restaurant(new_name, new_address, new_phone, new_zip, new_image, cuisine):
    # Create a restaurant with the provided input.
    # At first, we will trust the user.

    # This line maps to line 18 above (the Restaurant.__init__ method)
    restaurant = Restaurant(new_name, new_address, new_phone, new_zip, new_image, cuisine)

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

    # This line maps to line 18 above (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity, restaurant_id)

    # Actually add this entry to the database
    db.session.add(entry)

    # Save all pending changes to the database
    db.session.commit()

    return entry


def delete_entry(new_name, new_price, new_quantity):
    # Delete an entry with the provided input.
    # At first, we will trust the user.

    # This line maps to line 18 above (the Menu.__init__ method)
    entry = Menu(new_name, new_price, new_quantity)

    # Actually delete this entry from the database
    db.session.delete(entry)

    # Save all pending changes to the database
    db.session.commit()

    return entry


if __name__ == "__main__":
    db.create_all()
