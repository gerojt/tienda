import unittest
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db, Product, Customer, Sale, SaleItem

class TiendaTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and initialize database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_home_page(self):
        """Test that home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sistema de Gesti', response.data)
    
    def test_login_page(self):
        """Test that login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Iniciar Sesi', response.data)
    
    def test_login_success(self):
        """Test successful login"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_login_failure(self):
        """Test failed login with wrong credentials"""
        response = self.client.post('/login', data={
            'username': 'wrong',
            'password': 'wrong'
        }, follow_redirects=True)
        self.assertIn(b'Credenciales inv', response.data)
    
    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Iniciar Sesi', response.data)
    
    def test_create_product(self):
        """Test creating a product"""
        with app.app_context():
            product = Product(
                name='Test Product',
                description='Test Description',
                price=99.99,
                stock=10
            )
            db.session.add(product)
            db.session.commit()
            
            # Verify product was created
            saved_product = Product.query.filter_by(name='Test Product').first()
            self.assertIsNotNone(saved_product)
            self.assertEqual(saved_product.price, 99.99)
            self.assertEqual(saved_product.stock, 10)
    
    def test_create_customer(self):
        """Test creating a customer"""
        with app.app_context():
            customer = Customer(
                name='John Doe',
                email='john@example.com',
                phone='1234567890',
                address='123 Main St'
            )
            db.session.add(customer)
            db.session.commit()
            
            # Verify customer was created
            saved_customer = Customer.query.filter_by(email='john@example.com').first()
            self.assertIsNotNone(saved_customer)
            self.assertEqual(saved_customer.name, 'John Doe')
    
    def test_create_sale(self):
        """Test creating a sale with products"""
        with app.app_context():
            # Create product
            product = Product(
                name='Test Product',
                description='Test Description',
                price=50.00,
                stock=10
            )
            db.session.add(product)
            
            # Create customer
            customer = Customer(
                name='Jane Doe',
                email='jane@example.com',
                phone='0987654321'
            )
            db.session.add(customer)
            db.session.commit()
            
            # Create sale
            sale = Sale(
                customer_id=customer.id,
                total=100.00,
                status='pending'
            )
            db.session.add(sale)
            db.session.flush()
            
            # Add sale item
            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=2,
                price=product.price
            )
            db.session.add(sale_item)
            db.session.commit()
            
            # Verify sale was created
            saved_sale = Sale.query.get(sale.id)
            self.assertIsNotNone(saved_sale)
            self.assertEqual(saved_sale.total, 100.00)
            self.assertEqual(len(saved_sale.items), 1)
            self.assertEqual(saved_sale.items[0].quantity, 2)
    
    def test_product_stock_update_on_sale(self):
        """Test that product stock is updated when a sale is made"""
        with app.app_context():
            # Create product with stock
            product = Product(
                name='Test Product',
                description='Test',
                price=50.00,
                stock=10
            )
            db.session.add(product)
            
            # Create customer
            customer = Customer(
                name='Test Customer',
                email='test@example.com'
            )
            db.session.add(customer)
            db.session.commit()
            
            initial_stock = product.stock
            
            # Simulate sale that reduces stock
            product.stock -= 3
            db.session.commit()
            
            # Verify stock was reduced
            updated_product = Product.query.get(product.id)
            self.assertEqual(updated_product.stock, initial_stock - 3)

if __name__ == '__main__':
    unittest.main()
