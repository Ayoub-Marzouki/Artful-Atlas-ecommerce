from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg, Count, F
from home.models import Technique, Style, SubjectMatter, Philosophy, Product, Artist, ProductReview, ArtistReview, CartOrder, CartOrderItems, Address, WishList, UserReview, UserRating, Profile, Offer
from home.forms import ProductReviewForm, ArtistReviewForm, CheckoutForm, UserReviewForm, UserRatingForm, ContactForm, NewsletterSubscriptionForm, ProfileForm, OfferForm
from django.template.loader import render_to_string

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

import calendar, stripe
from django.db.models.functions import ExtractMonth

from django.core.exceptions import ObjectDoesNotExist

import datetime, json

def index(request):
    artists = Artist.objects.all()
    products = Product.objects.all()
    
    try:
        chosen_product = Product.objects.get(chosen=True)
        exclusive_products = Product.objects.filter(exclusive = True)
        featured_products = Product.objects.filter(featured = True)
    except ObjectDoesNotExist:
        chosen_product = None
        exclusive_products = None
        featured_products = None

    # Add user reviews / ratings :

    reviews = UserReview.objects.all().order_by("-date") # to show the latest reviews
    ratings = UserRating.objects.all().order_by("-date")

    

    
    user_rating = UserRating()
    user_review = UserReview()

    if request.method == 'POST':
        if request.POST.get('action') == 'review': 
            user_review = UserReview.objects.create(
            user=request.user,
            review=request.POST['review']
        )
        elif request.POST.get('action') == 'rating':  
            user_rating = UserRating.objects.create(
            user=request.user,
            rating=request.POST['rating']
        )

    # User review form
    review_form = UserReviewForm()
    rating_form = UserRatingForm()
    
    # Allow only 1 review per user
    make_review = True
    make_rating = True
    
    rating_count = UserRating.objects.all().count()
    
    if request.user.is_authenticated:
        user_review_count = UserReview.objects.filter(user=request.user).count()
        user_rating_count = UserRating.objects.filter(user=request.user).count()

        if user_review_count > 0:
            make_review = False
        if user_rating_count > 0:
            make_rating = False
    

    average_rating = UserRating.objects.all().aggregate(rating=Avg("rating"))

    if request.user.is_authenticated:
        user = request.user # to get the current user
        context = {
        'featured_products':featured_products,
        'exclusive_products':exclusive_products,
        'chosen_product':chosen_product,
        'products':products,
        'artists':artists,

        'user':user.username,
        'review':user_review.review,
        'reviews':reviews,
        'ratings':ratings,
        'review_form':review_form,
        'rating_form':rating_form,
        'make_review':make_review,
        'make_rating':make_rating,
        'rating':user_rating.rating,
        "average_rating":average_rating,
        'rating_count':rating_count,
    }
    else:
        context = {
        'featured_products':featured_products,
        'exclusive_products':exclusive_products,
        'chosen_product':chosen_product,
        'products':products,
        'artists':artists,

        'review':user_review.review,
        'reviews':reviews,
        'ratings':ratings,
        'review_form':review_form,
        'rating_form':rating_form,
        # 'make_review':make_review,
        'rating':user_rating.rating,
        "average_rating":average_rating,
        'rating_count':rating_count,
    }
    return render(request,'home/index.html', context)

def services_view(request):

    return render(request, 'home/services.html')

def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request,"Message sent! Thank you for your feedback.")
            return redirect("home:contact")
    else:
        contact_form = ContactForm()
    

    # Handling the subscription to NewsLetter
    if request.method == 'POST':
        newsletter_form = NewsletterSubscriptionForm(request.POST)
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request,"Subscribed!")
            return redirect("home:contact")
    else:
        newsletter_form = NewsletterSubscriptionForm()

    context = {
        'contact_form':contact_form,
        'newsletter_form':newsletter_form,
    } 
    return render(request,'home/contact.html', context)


