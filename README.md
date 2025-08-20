# 🛍️ E-Commerce Website

A full-featured e-commerce website built with Django and PostgreSQL, featuring user authentication, product catalog, shopping cart, and admin panel.

## ✨ Features

### 🔐 User Authentication
- **Custom User Registration** with comprehensive validation
- **Email-based Login System** with remember me functionality
- **User Profile Management** with personal information
- **Password Strength Requirements** with real-time validation
- **Secure Session Management**

### 🛒 Product Catalog
- **10+ Sample Products** across multiple categories
- **Advanced Product Search** and filtering
- **Category and Brand Management**
- **Product Variants** (sizes, colors, etc.)
- **Stock Management** with low stock warnings
- **Product Reviews and Ratings** (5-star system)
- **Related Products** suggestions

### 🛍️ Shopping Cart
- **Add to Cart** functionality with AJAX
- **Real-time Cart Updates** without page refresh
- **Quantity Management** with stock validation
- **Cart Persistence** across sessions
- **Remove Items** from cart
- **Price Calculations** with discounts

### 👨‍💼 Admin Panel
- **Product Management** with rich admin interface
- **Inventory Tracking** and stock management
- **User Management** with custom user model
- **Order Management** (extensible)
- **Category and Brand Management**
- **Review Moderation**

### 🎨 Modern UI/UX
- **Responsive Design** that works on all devices
- **Modern Bootstrap 5** styling
- **Glassmorphism Effects** on login/signup pages
- **Smooth Animations** and transitions
- **Toast Notifications** for user feedback
- **Professional Product Cards** with hover effects

## 🛠️ Technology Stack

- **Backend:** Django 5.2.5
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Forms:** Django Crispy Forms with Bootstrap 5
- **Authentication:** Custom Django Authentication
- **Image Handling:** Pillow
- **AJAX:** Vanilla JavaScript with Fetch API

## 📋 Requirements

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ecom-website.git
cd ecom-website
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

#### Install PostgreSQL (if not installed)
```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download from https://www.postgresql.org/download/
```

#### Create Database and User
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database and user
CREATE ROLE ecommerce_user WITH LOGIN PASSWORD 'ecommerce_password';
CREATE DATABASE ecommerce_db OWNER ecommerce_user;
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
ALTER ROLE ecommerce_user CREATEDB;
```

### 5. Configure Environment
Update `ecommerce/settings.py` with your database credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Populate Sample Data
```bash
python manage.py populate_products
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the website.

## 📱 Usage

### For Customers:
1. **Browse Products:** Visit the home page and click "Start Shopping"
2. **Search & Filter:** Use the search bar and category filters
3. **View Product Details:** Click on any product for detailed information
4. **Add to Cart:** Select quantity and variants, then add to cart
5. **Manage Cart:** Update quantities or remove items from cart
6. **User Account:** Register/login to save cart and track orders

### For Administrators:
1. **Access Admin Panel:** Visit `/admin/` and login with superuser credentials
2. **Manage Products:** Add, edit, or delete products
3. **Manage Inventory:** Update stock quantities and track low stock
4. **Manage Users:** View and manage customer accounts
5. **Review Management:** Moderate customer reviews

## 🗂️ Project Structure

```
ecom_website/
├── ecommerce/                 # Main project directory
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/                 # User authentication app
│   ├── models.py            # Custom user model
│   ├── forms.py             # Authentication forms
│   ├── views.py             # Authentication views
│   └── admin.py             # User admin configuration
├── products/                 # Product catalog app
│   ├── models.py            # Product, Cart, Review models
│   ├── views.py             # Product and cart views
│   ├── admin.py             # Product admin configuration
│   └── management/          # Custom management commands
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── home.html           # Home page
│   ├── accounts/           # Authentication templates
│   └── products/           # Product templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Key Features Explained

### Custom User Model
- Extended Django's AbstractUser
- Additional fields: phone, address, profile image
- Email-based authentication instead of username

### Product Management
- Comprehensive product model with 20+ fields
- Support for product variants (size, color, etc.)
- Advanced inventory tracking
- SEO-friendly URLs with slugs

### Shopping Cart
- Session-based cart for anonymous users
- Database-stored cart for authenticated users
- Real-time updates with AJAX
- Stock validation on every action

### Security Features
- CSRF protection on all forms
- SQL injection prevention with Django ORM
- XSS protection with template escaping
- Secure password hashing with Django's built-in system

## 🎯 Sample Products

The system comes with 10 pre-loaded products:
1. **Wireless Bluetooth Headphones** - Electronics ($89.99)
2. **Premium Cotton T-Shirt** - Clothing ($24.99)
3. **Smart LED Desk Lamp** - Home & Garden ($45.99)
4. **Professional Yoga Mat** - Sports & Outdoors ($39.99)
5. **Complete Python Programming Guide** - Books ($29.99)
6. **Wireless Gaming Mouse** - Electronics ($79.99)
7. **Casual Denim Jeans** - Clothing ($54.99)
8. **Smart Home Security Camera** - Electronics ($149.99)
9. **Ceramic Plant Pot Set** - Home & Garden ($34.99)
10. **Resistance Bands Set** - Sports & Outdoors ($19.99)

## 🔮 Future Enhancements

- [ ] Order Management System
- [ ] Payment Gateway Integration (Stripe/PayPal)
- [ ] Email Notifications
- [ ] Wishlist Functionality
- [ ] Product Recommendations
- [ ] Multi-vendor Support
- [ ] Mobile App (React Native/Flutter)
- [ ] Advanced Analytics Dashboard
- [ ] Inventory Alerts
- [ ] Coupon/Discount System

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- PostgreSQL Community
- Stack Overflow Community

## 📞 Support

If you have any questions or need help with setup, please open an issue on GitHub or contact the author.

---

⭐ **Star this repository if you found it helpful!**
