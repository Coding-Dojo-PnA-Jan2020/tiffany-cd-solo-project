from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re


# ========================
# INIT
# ========================

app = Flask(__name__)
app.secret_key = 'mmmm, sure tastes good'
bcrypt = Bcrypt(app)



# ========================
# CONSTANTS
# ========================

database = 'recipe_app'
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



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
  mysql = connectToMySQL(database)
  query = 'SELECT * FROM users WHERE user_ID = %(user_id)s;'
  data = {
    'user_id': session['user_id']
  }
  user = mysql.query_db(query, data)

  return render_template('dashboard.html', user = user)



# 
# 
# ADD RECIPE
@app.route('/add-recipe')
def render_add_recipe():
  return render_template('add-recipe.html')



# 
# 
# RECIPE BOOK
@app.route('/recipe-book')
def render_recipe_book():

  # Recipe List
  mysql = connectToMySQL(database)
  query = 'SELECT * FROM recipes ORDER BY recipe_name;'
  recipe_list = mysql.query_db(query)

  return render_template('recipe-book.html', recipe_book = recipe_list)



# 
# 
# VIEW/PRINT RECIPE
@app.route('/view-recipe/<recipe_id>')
def render_view_recipe(recipe_id):
  mysql = connectToMySQL(database)
  query = 'SELECT * FROM recipe_app.recipes LEFT JOIN recipe_app.instructions ON recipes.recipe_id = instructions.fk_inst_recipe_id LEFT JOIN recipe_app.recipe_ingredients ON recipes.recipe_id = recipe_ingredients.fk_ingr_recipe_id WHERE recipes.recipe_id = %(recipe_id)s;'
  data = {
    'recipe_id': recipe_id
  }
  view_recipe = mysql.query_db(query, data)

  return render_template('view-recipe.html', view_recipe = view_recipe)



# 
# 
# MODIFY RECIPE
@app.route('/modify-recipe/<recipe_id>')
def render_modify_recipe(recipe_id):
  mysql = connectToMySQL(database)
  query = 'SELECT * FROM recipe_app.recipes LEFT JOIN recipe_app.instructions ON recipes.recipe_id = instructions.fk_inst_recipe_id LEFT JOIN recipe_app.recipe_ingredients ON recipes.recipe_id = recipe_ingredients.fk_ingr_recipe_id WHERE recipes.recipe_id = %(recipe_id)s;'
  data = {
    'recipe_id': recipe_id
  }
  modify_recipe = mysql.query_db(query, data)

  return render_template('modify-recipe.html', modify_recipe = modify_recipe)



# 
# 
# DELETE RECIPE
@app.route('/delete/<recipe_id>')
def on_delete(recipe_id):
  mysql = connectToMySQL(database)
  query = 'DELETE FROM recipes WHERE recipe_id = %(recipe_id)s;'
  data = {
    'recipe_id': recipe_id
  }
  mysql.query_db(query, data)
  flash('Recipe successfully deleted!', 'delete_recipe_success')
  return redirect('/recipe-book')



# 
# 
# MASTER INGREDIENTS LIST
@app.route('/ingredients-list')
def render_ingredients():
  mysql = connectToMySQL(database)
  query = 'SELECT * FROM ingredients ORDER BY ingredient;'
  ingredients_list = mysql.query_db(query)

  return render_template('master-ingredients-list.html', ingredients_list = ingredients_list)



# 
# 
# ADD INGREDIENT
@app.route('/add-ingredient')
def render_add_ingredient():
  return render_template('add-ingredient.html')



# 
# 
# ACCOUNT SETTINGS
# Profile
@app.route('/account-settings')
def render_account():
  mysql = connectToMySQL(database)
  query = 'SELECT * FROM users WHERE user_id = %(user_id)s;'
  data = {
    'user_id': session['user_id']
  }
  user_info = mysql.query_db(query, data)

  return render_template('account-settings.html', user_info = user_info[0])



# ========================
# POST
# ========================

# 
# 
# REGISTRATION
@app.route('/register', methods=['POST'])
def on_registration():

  # Validation
  form_is_valid = True

  if len(request.form['first-name']) < 1:
    flash('Please enter your First Name.', 'registration_fail')
    form_is_valid = False
  if len(request.form['last-name']) < 1:
    flash('Please enter your Last Name.', 'registration_fail')
    form_is_valid = False
  if len(request.form['registration-email']) < 5:
    flash('Please enter your Email.', 'registration_fail')
    form_is_valid = False
  if not email_regex.match(request.form['registration-email']):
    flash('Please enter a valid Email.', 'registration_fail')
    form_is_valid = False
  if len(request.form['registration-password']) < 5:
    flash('Password must be at least 5 characters.', 'registration_fail')
    form_is_valid = False
  if request.form['registration-password'] != request.form['confirm-password']:
    flash('Passwords must match.', 'registration_fail')
    form_is_valid = False

  #  form_is_valid / Check Email Against Users Table
  if form_is_valid:
    mysql = connectToMySQL(database)
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {
      'email': request.form['registration-email']
    }
    email_dup_check = mysql.query_db(query, data)

    if email_dup_check:
      flash('This email is already being used.', 'registration_fail')
      return redirect('/')

    # If Not in Database, Add New User
    else:
      bcrypt_password = bcrypt.generate_password_hash(request.form['registration-password'])
      mysql = connectToMySQL(database)
      query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
      data = {
        'first_name': request.form['first-name'],
        'last_name': request.form['last-name'],
        'email': request.form['registration-email'],
        'password': bcrypt_password
      }
      new_user = mysql.query_db(query, data)
      session['user_id'] = new_user
      flash('You have successfully registered!', 'registration_success' )
      return redirect('/dashboard')

  return redirect('/')