def about_view(request):
    reviews = UserReview.objects.all().order_by("-date")

    context = {
        'reviews':reviews,
    }
    
    return render(request,'home/about.html', context)

def faqs_view(request):
    
    return render(request,'home/faqs.html')

def product_list_view(request):
    products = Product.objects.filter(product_status = "published")
    techniques = Technique.objects.all().order_by('title')
    styles = Style.objects.all().order_by('title')
    subjects = SubjectMatter.objects.all().order_by('title')
    philosophies = Philosophy.objects.all().order_by('title')
    
    context = {
        "products":products,
        "techniques":techniques,
        "styles":styles,
        "subjects":subjects,
        "philosophies":philosophies,
    }
    return render(request,'store/store.html', context)


def product_detail_view(request, pid):
    
    current_url = request.build_absolute_uri()
    next_url = request.GET.get('next')

    product = Product.objects.get(pid=pid)
    product_wishlist_count = product.wishlist_set.count()
    product_images = product.product_images.all()
    related_products = Product.objects.filter(Q(technique=product.technique) | Q(style=product.style)).exclude(pid=pid)[:10]

    # Reviews 
    reviews = ProductReview.objects.filter(product=product).order_by("-date") # to show the latest reviews

    # Get average reviews of a product
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))

    # Product review form
    review_form = ProductReviewForm()

    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count > 0:
            make_review = False

    # Check if the logged-in user is the artist themselves
    if request.user == product.artist.user:
        make_review = False
       


    context = {
        "product":product,
        "product_images":product_images,
        "reviews":reviews,
        "review_form":review_form,
        "average_rating":average_rating,
        "related_products":related_products,
        "make_review":make_review,
        "next_url": next_url,
        "current_url":current_url,
        'product_wishlist_count':product_wishlist_count,
    }
    return render(request, "store/product-details.html",context)


def artist_list_view(request):
    artists = Artist.objects.all()
    techniques = Technique.objects.all().order_by('title')
    styles = Style.objects.all().order_by('title')
    subjects = SubjectMatter.objects.all().order_by('title')
    philosophies = Philosophy.objects.all().order_by('title')
    context = {
        "artists": artists,
        "techniques":techniques,
        "styles":styles,
        "subjects":subjects,
        "philosophies":philosophies,
    }
    return render(request, "artists/artists.html",context)

def artist_detail_view(request, aid):
    current_url = request.build_absolute_uri()
    next_url = request.GET.get('next')

    print("next url",next_url)
    print("current url ", current_url)


    artist = Artist.objects.get(aid=aid)
    reviews = ArtistReview.objects.filter(artist=artist).order_by("-date") # to show the latest reviews

    # Get average reviews of a product
    average_rating = ArtistReview.objects.filter(artist=artist).aggregate(rating = Avg('rating'))

    # Increment artist view count
    artist.views += 1
    artist.save()

    # Product review form
    review_form = ArtistReviewForm()
    
    # Allow only 1 review per artist per user
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ArtistReview.objects.filter(user=request.user, artist=artist).count()

        if request.user == artist.user:
            make_review = False
            
        elif user_review_count > 0:
            make_review = False
    
    context = {
        "artist": artist,
        "reviews":reviews,
        "make_review":make_review,
        "review_form":review_form,
        "average_rating":average_rating,
        "next_url": next_url,
        "current_url":current_url,
    }
    return render(request, "artists/artist-details.html",context)


def add_product_review(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user # to get the logged in user
    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating']
    )

    product_images = product.product_images.all()
    related_products = Product.objects.filter(Q(technique=product.technique) | Q(style=product.style)).exclude(pid=pid)[:10]

    # Reviews 
    reviews = ProductReview.objects.filter(product=product).order_by("-date") # to show the latest reviews

    # Get average reviews of a product
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))

    # Product review form
    review_form = ProductReviewForm()

    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
        'average_rating':average_rating,
        "product":product,
        "product_images":product_images,
        "reviews":reviews,
        "review_form":review_form,
        "related_products":related_products,
        "make_review":make_review,
    }
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return render(request, "store/product-details.html",context)

