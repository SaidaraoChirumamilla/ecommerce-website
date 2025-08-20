from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category, Brand, Product, ProductVariant, ProductReview
from django.contrib.auth import get_user_model
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate database with sample products'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Clothing', 'description': 'Fashion and apparel for everyone'},
            {'name': 'Home & Garden', 'description': 'Everything for your home and garden'},
            {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
            {'name': 'Books', 'description': 'Books and educational materials'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create brands
        brands_data = [
            {'name': 'TechPro', 'description': 'Professional technology solutions'},
            {'name': 'StyleMax', 'description': 'Maximum style for everyone'},
            {'name': 'HomeComfort', 'description': 'Comfort for your home'},
            {'name': 'SportFit', 'description': 'Fitness and sports equipment'},
            {'name': 'BookWorld', 'description': 'World of knowledge'},
            {'name': 'GadgetHub', 'description': 'Hub for all gadgets'},
        ]
        
        brands = {}
        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data['name'],
                defaults={
                    'slug': slugify(brand_data['name']),
                    'description': brand_data['description']
                }
            )
            brands[brand_data['name']] = brand
            if created:
                self.stdout.write(f'Created brand: {brand.name}')
        
        # Create 10 sample products
        products_data = [
            {
                'name': 'Wireless Bluetooth Headphones',
                'brand': 'TechPro',
                'category': 'Electronics',
                'price': Decimal('89.99'),
                'original_price': Decimal('129.99'),
                'discount_percentage': 31,
                'stock_quantity': 50,
                'short_description': 'High-quality wireless headphones with noise cancellation',
                'description': 'Experience premium sound quality with these wireless Bluetooth headphones. Features include active noise cancellation, 30-hour battery life, and comfortable over-ear design.',
                'features': ['Active Noise Cancellation', '30-hour battery', 'Bluetooth 5.0', 'Comfortable fit'],
                'specifications': {'Battery': '30 hours', 'Connectivity': 'Bluetooth 5.0', 'Weight': '250g'},
                'is_featured': True,
                'is_bestseller': True,
                'free_shipping': True,
            },
            {
                'name': 'Premium Cotton T-Shirt',
                'brand': 'StyleMax',
                'category': 'Clothing',
                'price': Decimal('24.99'),
                'original_price': Decimal('34.99'),
                'discount_percentage': 29,
                'stock_quantity': 100,
                'short_description': '100% premium cotton t-shirt in various colors',
                'description': 'Made from 100% premium cotton, this t-shirt offers exceptional comfort and durability. Available in multiple colors and sizes.',
                'features': ['100% Cotton', 'Pre-shrunk', 'Machine washable', 'Various colors'],
                'specifications': {'Material': '100% Cotton', 'Care': 'Machine wash', 'Origin': 'USA'},
                'is_new_arrival': True,
                'free_shipping': False,
            },
            {
                'name': 'Smart LED Desk Lamp',
                'brand': 'HomeComfort',
                'category': 'Home & Garden',
                'price': Decimal('45.99'),
                'stock_quantity': 25,
                'short_description': 'Smart LED desk lamp with app control and multiple lighting modes',
                'description': 'Illuminate your workspace with this smart LED desk lamp. Control brightness, color temperature, and scheduling through the mobile app.',
                'features': ['App Control', 'Multiple lighting modes', 'Touch controls', 'Energy efficient'],
                'specifications': {'Power': '12W', 'Connectivity': 'WiFi', 'Lumens': '800'},
                'is_featured': True,
                'free_shipping': True,
            },
            {
                'name': 'Professional Yoga Mat',
                'brand': 'SportFit',
                'category': 'Sports & Outdoors',
                'price': Decimal('39.99'),
                'original_price': Decimal('59.99'),
                'discount_percentage': 33,
                'stock_quantity': 75,
                'short_description': 'Non-slip professional yoga mat with carrying strap',
                'description': 'Perfect for yoga, pilates, and fitness exercises. Made from eco-friendly materials with superior grip and cushioning.',
                'features': ['Non-slip surface', 'Eco-friendly', '6mm thick', 'Carrying strap included'],
                'specifications': {'Size': '183x61cm', 'Thickness': '6mm', 'Material': 'TPE'},
                'is_bestseller': True,
                'free_shipping': True,
            },
            {
                'name': 'Complete Python Programming Guide',
                'brand': 'BookWorld',
                'category': 'Books',
                'price': Decimal('29.99'),
                'stock_quantity': 200,
                'short_description': 'Comprehensive guide to Python programming for beginners to advanced',
                'description': 'Master Python programming with this comprehensive guide covering everything from basics to advanced topics including web development, data science, and machine learning.',
                'features': ['500+ pages', 'Code examples', 'Exercises', 'Online resources'],
                'specifications': {'Pages': '520', 'Format': 'Paperback', 'Language': 'English'},
                'is_new_arrival': True,
                'free_shipping': True,
            },
            {
                'name': 'Wireless Gaming Mouse',
                'brand': 'GadgetHub',
                'category': 'Electronics',
                'price': Decimal('79.99'),
                'original_price': Decimal('99.99'),
                'discount_percentage': 20,
                'stock_quantity': 40,
                'short_description': 'High-precision wireless gaming mouse with RGB lighting',
                'description': 'Dominate your games with this high-precision wireless gaming mouse. Features customizable RGB lighting, programmable buttons, and ultra-fast response time.',
                'features': ['16000 DPI sensor', 'RGB lighting', '8 programmable buttons', '100-hour battery'],
                'specifications': {'DPI': '16000', 'Buttons': '8', 'Battery': '100 hours'},
                'is_featured': True,
                'free_shipping': True,
            },
            {
                'name': 'Casual Denim Jeans',
                'brand': 'StyleMax',
                'category': 'Clothing',
                'price': Decimal('54.99'),
                'original_price': Decimal('79.99'),
                'discount_percentage': 31,
                'stock_quantity': 80,
                'short_description': 'Classic fit denim jeans in multiple washes',
                'description': 'Timeless denim jeans with a classic fit. Made from premium denim with stretch for comfort. Available in multiple washes and sizes.',
                'features': ['Classic fit', 'Stretch denim', 'Multiple washes', 'Reinforced stitching'],
                'specifications': {'Material': '98% Cotton, 2% Elastane', 'Fit': 'Classic', 'Origin': 'USA'},
                'is_bestseller': True,
                'free_shipping': False,
            },
            {
                'name': 'Smart Home Security Camera',
                'brand': 'TechPro',
                'category': 'Electronics',
                'price': Decimal('149.99'),
                'original_price': Decimal('199.99'),
                'discount_percentage': 25,
                'stock_quantity': 30,
                'short_description': '4K smart security camera with night vision and motion detection',
                'description': 'Keep your home secure with this 4K smart security camera. Features include night vision, motion detection, two-way audio, and cloud storage.',
                'features': ['4K resolution', 'Night vision', 'Motion detection', 'Two-way audio', 'Cloud storage'],
                'specifications': {'Resolution': '4K', 'Storage': 'Cloud/SD', 'Connectivity': 'WiFi'},
                'is_featured': True,
                'free_shipping': True,
            },
            {
                'name': 'Ceramic Plant Pot Set',
                'brand': 'HomeComfort',
                'category': 'Home & Garden',
                'price': Decimal('34.99'),
                'stock_quantity': 60,
                'short_description': 'Set of 3 ceramic plant pots with drainage holes',
                'description': 'Beautiful set of 3 ceramic plant pots perfect for indoor plants. Each pot includes drainage holes and matching saucers.',
                'features': ['Set of 3 pots', 'Drainage holes', 'Matching saucers', 'Various sizes'],
                'specifications': {'Material': 'Ceramic', 'Sizes': 'Small, Medium, Large', 'Color': 'White'},
                'is_new_arrival': True,
                'free_shipping': False,
            },
            {
                'name': 'Resistance Bands Set',
                'brand': 'SportFit',
                'category': 'Sports & Outdoors',
                'price': Decimal('19.99'),
                'original_price': Decimal('29.99'),
                'discount_percentage': 33,
                'stock_quantity': 120,
                'short_description': 'Complete resistance bands set for home workouts',
                'description': 'Complete your home gym with this resistance bands set. Includes 5 bands with different resistance levels, handles, and door anchor.',
                'features': ['5 resistance levels', 'Comfortable handles', 'Door anchor', 'Carrying bag'],
                'specifications': {'Bands': '5', 'Material': 'Natural latex', 'Max resistance': '100lbs'},
                'is_bestseller': True,
                'free_shipping': True,
            },
        ]
        
        # Create products
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slugify(product_data['name']),
                    'brand': brands[product_data['brand']],
                    'category': categories[product_data['category']],
                    'price': product_data['price'],
                    'original_price': product_data.get('original_price'),
                    'discount_percentage': product_data.get('discount_percentage', 0),
                    'stock_quantity': product_data['stock_quantity'],
                    'short_description': product_data['short_description'],
                    'description': product_data['description'],
                    'features': product_data['features'],
                    'specifications': product_data['specifications'],
                    'is_featured': product_data.get('is_featured', False),
                    'is_bestseller': product_data.get('is_bestseller', False),
                    'is_new_arrival': product_data.get('is_new_arrival', False),
                    'free_shipping': product_data.get('free_shipping', False),
                    'sku': f'SKU-{random.randint(10000, 99999)}',
                    'weight': Decimal(str(random.uniform(0.1, 5.0))),
                    'max_order_quantity': 10,
                    'min_stock_level': 5,
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')
                
                # Add some variants for clothing items
                if product.category.name == 'Clothing':
                    sizes = ['S', 'M', 'L', 'XL']
                    colors = ['Black', 'White', 'Blue', 'Red']
                    
                    for size in sizes:
                        ProductVariant.objects.create(
                            product=product,
                            variant_type='Size',
                            name=size,
                            stock_quantity=random.randint(10, 30),
                            sku_suffix=f'-{size}'
                        )
                    
                    for color in colors:
                        ProductVariant.objects.create(
                            product=product,
                            variant_type='Color',
                            name=color,
                            stock_quantity=random.randint(10, 30),
                            sku_suffix=f'-{color[:3].upper()}'
                        )
        
        # Create some sample reviews
        try:
            user = User.objects.first()
            if user:
                products = Product.objects.all()[:5]  # Get first 5 products
                
                sample_reviews = [
                    {'rating': 5, 'title': 'Excellent product!', 'review': 'Really happy with this purchase. Great quality and fast delivery.'},
                    {'rating': 4, 'title': 'Good value', 'review': 'Good product for the price. Would recommend to others.'},
                    {'rating': 5, 'title': 'Love it!', 'review': 'Exactly what I was looking for. Perfect quality and design.'},
                    {'rating': 4, 'title': 'Satisfied', 'review': 'Good product, meets expectations. Delivery was quick.'},
                    {'rating': 5, 'title': 'Outstanding', 'review': 'Outstanding quality and service. Will definitely buy again.'},
                ]
                
                for i, product in enumerate(products):
                    review_data = sample_reviews[i]
                    ProductReview.objects.get_or_create(
                        product=product,
                        user=user,
                        defaults={
                            'rating': review_data['rating'],
                            'title': review_data['title'],
                            'review': review_data['review'],
                            'is_verified_purchase': True
                        }
                    )
        except Exception as e:
            self.stdout.write(f'Note: Could not create sample reviews: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample products!')
        )