# 
# 
# LOGIN
@app.route('/login', methods=['POST'])
def on_login():

  # Validation
  form_is_valid = True

  if not email_regex.match(request.form['login-email']):
    flash('Please enter a valid Email.', 'login_fail')
    form_is_valid = False
  if len(request.form['login-email']) < 1:
    flash('Please enter your Email.', 'login_fail')
    form_is_valid = False
  if len(request.form['login-password']) < 5:
    flash('Please enter your Password.', 'login_fail')
    form_is_valid = False

  # form_is_valid / Check Email Against Users Table
  if form_is_valid:
    mysql = connectToMySQL(database)
    query = 'SELECT * FROM users WHERE email = %(email)s;'
    data = {
      'email': request.form['login-email']
    }

    confirm_user_email = mysql.query_db(query, data)
# flash for if email not in database

    # Check bcrypt Match
    if confirm_user_email:
      if bcrypt.check_password_hash(confirm_user_email[0]['password'], request.form['login-password']):
        session['user_id'] = confirm_user_email[0]['user_id']
        return redirect('/dashboard')
      else:
        flash('Password does not match User Email. You could not be logged in.', 'login_fail')
  return redirect('/')



# 
# 
# ADD RECIPE
@app.route('/add-new-recipe', methods=['POST'])
def on_create_recipe():

  # Validation
  form_is_valid = True

  if len(request.form['recipe-name']) < 1:
    flash('Please enter at least one Ingredient.', 'ingredient_fail')
    form_is_valid = False
  if len(request.form['ingredient']) < 1:
    flash('Please enter at least one Ingredient.', 'ingredient_fail')
    form_is_valid = False
  if len(request.form['instruction']) < 1:
    flash('Please enter at least one Instruction.', 'instruction_fail')
    form_is_valid = False

  #  form_is_valid / Recipe INSERT Query
  if form_is_valid:
    mysql = connectToMySQL(database)
    query = 'INSERT INTO recipes (recipe_name, recipe_description, fk_user_id) VALUES (%(recipe_name)s, %(recipe_description)s, %(fk_user_id)s);'
    data = {
      'recipe_name': request.form['recipe-name'], 
      'recipe_description': request.form['recipe-description'],
      'fk_user_id': session['user_id'],
    }
    recipe_table_result = mysql.query_db(query, data)

    # print(recipe_table_result)

  # Instructions INSERT Query
    instruction_mysql = connectToMySQL(database)
    instruction_query = 'INSERT INTO instructions (step_number, instruction, fk_inst_recipe_id) VALUES (%(step_number)s, %(instruction)s, %(fk_inst_recipe_id)s);'
    instruction_data = {
      'step_number': request.form['step-number'],
      'instruction': request.form['instruction'],
      'fk_inst_recipe_id': recipe_table_result
    }
    instruction_mysql.query_db(instruction_query, instruction_data)

  # Recipe_Ingredients INSERT Query
    recipe_ingredients_mysql = connectToMySQL(database)
    recipe_ingredients_query = 'INSERT INTO recipe_ingredients (quantity, unit_of_measure, recipe_ingredient, fk_ingr_recipe_id) VALUES (%(quantity)s, %(unit_of_measure)s, %(recipe_ingredient)s, %(fk_ingr_recipe_id)s);'
    recipe_ingredients_data = {
      'quantity': request.form['quantity'],
      'unit_of_measure': request.form['unit-of-measure'],
      'recipe_ingredient': request.form['ingredient'],
      'fk_ingr_recipe_id': recipe_table_result
    }
    recipe_ingredients_mysql.query_db(recipe_ingredients_query, recipe_ingredients_data)

    flash('Recipe successfully added!','add_recipe_success' )
  else:
    flash('Recipe could not be added.','add_recipe_fail' )
    return redirect('/add-recipe')

  return redirect('/recipe-book')



  # mysql = connectToMySQL(database)
  # query = 'INSERT'
  # # 'SELECT * FROM recipe_app.recipes LEFT JOIN instructions ON recipes.recipe_id = instructions.fk_recipe_id LEFT JOIN recipes_have_ingredients ON recipes.recipe_id = recipes_have_ingredients.recipe_id LEFT JOIN ingredients ON recipes_have_ingredients.ingredient_id = ingredients.ingredient_id WHERE recipes.recipe_id = %(recipe_id)s;'
  # data = {
  #   # 
  # }



