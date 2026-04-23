from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///affiliate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

PRODUCTS_PER_PAGE = 20

CATEGORIES = [
    'Electronics', 'Home & Kitchen', 'Fashion', 'Books',
    'Health & Beauty', 'Toys & Games', 'Sports', 'Automotive', 'Other'
]

# ── Models ────────────────────────────────────────────────────────────────────

class Admin(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False)
    description    = db.Column(db.Text, nullable=False)
    image_url      = db.Column(db.String(500), nullable=False)
    affiliate_link = db.Column(db.String(500), nullable=False)
    price          = db.Column(db.Float, nullable=True, default=0.0)
    rating         = db.Column(db.Float, nullable=True, default=0.0)   # 0.0 – 5.0
    category       = db.Column(db.String(100), nullable=True, default='Other')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'affiliate_link': self.affiliate_link,
            'price': self.price,
            'rating': self.rating,
            'category': self.category,
        }

# ── Auth helpers ──────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ── Public routes ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    page     = request.args.get('page', 1, type=int)
    query    = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()

    qry = Product.query

    # ── Category filter — exact match ─────────────────────────────────────────
    if category and category != 'All':
        qry = qry.filter(Product.category == category)

    # ── Search filter — only on name and description, NOT category ────────────
    if query:
        like = f'%{query}%'
        qry = qry.filter(
            db.or_(
                Product.name.ilike(like),
                Product.description.ilike(like)
            )
        )

    total    = qry.count()
    pages    = math.ceil(total / PRODUCTS_PER_PAGE) or 1
    page     = max(1, min(page, pages))
    products = qry.order_by(Product.id.desc()) \
                  .offset((page - 1) * PRODUCTS_PER_PAGE) \
                  .limit(PRODUCTS_PER_PAGE) \
                  .all()

    return render_template('index.html',
                           products=products,
                           page=page,
                           pages=pages,
                           total=total,
                           query=query,
                           active_category=category,
                           categories=CATEGORIES)


@app.route('/product/<int:product_id>')
def product(product_id):
    p = Product.query.get_or_404(product_id)
    return render_template('product.html', product=p)


# ── Auth routes ───────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin    = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['admin_id'] = admin.id
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/admin/logout')
def logout():
    session.pop('admin_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ── Admin dashboard ───────────────────────────────────────────────────────────

@app.route('/admin/dashboard')
@login_required
def dashboard():
    q   = request.args.get('q', '').strip()
    qry = Product.query
    if q:
        like = f'%{q}%'
        qry = qry.filter(
            db.or_(Product.name.ilike(like), Product.category.ilike(like))
        )
    products = qry.order_by(Product.id.desc()).all()
    return render_template('dashboard.html', products=products, categories=CATEGORIES, q=q)


@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name           = request.form.get('name', '').strip()
        description    = request.form.get('description', '').strip()
        image_url      = request.form.get('image_url', '').strip()
        affiliate_link = request.form.get('affiliate_link', '').strip()
        category       = request.form.get('category', 'Other').strip()
        try:
            price  = float(request.form.get('price', 0) or 0)
            rating = float(request.form.get('rating', 0) or 0)
            rating = max(0.0, min(5.0, rating))
        except ValueError:
            price = 0.0
            rating = 0.0

        if not all([name, description, image_url, affiliate_link]):
            flash('Name, description, image URL and affiliate link are required.', 'danger')
            return render_template('product_form.html', action='Add', product=None, categories=CATEGORIES)

        p = Product(name=name, description=description, image_url=image_url,
                    affiliate_link=affiliate_link, price=price,
                    rating=rating, category=category)
        db.session.add(p)
        db.session.commit()
        flash(f'"{name}" added successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('product_form.html', action='Add', product=None, categories=CATEGORIES)


@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        p.name           = request.form.get('name', '').strip()
        p.description    = request.form.get('description', '').strip()
        p.image_url      = request.form.get('image_url', '').strip()
        p.affiliate_link = request.form.get('affiliate_link', '').strip()
        p.category       = request.form.get('category', 'Other').strip()
        try:
            p.price  = float(request.form.get('price', 0) or 0)
            p.rating = float(request.form.get('rating', 0) or 0)
            p.rating = max(0.0, min(5.0, p.rating))
        except ValueError:
            p.price  = 0.0
            p.rating = 0.0

        if not all([p.name, p.description, p.image_url, p.affiliate_link]):
            flash('Name, description, image URL and affiliate link are required.', 'danger')
            return render_template('product_form.html', action='Edit', product=p, categories=CATEGORIES)

        db.session.commit()
        flash(f'"{p.name}" updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('product_form.html', action='Edit', product=p, categories=CATEGORIES)


@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    name = p.name
    db.session.delete(p)
    db.session.commit()
    flash(f'"{name}" deleted.', 'info')
    return redirect(url_for('dashboard'))


# ── Jinja helpers ─────────────────────────────────────────────────────────────

@app.template_filter('stars')
def stars_filter(rating):
    """Return list of star types: 'full', 'half', 'empty' for a 0-5 rating."""
    stars = []
    r = float(rating or 0)
    for i in range(5):
        if r >= i + 1:
            stars.append('full')
        elif r >= i + 0.5:
            stars.append('half')
        else:
            stars.append('empty')
    return stars


@app.template_filter('inr')
def inr_filter(value):
    """Format a number as ₹1,299"""
    try:
        v = float(value)
        if v == 0:
            return 'Price not set'
        return f'₹{v:,.0f}'
    except Exception:
        return 'N/A'


# ── DB init ───────────────────────────────────────────────────────────────────

def init_db():
    with app.app_context():
        db.create_all()
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('✅  Default admin created  →  username: admin | password: admin123')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
