from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re


# ========================
# INIT
# ========================

app = Flask(__name__)
app.secret_key = 'sure tastes good'
bcrypt = Bcrypt(app)



# ========================
# CONSTANTS
# ========================

Database = ''
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



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