def add_artist_review(request,aid):
    artist = Artist.objects.get(pk=aid)
    user = request.user # to get the logged in user
    review = ArtistReview.objects.create(
        user = user,
        artist = artist,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    reviews = ArtistReview.objects.filter(artist=artist).order_by("-date") # to show the latest reviews

    # Product review form
    review_form = ArtistReviewForm()
    
    # Allow only 1 review per artist per user
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ArtistReview.objects.filter(user=request.user, artist=artist).count()

        if user_review_count > 0:
            make_review = False
    

    average_rating = ArtistReview.objects.filter(artist=artist).aggregate(rating=Avg("rating"))
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'reviews':reviews,
        'review_form':review_form,
        'make_review':make_review,
        'rating':request.POST['rating'],
        'average_rating':average_rating,
        "artist": artist,
        "average_rating":average_rating,
    }

    return render(request, "artists/artist-details.html",context)




def artist_search_view(request):
    query = request.GET.get("q")
    location = request.GET.get("location")
    techniques_ids = request.GET.getlist("techniques")  
    styles_ids = request.GET.getlist("styles")         
    subjects_ids = request.GET.getlist("subjects") 
    philosophies_ids = request.GET.getlist("philosophies")

    artists = Artist.objects.all()
    all_techniques = Technique.objects.all()
    all_styles = Style.objects.all()
    all_subjects = SubjectMatter.objects.all()
    all_philosophies = Philosophy.objects.all()
    
    selected_techniques = Technique.objects.filter(pk__in=techniques_ids)
    selected_styles = Style.objects.filter(pk__in=styles_ids)
    selected_subjects = SubjectMatter.objects.filter(pk__in=subjects_ids)
    selected_philosophies = Philosophy.objects.filter(pk__in=philosophies_ids)

    if query and location:
        artists = artists.filter(Q(name__icontains=query) & Q(city__icontains=location))
    elif query:
        artists = artists.filter(name__icontains=query)
    elif location:
        artists = artists.filter(city__icontains=location)

    if techniques_ids:
        artists = artists.filter(technique__in=selected_techniques)

    if styles_ids:
        artists = artists.filter(style__in=selected_styles)

    if subjects_ids:
        artists = artists.filter(subject_matter__in=selected_subjects)

    if philosophies_ids:
        artists = artists.filter(philosophy__in=selected_philosophies)
    
    context = {
        "artists": artists,
        "query": query,
        "location": location,
        "selected_techniques": selected_techniques,
        "selected_styles": selected_styles,
        "selected_subjects": selected_subjects,
        "selected_philosophies": selected_philosophies,
        "all_techniques": all_techniques,
        "all_styles": all_styles,
        "all_subjects": all_subjects,
        "all_philosophies": all_philosophies,
    }

    return render(request, "search/artists-search.html", context)


