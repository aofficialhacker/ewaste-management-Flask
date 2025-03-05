# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 06:25:31 2021

@author
"""

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email
import os
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.static_folder = 'FlaskCssFiles'
app.static_url_path = '/static'

# Register a second static folder for Images
from flask import Blueprint
images_bp = Blueprint('images', __name__, static_folder='Images', static_url_path='/static/Images')
app.register_blueprint(images_bp)

# Configure path for HTML files stored in FlaskHtmlFiles
app.config['FLASKHTMLFILES'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FlaskHtmlFiles')
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Configure MongoDB using your Atlas connection string.
# Optionally, you can append a database name (e.g., /ewaste_db) after the host if desired.
app.config["MONGO_URI"] = "mongodb+srv://ayesha:ayesha123@cluster0.4nzbi.mongodb.net/ewaste_db?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Define WTForms for Login and Signup
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

# Routes for pages served from FlaskHtmlFiles folder
@app.route('/aboutus')
@app.route('/aboutus.html')
def aboutus():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'aboutus.html')

@app.route('/faqs')
@app.route('/faq.html')
def faqs():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'faq.html')

@app.route('/productfull')
def productfull():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfull.html')

@app.route('/productfullmobile.html')
def product_mobile():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullmobile.html')

@app.route('/productfullBattery.html')
def product_battery():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullBattery.html')

@app.route('/productfullLedBulb.html')
def product_led_bulb():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullLedBulb.html')

@app.route('/productfullLaptop.html')
def product_laptop():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullLaptop.html')

@app.route('/productfullFridge.html')
def product_fridge():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullFridge.html')

@app.route('/productfullheadphone.html')
def product_headphone():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullheadphone.html')

@app.route('/productfullmotherboard.html')
def product_motherboard():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullmotherboard.html')

@app.route('/productfullCablewire.html')
def product_cablewire():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullCablewire.html')

@app.route('/productfullram.html')
def product_ram():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullram.html')

@app.route('/productfullSmartwatch.html')
def product_smartwatch():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfullSmartwatch.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'contact.html')

@app.route('/sell')
@app.route('/sell.html')
def sell():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'sell.html')

# Routes for pages served from the templates folder
@app.route('/')
def home_public():
    # Public home page using templates/home.html
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Look up the user in the "users" collection
        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            flash("✅ Logged in successfully!", "success")
            return redirect(url_for('home_loggedin'))
        else:
            flash("❌ Incorrect username or password. Please try again.", "error")
            return redirect(url_for('login'))
    # Renders login1.html from the templates folder
    return render_template('login1.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Check if user already exists
        if mongo.db.users.find_one({"username": username}):
            flash("⚠️ Username already exists. Please choose a different one.", "warning")
            return redirect(url_for('signup'))
        # Hash the password and store the user in the "users" collection
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash("✅ Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# Logged-in home page: served from FlaskHtmlFiles folder
@app.route('/loggedin_home')
def home_loggedin():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'home.html')

if __name__ == '__main__':
    app.run(debug=True)
