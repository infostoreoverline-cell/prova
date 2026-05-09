from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User, Booking

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('main.register'))
        
        user_email = User.query.filter_by(email=email).first()
        if user_email:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('main.register'))
            
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    
@bp.route('/tavoli')
def tavoli():
    return render_template('tavoli.html')
    
@bp.route('/pulegge')
def pulegge():
    return render_template('pulegge.html')

@bp.route('/cart')
@login_required
def cart():
    # Placeholder for cart
    return render_template('cart.html')

@bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    product_type = request.form.get('product_type')
    
    if product_type == 'table':
        color = request.form.get('color')
        frame = request.form.get('frame')
        density = request.form.get('density')
        details = f"Color: {color}, Frame: {frame}, Density: {density}"
        price = 450.00
        product_name = "Pro Series Table"
    elif product_type == 'pulley':
        size = request.form.get('size')
        details = f"Size: {size}"
        price = 285.00
        product_name = "Pulley System"
    else:
        flash("Invalid product type.", "danger")
        return redirect(url_for('main.home'))
        
    booking = Booking(
        product_name=product_name,
        product_type=product_type,
        details=details,
        price=price,
        user_id=current_user.id
    )
    db.session.add(booking)
    db.session.commit()
    
    flash(f"{product_name} added to your cart!", "success")
    return redirect(url_for('main.cart'))