def product_search_view(request):
    query = request.GET.get("q")
    techniques_ids = request.GET.getlist("techniques")  
    styles_ids = request.GET.getlist("styles")         
    subjects_ids = request.GET.getlist("subjects") 
    philosophies_ids = request.GET.getlist("philosophies")
    price_range = request.GET.get("price_range")

    products = Product.objects.all()
    all_techniques = Technique.objects.all()
    all_styles = Style.objects.all()
    all_subjects = SubjectMatter.objects.all()
    all_philosophies = Philosophy.objects.all()
    
    selected_techniques = Technique.objects.filter(pk__in=techniques_ids)
    selected_styles = Style.objects.filter(pk__in=styles_ids)
    selected_subjects = SubjectMatter.objects.filter(pk__in=subjects_ids)
    selected_philosophies = Philosophy.objects.filter(pk__in=philosophies_ids)

    selected_price_ranges = []

    if query :
        products = products.filter(title__icontains=query)
    if techniques_ids:
        products = products.filter(technique__in=selected_techniques)

    if styles_ids:
        products = products.filter(style__in=selected_styles)

    if subjects_ids:
        products = products.filter(subject_matter__in=selected_subjects)

    if philosophies_ids:
        products = products.filter(philosophy__in=selected_philosophies)
    
    if price_range:
        selected_price_ranges.append(price_range)
        if price_range == "under_500":
            products = products.filter(price__lt=500)
        elif price_range == "500_1000":
            products = products.filter(price__range=(500, 1000))
        elif price_range == "1000_2000":
            products = products.filter(price__range=(1000, 2000)) 
        elif price_range == "2000_5000":
            products = products.filter(price__range=(2000, 5000)) 
        elif price_range == "5000_10000":
            products = products.filter(price__range=(5000, 10000)) 
        elif price_range == "above_10000":
            products = products.filter(price__gt=(10000)) 


    context = {
        "products": products,
        "query": query,
        "selected_techniques": selected_techniques,
        "selected_styles": selected_styles,
        "selected_subjects": selected_subjects,
        "selected_philosophies": selected_philosophies,
        "selected_price_ranges":selected_price_ranges,
        "all_techniques": all_techniques,
        "all_styles": all_styles,
        "all_subjects": all_subjects,
        "all_philosophies": all_philosophies,
    }

    return render(request, "search/products-search.html", context)


def add_to_cart(request):
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'price': request.GET['price'],
        'image':request.GET['image'],
        'artist':request.GET['artist'],
        'page':request.GET['page'],
        'artistpage':request.GET['artistpage'],
    }
    if 'cart_data_object' in request.session:
        if str(request.GET['id']) in request.session['cart_data_object']:
            cart_data = request.session['cart_data_object']
            cart_data[str(request.GET['id'])]['quantity'] = 1  # Always set quantity to 1
            cart_data.update(cart_data)
            request.session['cart_data_object'] = cart_data
        else:
            cart_data = request.session['cart_data_object']
            cart_data.update(cart_product)
            request.session['cart_data_object'] = cart_data
    else:
        request.session['cart_data_object'] = cart_product

    return JsonResponse({"data": request.session['cart_data_object'], 'totalCartItems': len(request.session['cart_data_object'])})


def cart_view(request):
    total_price = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            total_price += float(item['price'])  # Update total price for each item
        return render(request, "home/cart.html", {"cart_data": request.session['cart_data_object'], 'totalCartItems': len(request.session['cart_data_object']), 'total_price': total_price})
    else:
        return render(request, "home/cart.html", {"cart_data": '', 'totalCartItems': 0, 'total_price': total_price})


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_object' in request.session:
        if product_id in request.session['cart_data_object']:
            cart_data = request.session['cart_data_object']
            del request.session['cart_data_object'][product_id]
            request.session['cart_data_object'] = cart_data
    
    total_price = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            total_price += float(item['price'])

    context = render_to_string("home/updated-cart.html", {"cart_data": request.session['cart_data_object'], 'totalCartItems': len(request.session['cart_data_object']), 'total_price': total_price})

    return JsonResponse({"data":context, 'totalCartItems': len(request.session['cart_data_object'])})  


