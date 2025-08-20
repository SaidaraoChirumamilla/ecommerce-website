from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    Category, Brand, Product, ProductImage, ProductReview, 
    ProductVariant, Cart, CartItem, Wishlist, WishlistItem
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main', 'order']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['variant_type', 'name', 'price_adjustment', 'stock_quantity', 'sku_suffix', 'is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'brand', 'category', 'price', 'stock_quantity', 
        'is_active', 'is_featured', 'average_rating', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_featured', 'is_bestseller', 'is_new_arrival',
        'category', 'brand', 'free_shipping', 'created_at'
    ]
    search_fields = ['name', 'description', 'sku', 'tags']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'average_rating', 'review_count', 'main_image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'brand', 'category')
        }),
        ('Product Details', {
            'fields': ('short_description', 'description', 'features', 'specifications')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'discount_percentage')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'min_stock_level', 'max_order_quantity')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_bestseller', 'is_new_arrival')
        }),
        ('SEO & Marketing', {
            'fields': ('meta_title', 'meta_description', 'tags'),
            'classes': ('collapse',)
        }),
        ('Shipping', {
            'fields': ('weight', 'dimensions', 'free_shipping', 'shipping_class'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('average_rating', 'review_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Main Image', {
            'fields': ('main_image_preview',),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ProductImageInline, ProductVariantInline]
    
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_active', 'mark_as_inactive']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected products as featured"
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
    mark_as_not_featured.short_description = "Remove featured status from selected products"
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_as_active.short_description = "Mark selected products as active"
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_as_inactive.short_description = "Mark selected products as inactive"
    
    def main_image_preview(self, obj):
        main_image = obj.get_main_image()
        if main_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', main_image)
        return "No main image"
    main_image_preview.short_description = 'Main Image'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'is_main', 'order', 'image_preview', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__name', 'alt_text']
    list_editable = ['is_main', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_approved', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'created_at']
    search_fields = ['product__name', 'user__email', 'title', 'review']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_reviews', 'reject_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"
    
    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    reject_reviews.short_description = "Reject selected reviews"

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'variant_type', 'name', 'final_price', 'stock_quantity', 'is_active']
    list_filter = ['variant_type', 'is_active']
    search_fields = ['product__name', 'name', 'variant_type']
    list_editable = ['stock_quantity', 'is_active']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'updated_at', 'total_price']
    fields = ['product', 'variant', 'quantity', 'unit_price', 'total_price', 'added_at']
    
    def unit_price(self, obj):
        return obj.unit_price
    unit_price.short_description = 'Unit Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'total_items', 'total_price']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'variant', 'quantity', 'unit_price', 'total_price', 'added_at']
    list_filter = ['added_at', 'updated_at']
    search_fields = ['cart__user__email', 'product__name']
    readonly_fields = ['added_at', 'updated_at', 'unit_price', 'total_price']

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ['added_at']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    inlines = [WishlistItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['wishlist__user__email', 'product__name']
    readonly_fields = ['added_at']