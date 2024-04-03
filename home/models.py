from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User



class Technique(models.Model):
    tid = ShortUUIDField(unique = True, length = 10, max_length = 30,prefix="Technique", alphabet = "abcdefgh123456")
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "technique")

    class Meta:
        verbose_name_plural = "Techniques"

    def technique_image(self):
        return mark_safe('<img src="%s" alt="technique" />' % (self.image.url))
    
    def __str__(self):
        return self.title



class Style(models.Model):
    sid = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix = "Style", alphabet = "abcdefgh123456") 
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = "Style")
    class Meta:
        verbose_name_plural = "Styles"

    def style_image(self):
        return mark_safe('<img src="%s" alt="style" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Artist(models.Model):
    aid = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix="artist", alphabet = "abcdefgh123456")
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = user_directory_path)
    description = models.TextField(null = True, blank = True)
    address = models.CharField(max_length = 200, default = "25 Jump Street ...")
    chat_resp_time = models.CharField(max_length = 200, default = "Not much!")
    phone = models.CharField(max_length = 200, default = "06 11 22 33 44")
    shipping_time = models.CharField(max_length = 200, default = "not much")
    authentic_rating = models.CharField(max_length = 100, default ="Good")
    days_return = models.CharField(max_length = 200, default ="100")
    warranty_period = models.CharField(max_length = 200)

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) # or models.CASCADE if you want to delete the rest of their data (store, products etc)

    class Meta:
        verbose_name_plural = "Artists"

    def artist_image(self):
        return mark_safe('<img src="%s" alt="artist" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    

    
# We'll work on this later
class Tags(models.Model):
    pass

# Defining the status of products. lowercase words are the words we'll use to add the necessary logic (backend), while uppercase words are the words that'll show up (frontend)
STATUS_CHOICE = (
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),
)

STATUS = (
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In review"),
    ("published","Published")
)

RATING = (
    (1,"★☆☆☆☆"),
    (2,"★★☆☆☆"),
    (3,"★★★☆☆"),
    (4,"★★★★☆"),
    (5,"★★★★★"),
)

class Product(models.Model):
    pid = ShortUUIDField(unique = True, length = 10, max_length = 30, prefix="product", alphabet = "abcdefgh123456")
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = user_directory_path)
    description = models.TextField(null = True, blank = True)
    price = models.DecimalField(max_digits=99999, decimal_places=2) # 99999,99
    old_price = models.DecimalField(max_digits=99999,decimal_places=2) # b7al sold
    specifications = models.TextField(null=True, blank = True) 
    product_status = models.CharField(choices = STATUS, max_length=10,default = "In review")
    status =models.BooleanField(default = True)
    in_stock = models.BooleanField(default = True)
    featured = models.BooleanField(default = False)

    # The tags, the user, the technique and the style associated with the product
    # tags = models.ForeignKey(Tags, on_delete = models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    technique = models.ForeignKey(Technique, on_delete = models.SET_NULL, null=True)
    style = models.ForeignKey(Style, on_delete = models.SET_NULL, null=True)
    
    # stock keeping unit; to keep track of stock levels
    sku = ShortUUIDField(unique = True, length = 4, max_length = 20, prefix="sku ", alphabet = "1234567890")

    # Date and time when the product was created
    date = models.DateTimeField(auto_now_add = True)
    # Date and time when the product was last updated
    updated = models.DateTimeField(null = True, blank = True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" alt="product" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_discount(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to = "product/images")
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = "Product Images"



class CartOrder(models.Model):
    # User who placed the order
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=99999, decimal_places=2)
    # Whether or not the order has been paid for
    paid_status = models.BooleanField(default = False)
    order_date = models.DateTimeField(auto_now_add = True)
    product_status = models.CharField(choices = STATUS_CHOICE, max_length=40,default = "Processing")

    class Meta:
        verbose_name_plural = "Cart Orders"


class CartOrderItems(models.Model):
     # Order the item belongs to
    order = models.ForeignKey(CartOrder, on_delete = models.CASCADE)
    product_status = models.CharField(max_length = 200)
    # maybe we should replace this product_status with product_status = models.CharField(choices = STATUS_CHOICE, max_length=40,default = "Processing")
     # Item name :
    item = models.CharField(max_length = 200)
    image = models.CharField(max_length = 200)
    quantity = models.IntegerField(default = 0)
    price = models.DecimalField(max_digits=99999, decimal_places=2)
    total = models.DecimalField(max_digits=99999, decimal_places=2)
    invoice_no = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    # Display the item image
    def order_image(self):
        return mark_safe('<img src="/media/%s" alt="cart-order-items" />' % (self.image))
    




class ProductReview(models.Model):
    # User who wrote the review
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    # The product being reviewed
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    review = models.TextField()
    # Rating given by the user
    rating = models.IntegerField(choices = RATING, default=None)
    # Date and time when the review was posted
    date = models.DateTimeField(auto_now_add = True) 
    
    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating


class WishList(models.Model):
    # User who added the product to the wish list
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Product added to the wish list
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # Date and time when the product was added to the wish list
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishes List"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    # User who owns the address
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length = 100, null = True)
    address_status = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = "Addresses"