def checkout(request):
    total_price = 0
    cart_total_price = 0
    
    order = CartOrder()

    try:
        active_address = Address.objects.get(user = request.user, address_status = True)
    except:  
        active_address = None  

    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            total_price += float(item['price'])

    # if request.method=="POST":
    #     full_name = request.POST.get("full-name") 
    #     address = request.POST.get("address")
    #     zip = request.POST.get("zip")
    #     country = request.POST.get("country")
    #     city = request.POST.get("city")
    #     email = request.POST.get("email")
    #     phone = request.POST.get("phone")

    #     request.session['full_name'] = full_name
    #     request.session['email'] = email
    #     request.session['phone'] = phone
    #     request.session['address'] = address
    #     request.session['zip'] = zip
    #     request.session['country'] = country
    #     request.session['city'] = city


    #     order = CartOrder.objects.create(
    #     user=request.user,
    #     full_name = full_name,
    #     email = email,
    #     phone = phone,
    #     address = address,
    #     zip = zip,
    #     country = country,
    #     city = city,
    #     price = total_price,
    #     )
    #     del request.session['full_name']
    #     del request.session['email'] 
    #     del request.session['phone']
    #     del request.session['address']
    #     del request.session['zip']
    #     del request.session['country'] 
    #     del request.session['city']

    #     for product_id, item in request.session['cart_data_object'].items():
    #         cart_total_price += float(item['price'])
    #         total_price += float(item['price'])
            
    #         cart_order_items = CartOrderItems.objects.create(
    #         order = order,
    #         invoice_no = "INVOICE_NO-" + str(order.id),
    #         name = item['title'],
    #         image = item['image'],
    #         price = item['price'],
    #         total = float(item['price']),
    #         product_page = item['page']
    #     )
    #     return redirect("home:payment", order.oid)

        order.user = request.user
        order.email = request.user.email
        if request.user.profile.phone:
            order.phone = request.user.profile.phone
        order.price = total_price
        price_in_usd = total_price / 10
        order.address = active_address.address
        order.save()
        
        for product_id, item in request.session['cart_data_object'].items():
            cart_total_price += float(item['price'])
            total_price += float(item['price'])
            product = Product.objects.get(id=product_id)
            cart_order_items = CartOrderItems.objects.create(
            product = product,
            order = order,
            invoice_no = "INVOICE_NO-" + str(order.id),
            name = item['title'],
            image = item['image'],
            price = item['price'],
            total = float(item['price']),
            product_page = item['page']
        )

    context = {
        "cart_data": request.session['cart_data_object'], 
        'totalCartItems': len(request.session['cart_data_object']), 
        'total_price': total_price,
        'active_address':active_address,
        'order':order,
        'price_in_usd':price_in_usd,
    }
    
    return render(request, "home/checkout.html", context)


def payment(request, oid):
    order = CartOrder.objects.get(oid = oid)
    order_items = CartOrderItems.objects.filter(order = order)

    context = {
        "order":order,
        "order_items":order_items,
    }
    return render(request, "home/payment.html", context) 
    


def payment_completed_view(request, oid):
    # Retrieve the CartOrder instance
    order = CartOrder.objects.get(oid=oid)

    # Calculate the total price of the cart items
    total_price = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            total_price += float(item['price'])

    # Access the associated CartOrderItems instances directly from the CartOrder instance
    cart_order_items = order.cartorderitems_set.all()

    # Update the paid_status of the order 
    if not order.paid_status:
        order.paid_status = True
        order.save()

        products = Product.objects.filter(cartorderitems__order=order)
        # Mark artworks as SOLD
        products.update(available=False)



    context = {
        "cart_data": request.session.get('cart_data_object', {}),
        'totalCartItems': len(request.session.get('cart_data_object', {})),
        'total_price': total_price,
        'order': order,
        'cart_order_items': cart_order_items,
    }
    return render(request, 'home/payment/payment-completed.html', context)



def payment_failed_view(request):
    # context = {
    #     'context':context,
    # }
    return render(request, 'home/payment/payment-failed.html')


