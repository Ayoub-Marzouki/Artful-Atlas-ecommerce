from django.contrib import admin

from home.models import Technique, Style, Artist, Tags, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, WishList, Address

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'featured', 'product_status']

class StyleAdmin(admin.ModelAdmin):
     list_display = ['title', 'style_image']

class TechniqueAdmin(admin.ModelAdmin):
     list_display = ['title', 'technique_image']

class ArtistAdmin(admin.ModelAdmin):
     list_display = ['title', 'artist_image']

class CartOrderAdmin(admin.ModelAdmin):
     list_display = ['user', 'price','paid_status','order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
     list_display = ['order', 'invoice_no','item','image', 'quantity', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
     list_display = ['user', 'product','review','rating']

class WishListAdmin(admin.ModelAdmin):
     list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
     list_display = ['user', 'address','address_status']


# admin.site.register(Tags,TagsAdmin)
admin.site.register(Technique,TechniqueAdmin)
admin.site.register(Style,StyleAdmin)
admin.site.register(Artist,ArtistAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(ProductImages,ProductImagesAdmin)
# We commented the line above because Django will automatically display the ProductImages related to a Product in the ProductAdmin page.
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems,CartOrderItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(WishList,WishListAdmin)
admin.site.register(Address,AddressAdmin)
