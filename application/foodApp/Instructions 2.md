# Progress

# 3/27/2021:
# Successfully implemented search, add, and delete restaurant in the "restaurant" table in the database HungryGators-19.

# Currently working on adding entries to the "menu" table without too much hardcoding in database. Then planning on to 
# work on deleting entries from the menu table, then finally try to search by entry items in the search bar for 
# searching restaurants.

# Then planning on working on calculating entry totals if a customer wants to order entries from a certain restaurant 
# and assign it to a delivery driver.

# To connect from backend to database, use:
# app.config['SQLALCHEMY_DATABASE_URI'] = mysql://username:password@server/db
# where username is the username to your database, password is the password to your database, server is the server of 
# your database, and db = HungryGators-19

# See https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/

# 3/29/2021:
# Backend now able to add and delete entries from menu for each of respective restaurants added to the database.
# It appears that we may need to implement a login/logout page to distinguish user and restaurant owner and admin 
# because only restaurant owners and admin can delete entries listed from the database, but this M2 VP does not require 
# login/logout...