@login_required
def customer_dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = Profile()

    address = Address.objects.filter(user = request.user).order_by("-address_status")

    offers = Offer.objects.filter(user = request.user).order_by("-id")

    this_month = datetime.datetime.now().month
    orders = CartOrder.objects.filter(user = request.user).order_by("-id")


    if request.method == "POST" and "add-address-button-name" in request.POST:
        address = request.POST.get("address")

        new_address = Address.objects.create(
            user = request.user,
            address = address,
        )
        messages.success(request,"Address added successfully!")
        return redirect("home:dashboard")


    if request.method == "POST" and "profile" in request.POST:
        # Check if the request is for editing profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_instance = profile_form.save(commit=False)
            profile_instance.user = request.user
            profile_instance.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("home:dashboard")
    else:
        profile_form = ProfileForm(instance=profile)

    if request.method == "POST":
        # Check if the user clicked the "Become an artist" button
        if "become-artist-button-name" in request.POST:
            user = request.user
            user.user_type = 'artist'
            Artist.objects.create(user=user, name=user.username)
            user.save()
            messages.success(request, "You are officially a registered artist on our website!")
            return redirect("artist-dashboard:artist-dashboard")

    context = {
        'orders':orders,
        'address':address,
        'this_month':this_month,
        'profile':profile,
        'profile_form':profile_form,
        'offers':offers,
    }
    return render(request, 'home/dashboard.html', context)



def update_address_status(request):
    id = request.GET['id']
    Address.objects.update(address_status = False)
    Address.objects.filter(id = id).update(address_status = True)
    return JsonResponse({"boolean": True})


def delete_address(request):
    if request.method == "GET":
        address_id = request.GET.get("address_id")

        try:
            address_to_delete = Address.objects.get(id=address_id)
            address_to_delete.delete()
            return JsonResponse({"success": True})
        except Address.DoesNotExist:
            return JsonResponse({"success": False, "error": "Address does not exist"}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def order_details(request, id):
    order = CartOrder.objects.get(user = request.user, id = id)
    order_items = CartOrderItems.objects.filter(order=order)
    
    context = {
        'order':order,
        'order_items':order_items,
    }
    return render(request, 'home/order-details.html', context)


def wishlist_view(request):
    if request.user.is_authenticated: 
        wishlist =WishList.objects.filter(user = request.user)
        wishlist_count = WishList.objects.filter(user = request.user).count()
        context = {
            'wishlist':wishlist,
            'wishlist_count':wishlist_count,
        }
        return render(request,"home/wishlist.html", context)
    else:
        messages.warning(request, "You must be logged in in order to have a wishlist.")
        return redirect('userauths:login')


def add_to_wishlist(request):
    product_id = request.GET.get('id')
    product = Product.objects.get(id=product_id)

    # Check if the product is already in the wishlist
    if WishList.objects.filter(product=product, user=request.user).exists():
        is_added = False
    else:
        # Add the product to the wishlist
        WishList.objects.create(product=product, user=request.user)
        is_added = True

    # Count the total number of wishlist items for the current user
    wishlist_count = WishList.objects.filter(user=request.user).count()

    # Construct the JSON response
    response_data = {
        "success": True,
        "wishlist_count": wishlist_count,
        "is_added": is_added
    }

    return JsonResponse(response_data)


def delete_item_from_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET.get('id')
        try:
            wishlist_item = WishList.objects.get(product_id=product_id, user=request.user)
            wishlist_item.delete()
            wishlist_count = WishList.objects.filter(user=request.user).count()
            return JsonResponse({'wishlist_count': wishlist_count,'success': True, 'message': 'Item removed from wishlist'})
        except WishList.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found in wishlist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    


@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        # Retrieve data from the AJAX request
        order_oid = request.POST.get('order_oid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip')

        # Retrieve the order object
        try:
            order = CartOrder.objects.get(oid=order_oid)
        except CartOrder.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

        # Update the order object with the retrieved data
        order.first_name = first_name
        order.last_name = last_name
        order.address = address
        order.city = city
        order.country = country
        order.zip = zip_code

        # Save the updated order object
        order.save()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Order updated successfully'})

    else:
        # If the request method is not POST, return an error response
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@login_required
def make_offer(request, pid):
    product = get_object_or_404(Product, pid=pid)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.artwork = product
            offer.user = request.user
            offer.save()
            messages.success(request, "Your offer has been sent to the artist!")
            return redirect('home:product-details', pid=pid)
    else:
        form = OfferForm()
    context = {
        'form': form, 
        'product': product,
    }
    return render(request, 'home/make-offer.html', context)
