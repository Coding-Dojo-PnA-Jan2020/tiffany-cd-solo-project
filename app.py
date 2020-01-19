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
  profile_image_link = db.Column(db.String(255))
  first_name = db.Column(db.String(255), nullable=False)
  last_name = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

recipe_ingredients_table = db.Table('recipe_ingredients',
  db.Column('fk_recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='cascade'), primary_key=True),
  db.Column('fk_ingredient_id', db.Integer, db.ForeignKey('ingredients.ingredient_id', ondelete='cascade'), primary_key=True),
  db.Column('quantity', db.Integer, nullable=False),
  db.Column('unit_of_measure', db.String(45), nullable=False),)

class Recipes(db.Model):
  recipe_id = db.Column(db.Integer, primary_key=True)
  recipe_image_link = db.Column(db.String(255))
  rating = db.Column(db.Integer)
  difficulty = db.Column(db.Integer)
  prep_time_mins = db.Column(db.Integer)
  recipe_name = db.Column(db.String(255), nullable=False)
  recipe_description = db.Column(db.String(255))
  author_source = db.Column(db.String(255))
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
  fk_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
  user = db.relationship('Users', foreign_keys=[fk_user_id], backref='user_recipes')
  ingredients_in_this_recipe = db.relationship('Ingredients', secondary=recipe_ingredients_table)

class Instructions(db.Model):
  instruction_id = db.Column(db.Integer, primary_key=True)
  step_number = db.Column(db.Integer, nullable=False)
  instruction = db.Column(db.String(1000), nullable=False)
  created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
  updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
  fk_recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
  recipe = db.relationship('Recipes', foreign_keys=[fk_recipe_id], backref='recipe_instructions')

class Ingredients(db.Model):
  ingredient_id = db.Column(db.Integer, primary_key=True)
  ingredient_image_link = db.Column(db.String(255))
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
  return render_template('registration-login.html')



# 
# 
# DASHBOARD
@app.route('/dashboard')
def render_dashboard():
  # User Session
  if'user_id' not in session:
    return redirect('/')
  
  all_registered_users = Users.query.all()
  # Database Query (Read)
  return render_template('dashboard.html', all_registered_users = all_registered_users)



# 
# 
# RECIPE BOOK
@app.route('/recipe-book')
def render_recipe_book():
  # Database Query (Read)
  return render_template('recipe-book.html')


# 
# 
# MODIFY RECIPE
@app.route('/recipe-book')
def render_modify_recipe():
  # Database Query (Read)
  return render_template('modify_recipe.html')



# 
# 
# VIEW/PRINT RECIPE
@app.route('/recipe-book')
def render_view_recipe():
  # Database Query (Read)
  return render_template('view_recipe.html')



# 
# 
# DELETE RECIPE
@app.route('/delete/<recipe_id>')
def on_delete():
  # Database Query (Delete)
  return redirect('/recipe-book')

# 
# 
# MASTER INGREDIENTS LIST
@app.route('/ingredients-list')
def render_ingredients():
  # Database Query
  return render_template('ingredients-list.html')



# 
# 
# ACCOUNT SETTINGS
# Profile
@app.route('/account-settings')
def render_account():
  # Database Query
  return render_template('account-settings.html')



# ========================
# POST
# ========================

# 
# 
# REGISTRATION
@app.route('/register', methods=['POST'])
def on_registration():
  form_is_valid = True

  # Validation
  if len(request.form['first_name']) < 1:
    flash('Please enter your First Name.', 'registration_fail')
    form_is_valid = False
  if len(request.form['last_name']) < 1:
    flash('Please enter your Last Name.', 'registration_fail')
    form_is_valid = False
  if len(request.form['registration_email']) < 5:
    flash('Please enter your Email.', 'registration_fail')
    form_is_valid = False
  if not email_regex.match(request.form['registration_email']):
    flash('Please enter a valid Email.', 'registration_fail')
    form_is_valid = False
  if (request.form['registration_password'] < 5):
    flash('Password must be at least 5 characters.', 'registration_fail')
    form_is_valid = False
  if request.form['registration_password'] != request.form['confirm_password']:
    flash('Passwords must match.', 'registration_fail')
    form_is_valid = False

  #  form_is_valid / Post Data
  if form_is_valid:

    return redirect('/')

# 
# 
# LOGIN
@app.route('/login', methods=['POST'])
def on_login():
  # Database Query (Read)

  # Validation
  form_is_valid = True

  if not email_regex.match(request.form['login_email']):
    flash('Please enter a valid Email.', 'login_fail')
    form_is_valid = False
  if len(request.form['login_email']) < 1:
    flash('Please enter your Email.', 'login_fail')
    form_is_valid = False
  if len(request.form['login_password']) < 1:
    flash('Please enter your Password.', 'login_fail')
    form_is_valid = False

  # Check bcrypt match


  return redirect('/')

# 
# 
# MODIFY RECIPE
@app.route('/modify-recipe', methods=['POST'])
def on_modify_recipe():

  # Validation
  form_is_valid = True

  if len(request.form['instruction']) < 1:
    flash('Please enter at least one Instruction.', 'instruction_fail')
  # Database Query (Update)

  return redirect('/recipe-book')



# 
# 
# ACCOUNT SETTINGS
# Profile
@app.route('/update-profile', methods=['POST'])
def on_update_profile():
  # Database Query (Update)

  return redirect('/account-settings')

# Login Information
@app.route('/update-login', methods=['POST'])
def on_update_login():
  # Database Query (Update)

  return redirect('/account-settings')


# ========================
# SESSION CLEAR
# ========================

# 
# 
# SIGN OUT
@app.route('/logout')
def on_logout():
  session.clear()
  return redirect('/')




if __name__ == "__main__":
  app.run(debug=True)