# 
# 
# MODIFY RECIPE
@app.route('/update-recipe/<recipe_id>', methods=['POST'])
def on_modify_recipe(recipe_id):

  mysql = connectToMySQL(database)
  query = 'UPDATE recipes SET recipe_name = %(recipe_name)s, recipe_description = %(recipe_description)s WHERE recipe_id = %(recipe_id)s;'
  data = {
    'recipe_name': request.form['update-recipe-name'], 
    'recipe_description': request.form['update-recipe-description'],
    'recipe_id': recipe_id,
    'fk_user_id': session['user_id'],
  }
  mysql.query_db(query, data)

  # print(recipe_table_result)

# Instructions INSERT Query
  instruction_mysql = connectToMySQL(database)
  instruction_query = 'UPDATE instructions SET step_number = %(step_number)s, instruction = %(instruction)s WHERE fk_inst_recipe_id = %(fk_inst_recipe_id)s;'
  instruction_data = {
    'step_number': request.form['update-step-number'],
    'instruction': request.form['update-instruction'],
    'fk_inst_recipe_id': recipe_id
  }
  instruction_mysql.query_db(instruction_query, instruction_data)

# Recipe_Ingredients INSERT Query
  recipe_ingredients_mysql = connectToMySQL(database)
  recipe_ingredients_query = 'UPDATE recipe_ingredients SET quantity = %(quantity)s, unit_of_measure = %(unit_of_measure)s, recipe_ingredient = %(recipe_ingredient)s WHERE fk_ingr_recipe_id = %(fk_ingr_recipe_id)s;'
  recipe_ingredients_data = {
    'quantity': request.form['update-quantity'],
    'unit_of_measure': request.form['update-unit-of-measure'],
    'recipe_ingredient': request.form['update-recipe-ingredient'],
    'fk_ingr_recipe_id': recipe_id
  }
  recipe_ingredients_mysql.query_db(recipe_ingredients_query, recipe_ingredients_data)
  flash('Your recipe has been successfully updated!', 'update_recipe_success')
  return redirect('/recipe-book')



# 
# 
# ADD INGREDIENT
@app.route('/add-new-ingredient', methods=['POST'])
def on_add_ingredient():

  # Validation
  form_is_valid = True

  if len(request.form['ingredient']) < 1:
    flash('Please enter the ingredient.', 'add_ingredient_fail')
    return redirect('/add-ingredient')
  else:
    mysql = connectToMySQL(database)
    query = 'INSERT INTO ingredients (ingredient) VALUES (%(ingredient)s);'
    data = {
      'ingredient': request.form['ingredient']
    }
    mysql.query_db(query, data)

  flash('Ingredient successfully added', 'add_ingredient_success')
  return redirect('/ingredients-list')



# 
# 
# ACCOUNT SETTINGS - UPDATE PROFILE
@app.route('/update-profile', methods=['POST'])
def on_update_profile():

  # Validation
  form_is_valid = True

  if len(request.form['update-first-name']) < 1:
    flash('Please enter your First Name.', 'update_profile_fail')
    form_is_valid = False
  if len(request.form['update-last-name']) < 1:
    flash('Please enter your Last Name.', 'update_profile_fail')
    form_is_valid = False

  #  form_is_valid / Update Profile Info
  if form_is_valid:
    mysql = connectToMySQL(database)
    query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s WHERE user_id = %(user_id)s;'
    data = {
      'first_name': request.form['update-first-name'],
      'last_name': request.form['update-last-name'],
      'user_id': session['user_id']
    }
    mysql.query_db(query, data)

    flash('Profile Information successfully updated!','update_profile_success' )
  else:
    flash('Profile Information could not be updated.','update_profile_fail' )

  return redirect('/account-settings')



# 
# 
# ACCOUNT SETTINGS - UPDATE LOGIN INFORMATION
@app.route('/update-login', methods=['POST'])
def on_update_login():

  # Validation
  form_is_valid = True

  if len(request.form['update-password']) < 5:
    flash('Password must be at least 5 characters.', 'update_login_fail')
    form_is_valid = False
  if request.form['update-password'] != request.form['confirm-update-password']:
    flash('Passwords must match.', 'update_login_fail')
    form_is_valid = False

  #  form_is_valid / Update Login Information
  if form_is_valid:
      bcrypt_password = bcrypt.generate_password_hash(request.form['update-password'])
      mysql = connectToMySQL(database)
      query = 'UPDATE users SET password = %(password)s WHERE user_id = %(user_id)s;'
      data = {
        'password': bcrypt_password,
        'user_id': session['user_id']
      }
      mysql.query_db(query, data)

      flash('Login Information successfully updated!', 'update_login_success' )
      return redirect('/account-settings')

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