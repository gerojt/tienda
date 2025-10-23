from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Customer {self.name}>'

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    customer = db.relationship('Customer', backref='sales')
    items = db.relationship('SaleItem', backref='sale', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Sale {self.id}>'

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<SaleItem {self.id}>'

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Por favor inicia sesión para acceder.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Simple authentication (in production, use proper password hashing)
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['username'] = username
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    total_products = Product.query.count()
    total_customers = Customer.query.count()
    total_sales = Sale.query.count()
    total_revenue = db.session.query(db.func.sum(Sale.total)).scalar() or 0
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_products=total_products,
                         total_customers=total_customers,
                         total_sales=total_sales,
                         total_revenue=total_revenue,
                         recent_sales=recent_sales)

# Product Routes
@app.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        
        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        
        flash('Producto agregado exitosamente!', 'success')
        return redirect(url_for('products'))
    
    return render_template('product_form.html', product=None)

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        
        db.session.commit()
        
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('products'))
    
    return render_template('product_form.html', product=product)

@app.route('/products/delete/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('products'))

# Customer Routes
@app.route('/customers')
@login_required
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        customer = Customer(name=name, email=email, phone=phone, address=address)
        db.session.add(customer)
        db.session.commit()
        
        flash('Cliente agregado exitosamente!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('customer_form.html', customer=None)

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        
        db.session.commit()
        
        flash('Cliente actualizado exitosamente!', 'success')
        return redirect(url_for('customers'))
    
    return render_template('customer_form.html', customer=customer)

@app.route('/customers/delete/<int:id>')
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    
    flash('Cliente eliminado exitosamente!', 'success')
    return redirect(url_for('customers'))

# Sales Routes
@app.route('/sales')
@login_required
def sales():
    sales = Sale.query.order_by(Sale.created_at.desc()).all()
    return render_template('sales.html', sales=sales)

@app.route('/sales/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    if request.method == 'POST':
        customer_id = int(request.form.get('customer_id'))
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        
        # Create sale
        sale = Sale(customer_id=customer_id, total=0)
        db.session.add(sale)
        db.session.flush()
        
        total = 0
        for product_id, quantity in zip(product_ids, quantities):
            if product_id and quantity:
                product = Product.query.get(int(product_id))
                qty = int(quantity)
                
                if product.stock >= qty:
                    # Add sale item
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        product_id=product.id,
                        quantity=qty,
                        price=product.price
                    )
                    db.session.add(sale_item)
                    
                    # Update stock
                    product.stock -= qty
                    
                    total += product.price * qty
                else:
                    flash(f'Stock insuficiente para {product.name}', 'danger')
                    db.session.rollback()
                    products = Product.query.filter(Product.stock > 0).all()
                    customers = Customer.query.all()
                    return render_template('sale_form.html', products=products, customers=customers)
        
        sale.total = total
        db.session.commit()
        
        flash('Venta registrada exitosamente!', 'success')
        return redirect(url_for('sales'))
    
    products = Product.query.filter(Product.stock > 0).all()
    customers = Customer.query.all()
    return render_template('sale_form.html', products=products, customers=customers)

@app.route('/sales/view/<int:id>')
@login_required
def view_sale(id):
    sale = Sale.query.get_or_404(id)
    return render_template('sale_detail.html', sale=sale)

@app.route('/sales/delete/<int:id>')
@login_required
def delete_sale(id):
    sale = Sale.query.get_or_404(id)
    
    # Restore stock
    for item in sale.items:
        product = Product.query.get(item.product_id)
        product.stock += item.quantity
    
    db.session.delete(sale)
    db.session.commit()
    
    flash('Venta eliminada exitosamente!', 'success')
    return redirect(url_for('sales'))

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print('Database initialized!')

if __name__ == '__main__':
    init_db()
    # Debug mode disabled for security - enable only in development
    app.run(debug=False)
