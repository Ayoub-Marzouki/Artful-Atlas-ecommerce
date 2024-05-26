from django.contrib import admin
from django.utils.html import format_html
from home.models import Technique, Style, Artist, Tags, Product, ProductImages, CartOrder, CartOrderItems, ProductReview, WishList, Address, ArtistReview, SubjectMatter, Philosophy, UserReview, UserRating, Contact, NewsletterSubscriber, Profile, Offer


def display_image(obj):
    if obj.image:
        return format_html('<img src="{}" style="width: 130px; height: auto;" />', obj.image.url)
    else:
        return "No Image"

display_image.short_description = 'Image'

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', display_image, 'price', 'featured', 'exclusive', 'chosen', 'product_status']

class StyleAdmin(admin.ModelAdmin):
    list_display = ['title',]

class TechniqueAdmin(admin.ModelAdmin):
    list_display = ['title',]

class SubjectMatterAdmin(admin.ModelAdmin):
    list_display = ['title']

class PhilosophyAdmin(admin.ModelAdmin):
    list_display = ['title']

class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', display_image]

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price','paid_status','order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no','name','image', 'price']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','review','rating']

class ArtistReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'artist', 'review', 'rating']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'address_status']
    list_display = ['user', 'address', 'address_status']


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['user','review']

class UserRatingAdmin(admin.ModelAdmin):
    list_display = ['user','rating']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','subject']

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', display_image, 'verified']

class OfferAdmin(admin.ModelAdmin):
    list_display = ['user', 'artwork', 'offer_price']

# Register models with their corresponding admin classes
admin.site.register(Technique, TechniqueAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(SubjectMatter, SubjectMatterAdmin)
admin.site.register(Philosophy, PhilosophyAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ArtistReview, ArtistReviewAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(UserRating, UserRatingAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Offer, OfferAdmin)
