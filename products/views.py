from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    Product, Category, Brand, Cart, CartItem, Wishlist, WishlistItem,
    ProductReview, ProductVariant
)

def product_list(request):
    """Product catalog page with filtering and search"""
    products = Product.objects.filter(is_active=True).select_related('brand', 'category')
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    # Sort options
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    """Detailed product page with all Amazon-like features"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get product images
    images = product.images.all().order_by('order', 'created_at')
    
    # Get product variants
    variants = product.variants.filter(is_active=True)
    
    # Get reviews
    reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')[:10]
    
    # Related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:6]
    
    context = {
        'product': product,
        'images': images,
        'variants': variants,
        'reviews': reviews,
        'related_products': related_products,
    }
    
    return render(request, 'products/product_detail.html', context)

@login_required
@require_POST
def add_to_cart(request):
    """Add product to cart via AJAX"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Check stock
        if product.stock_quantity < quantity:
            return JsonResponse({
                'success': False,
                'message': f'Only {product.stock_quantity} items available.'
            })
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart!',
            'cart_total_items': cart.total_items,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })

@login_required
@require_POST
def update_cart_quantity(request):
    """Update cart item quantity via AJAX"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        # Check stock
        available_stock = cart_item.variant.stock_quantity if cart_item.variant else cart_item.product.stock_quantity
        if available_stock < quantity:
            return JsonResponse({
                'success': False,
                'message': f'Only {available_stock} items available in stock.'
            })
        
        # Check max order quantity
        if quantity > cart_item.product.max_order_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Maximum order quantity is {cart_item.product.max_order_quantity}.'
            })
        
        if quantity <= 0:
            cart_item.delete()
            message = 'Item removed from cart.'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Cart updated successfully!'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total_items': cart.total_items,
            'cart_total_price': str(cart.total_price),
            'item_total_price': str(cart_item.total_price) if quantity > 0 else '0.00'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })

@login_required
@require_POST
def remove_from_cart(request):
    """Remove item from cart via AJAX"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart successfully!',
            'cart_total_items': cart.total_items,
            'cart_total_price': str(cart.total_price)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })

@login_required
def cart_view(request):
    """Shopping cart page"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product', 'variant').all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    # Calculate savings
    total_savings = 0
    if cart_items:
        for item in cart_items:
            if item.product.original_price and item.product.discount_percentage > 0:
                savings_per_item = item.product.original_price - item.product.price
                total_savings += savings_per_item * item.quantity
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_savings': total_savings,
    }
    
    return render(request, 'products/cart.html', context)

def get_cart_context(request):
    """Helper function to get cart context for templates"""
    cart_total_items = 0
    cart_total_price = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_total_items = cart.total_items
            cart_total_price = cart.total_price
        except Cart.DoesNotExist:
            pass
    
    return {
        'cart_total_items': cart_total_items,
        'cart_total_price': cart_total_price,
    }