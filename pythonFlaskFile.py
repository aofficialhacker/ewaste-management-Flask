# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 06:25:31 2021

@author
"""

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
import os
import uuid
from datetime import datetime
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId

app = Flask(__name__)
app.static_folder = 'FlaskCssFiles'
app.static_url_path = '/static'

# Register a second static folder for Images
from flask import Blueprint
images_bp = Blueprint('images', __name__, static_folder='Images', static_url_path='/static/Images')
app.register_blueprint(images_bp)

# Register uploads folder for serving uploaded files
uploads_bp = Blueprint('uploads', __name__, static_folder='uploads', static_url_path='/uploads')
app.register_blueprint(uploads_bp)

# Configure path for HTML files stored in FlaskHtmlFiles
app.config['FLASKHTMLFILES'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'FlaskHtmlFiles')
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max upload size
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

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
    phone = StringField('Phone Number', validators=[DataRequired()])
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
    # Check if an ID was provided in the query parameters
    item_id = request.args.get('id')
    
    if item_id:
        # Fetch the item details from MongoDB
        try:
            item = mongo.db.listings.find_one({"_id": item_id})
        except:
            # If the ID is not a valid ObjectId, try as string
            from bson.objectid import ObjectId
            try:
                item = mongo.db.listings.find_one({"_id": ObjectId(item_id)})
            except:
                item = None
        
        if item:
            # Convert ObjectId to string for template
            item['_id'] = str(item['_id'])
            # Make sure user_id is a string for template
            if 'user_id' in item and isinstance(item['user_id'], ObjectId):
                item['user_id'] = str(item['user_id'])
            return render_template('productfull.html', item=item)
    
    # If no ID provided or item not found, return the default template
    return send_from_directory(app.config['FLASKHTMLFILES'], 'productfull.html')

@app.route('/productfullmobile.html')
def product_mobile():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Smartphone',
        'brand': 'Samsung',
        'description': 'Used smartphone in good condition. Minor scratches on the screen but fully functional.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['mobile.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullBattery.html')
def product_battery():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Rechargeable Battery Pack',
        'brand': 'Generic',
        'description': 'Used rechargeable battery pack in working condition. Holds charge well.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['battery.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullLedBulb.html')
def product_led_bulb():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'LED Bulb',
        'brand': 'Philips',
        'description': 'Used LED bulb in working condition. Energy efficient and bright.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['bulb.jpeg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullLaptop.html')
def product_laptop():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Lenovo ThinkPad X1 Carbon - 14" Ultrabook',
        'brand': 'Lenovo',
        'description': 'Used ThinkPad laptop in excellent condition. Intel Core i7 processor, 16GB RAM, 512GB SSD.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['dell.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullFridge.html')
def product_fridge():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Refrigerator',
        'brand': 'Samsung',
        'description': 'Used refrigerator in good working condition. Energy efficient with freezer compartment.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['frige.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullheadphone.html')
def product_headphone():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Wireless Headphones',
        'brand': 'Sony',
        'description': 'Wireless headphones with noise cancellation. Good battery life and sound quality.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['headphone.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullmotherboard.html')
def product_motherboard():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Intel Z590 ATX Motherboard',
        'brand': 'Intel',
        'description': 'This motherboard is in working condition with all ports functional. Supports 10th and 11th Gen Intel processors. Includes I/O shield and original packaging.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['motherboard.jpeg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullCablewire.html')
def product_cablewire():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Cable Wire',
        'brand': 'Generic',
        'description': 'Used cable wire in good condition. Various lengths available.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['wire.jpeg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullram.html')
def product_ram():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'SSD RAM',
        'brand': 'Kingston',
        'description': 'High-performance RAM module with fast read/write speeds.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['ram.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/productfullSmartwatch.html')
def product_smartwatch():
    # Create a dummy item for the template
    item = {
        '_id': 'dummy_id',
        'user_id': 'seller_id',
        'product_type': 'Smartwatch',
        'brand': 'Apple',
        'description': 'Used smartwatch in excellent condition. All features working properly.',
        'created_at': datetime.now(),
        'status': 'available',
        'images': ['watch.jpg']
    }
    # Render the template with session and item variables
    return render_template('productfull.html', item=item)

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'contact.html')

@app.route('/sell')
@app.route('/sell.html')
def sell():
    return send_from_directory(app.config['FLASKHTMLFILES'], 'sell.html')

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/sell', methods=['POST'])
def api_sell():
    if 'user_id' not in request.form:
        # In a real app, you would get this from the session
        user_id = 'anonymous_user'  
    else:
        user_id = request.form['user_id']
    
    product_type = request.form.get('product_type')
    brand = request.form.get('brand')
    description = request.form.get('description')
    
    # Validate required fields
    if not product_type or not brand or not description:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    # Process uploaded files
    uploaded_files = []
    for key in request.files:
        file = request.files[key]
        
        if file and allowed_file(file.filename):
            # Generate a secure filename with UUID to avoid duplicates
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Add to uploaded files list
            uploaded_files.append(unique_filename)
    
    if not uploaded_files:
        return jsonify({'success': False, 'message': 'No valid images uploaded'})
    
    # Create a new listing document
    listing = {
        'user_id': user_id,
        'product_type': product_type,
        'brand': brand,
        'description': description,
        'images': uploaded_files,
        'created_at': datetime.now(),
        'status': 'pending'  # pending, approved, sold, etc.
    }
    
    # Save to MongoDB
    result = mongo.db.listings.insert_one(listing)
    
    if result.inserted_id:
        return jsonify({
            'success': True, 
            'message': 'Listing created successfully',
            'listing_id': str(result.inserted_id)
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to create listing'})

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
            # Store user information in session
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
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
        # Get phone number from form
        phone = form.phone.data
        # Hash the password and store the user in the "users" collection
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "phone": phone,
            "password": hashed_password
        })
        flash("✅ Signup successful! Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# Logged-in home page: served from templates folder with recent listings
@app.route('/loggedin_home')
def home_loggedin():
    # Fetch the most recent listings from the database
    recent_listings = list(mongo.db.listings.find().sort('created_at', -1).limit(6))
    
    # Convert ObjectId to string for each listing
    for listing in recent_listings:
        listing['_id'] = str(listing['_id'])
    
    return render_template('loggedin_home.html', recent_listings=recent_listings)

# Route for recently posted items page
@app.route('/recent_items')
def recent_items():
    # Fetch all recent listings from the database
    recent_listings = list(mongo.db.listings.find().sort('created_at', -1).limit(20))
    
    # Convert ObjectId to string for each listing
    for listing in recent_listings:
        listing['_id'] = str(listing['_id'])
    
    # Check if an ID was provided in the query parameters
    item_id = request.args.get('id')
    selected_item = None
    
    if item_id:
        # Find the selected item in the recent_listings
        for item in recent_listings:
            if item['_id'] == item_id:
                selected_item = item
                break
        
        # If not found in recent_listings, try to fetch from database
        if not selected_item:
            try:
                from bson.objectid import ObjectId
                item = mongo.db.listings.find_one({"_id": ObjectId(item_id)})
                if item:
                    item['_id'] = str(item['_id'])
                    selected_item = item
            except:
                selected_item = None
    
    return render_template('recent_items.html', recent_listings=recent_listings, selected_item=selected_item)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash("✅ Logged out successfully!", "success")
    return redirect(url_for('home_public'))

# Chat functionality
@app.route('/chat/<item_id>/<seller_id>', methods=['GET'])
def chat(item_id, seller_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash("❌ Please log in to chat with sellers.", "error")
        return redirect(url_for('login'))
    
    current_user_id = session['user_id']
    
    # Don't allow users to chat with themselves
    if current_user_id == seller_id:
        flash("❌ You cannot chat with yourself.", "error")
        return redirect(url_for('home_loggedin'))
    
    # Get item details
    try:
        # Try to convert item_id to ObjectId if it's not already
        if not isinstance(item_id, ObjectId):
            try:
                item_id_obj = ObjectId(item_id)
            except:
                item_id_obj = item_id
        else:
            item_id_obj = item_id
            
        item = mongo.db.listings.find_one({"_id": item_id_obj})
    except Exception as e:
        print(f"Error finding item: {e}")
        item = None
    
    if not item:
        flash("❌ Item not found.", "error")
        return redirect(url_for('home_loggedin'))
    
    # Convert ObjectId to string for template
    item['_id'] = str(item['_id'])
    
    # Get seller details
    try:
        # Try to convert seller_id to ObjectId if it's not already
        if not isinstance(seller_id, ObjectId):
            try:
                seller_id_obj = ObjectId(seller_id)
            except:
                seller_id_obj = seller_id
        else:
            seller_id_obj = seller_id
            
        seller = mongo.db.users.find_one({"_id": seller_id_obj})
    except Exception as e:
        print(f"Error finding seller: {e}")
        seller = None
        
    if not seller:
        flash("❌ Seller not found.", "error")
        return redirect(url_for('home_loggedin'))
    
    # Find existing conversation or create a new one
    conversation = mongo.db.conversations.find_one({
        "item_id": item_id,
        "participants": {"$all": [current_user_id, seller_id]}
    })
    
    if not conversation:
        # Create a new conversation
        conversation_id = mongo.db.conversations.insert_one({
            "item_id": item_id,
            "participants": [current_user_id, seller_id],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }).inserted_id
        conversation_id = str(conversation_id)
        messages = []
    else:
        # Get existing conversation
        conversation_id = str(conversation["_id"])
        # Get messages for this conversation
        messages = list(mongo.db.messages.find({"conversation_id": conversation_id}).sort("timestamp", 1))
    
    # Get seller's phone number
    seller_phone = seller.get('phone', 'Not provided')
    
    return render_template('chat.html', 
                          item=item, 
                          seller_id=seller_id,
                          seller_username=seller['username'],
                          seller_phone=seller_phone,
                          current_user_id=current_user_id,
                          conversation_id=conversation_id,
                          messages=messages)

@app.route('/send_message/<conversation_id>', methods=['POST'])
def send_message(conversation_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash("❌ Please log in to send messages.", "error")
        return redirect(url_for('login'))
    
    current_user_id = session['user_id']
    message_content = request.form.get('message')
    
    if not message_content:
        flash("❌ Message cannot be empty.", "error")
        
        # Get conversation details to extract item_id and seller_id
        try:
            conversation = mongo.db.conversations.find_one({"_id": ObjectId(conversation_id)})
            if conversation:
                item_id = conversation['item_id']
                # Get the other participant (receiver)
                receiver_id = next(p for p in conversation['participants'] if p != current_user_id)
                return redirect(url_for('chat', item_id=item_id, seller_id=receiver_id))
        except:
            pass
            
        # If we couldn't get the conversation details, redirect to home
        return redirect(url_for('home_loggedin'))
    
    # Get conversation details
    try:
        conversation = mongo.db.conversations.find_one({"_id": ObjectId(conversation_id)})
    except:
        flash("❌ Conversation not found.", "error")
        return redirect(url_for('home_loggedin'))
    
    if not conversation:
        flash("❌ Conversation not found.", "error")
        return redirect(url_for('home_loggedin'))
    
    # Verify user is part of this conversation
    if current_user_id not in conversation['participants']:
        flash("❌ You are not authorized to send messages in this conversation.", "error")
        return redirect(url_for('home_loggedin'))
    
    # Get the other participant (receiver)
    receiver_id = next(p for p in conversation['participants'] if p != current_user_id)
    
    # Save the message
    mongo.db.messages.insert_one({
        "conversation_id": conversation_id,
        "sender_id": current_user_id,
        "receiver_id": receiver_id,
        "content": message_content,
        "timestamp": datetime.now(),
        "read": False
    })
    
    # Update conversation's updated_at timestamp
    mongo.db.conversations.update_one(
        {"_id": ObjectId(conversation_id)},
        {"$set": {"updated_at": datetime.now()}}
    )
    
    # Redirect back to the chat
    return redirect(url_for('chat', item_id=conversation['item_id'], seller_id=receiver_id))

@app.route('/my_conversations')
def my_conversations():
    # Check if user is logged in
    if 'user_id' not in session:
        flash("❌ Please log in to view your conversations.", "error")
        return redirect(url_for('login'))
    
    current_user_id = session['user_id']
    
    # Get all conversations for the current user
    conversations = list(mongo.db.conversations.find({
        "participants": current_user_id
    }).sort("updated_at", -1))
    
    # Get details for each conversation
    conversation_details = []
    for conv in conversations:
        # Get the other participant
        other_participant_id = next(p for p in conv['participants'] if p != current_user_id)
        other_user = mongo.db.users.find_one({"_id": ObjectId(other_participant_id)})
        
        # Get the item
        item = mongo.db.listings.find_one({"_id": ObjectId(conv['item_id'])})
        
        # Get the last message
        last_message = mongo.db.messages.find_one(
            {"conversation_id": str(conv["_id"])},
            sort=[('timestamp', -1)]
        )
        
        # Count unread messages
        unread_count = mongo.db.messages.count_documents({
            "conversation_id": str(conv["_id"]),
            "receiver_id": current_user_id,
            "read": False
        })
        
        conversation_details.append({
            "id": str(conv["_id"]),
            "item": item,
            "other_user": other_user,
            "last_message": last_message,
            "unread_count": unread_count,
            "updated_at": conv["updated_at"]
        })
    
    return render_template('conversations.html', conversations=conversation_details)

if __name__ == '__main__':
    app.run(debug=True)
