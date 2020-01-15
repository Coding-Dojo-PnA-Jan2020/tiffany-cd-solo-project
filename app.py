from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import re



# ========================
# INIT
# ========================

app = Flask(__name__)
app.secret_key = 'sure tastes good'
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)



# ========================
# CONSTANTS
# ========================

Database = ''
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



# ========================
# DATABASE
# ========================

class Users(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(255), nullable=False)
  last_name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

recipe_ingredients_table = db.Table('recipe_ingredients',
  db.Column('fk_recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='cascade'), primary_key=True),
  db.Column('fk_ingredient_id', db.Integer, db.ForeignKey('ingredients.ingredient_id_id', ondelete='cascade'), primary_key=True),
  db.Column('quantity', db.Integer, nullable=False),
  db.Column('unit_of_measure', db.String(45), nullable=False),)

class Recipes(db.Model):
  recipe_id = db.Column(db.Integer, primary_key=True)
  rating = db.Column(db.Integer)
  difficulty = db.Column(db.Integer)
  prep_time_mins = db.Column(db.Integer)
  recipe_name = db.Column(db.String(255), nullable=False)
  recipe_description = db.Column(db.String(255))
  author_source = db.Column(db.String(255))
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
  fk_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id') nullable=False)
  user = db.relationship('Users', foreign_keys=[fk_user_id], backref='user_recipes')
  ingredients_in_this_recipe = db.relationship('Ingredients', secondary=recipe_ingredients_table)

class Instructions(db.Model):
  instruction_id = db.Column(db.Integer)
  step_number = db.Column(db.Integer, nullable=False)
  instruction = db.Column(db.String(1000), nullable=False)
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
  fk_recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id') nullable=False)
  recipe = db.relationship('Recipes', foreign_keys=[fk_recipe_id], backref='recipe_instructions')

class Ingredients(db.Model):
  ingredient_id = db.Column(db.Integer)
  ingredient = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
  recipe_using_these_ingredients = db.relationship('Recipes', secondary=recipe_ingredients_table)


# ========================
# GET
# ========================

# 
# 
# INDEX
@app.route('/')
def render_registration_login():
  pass


# 
# 
# DASHBOARD




# 
# 
# RECIPE BOOK




# 
# 
# VIEW/PRINT RECIPE




# 
# 
# MODIFY RECIPE




# 
# 
# VIEW/PRINT RECIPE




# 
# 
# DELETE RECIPE



# 
# 
# MASTER INGREDIENTS LIST




# 
# 
# ACCOUNT SETTINGS




# ========================
# POST
# ========================


# 
# 
# MODIFY RECIPE




# 
# 
# ACCOUNT SETTINGS




# ========================
# SESSION CLEAR
# ========================

# 
# 
# SIGN OUT




if __name__ == "__main__":
  app.run(debug=True)