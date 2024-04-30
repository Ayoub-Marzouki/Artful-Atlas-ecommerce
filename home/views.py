from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.db.models import Q, Avg
from home.models import Technique, Style, SubjectMatter, Philosophy, Product, Artist, ProductReview, ArtistReview, CartOrder, CartOrderItems, Address, WishList
from home.forms import ProductReviewForm, ArtistReviewForm, CheckoutForm
from django.template.loader import render_to_string

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

def index(request):
    artists = Artist.objects.all()
    products = Product.objects.all()
    exclusive_products = Product.objects.filter(exclusive = True)
    featured_products = Product.objects.filter(featured = True)
    chosen_product = Product.objects.get(chosen = True)
    context = {
        'featured_products':featured_products,
        'exclusive_products':exclusive_products,
        'chosen_product':chosen_product,
        'products':products,
        'artists':artists,
    }
    return render(request,'home/index.html', context)


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
        "product":product,
        "product_images":product_images,
        "reviews":reviews,
        "review_form":review_form,
        "average_rating":average_rating,
        "related_products":related_products,
        "make_review":make_review,
        "next_url": next_url,
        "current_url":current_url,
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

    # Product review form
    review_form = ArtistReviewForm()
    
    # Allow only 1 review per artist per user
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ArtistReview.objects.filter(user=request.user, artist=artist).count()

        if user_review_count > 0:
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


def checkout_view(request):

    paypal_total_price = 0
    cart_total_price = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            paypal_total_price += float(item['price'])

        order = CartOrder.objects.create(
            user=request.user,
            price = paypal_total_price,
        )
        # Cart 
        for product_id, item in request.session['cart_data_object'].items():
            cart_total_price += float(item['price'])
            cart_order_items = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-" + str(order.id),
                name = item['title'],
                image = item['image'],
                price = item['price'],
                total = float(item['price']),
                product_page = item['page']
            )


    host = request.get_host()
    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':cart_total_price,
        'item_name':"Order-Item-No-" + str(order.id),
        'invoice':"Invoice_No-" + str(order.id),
        'currency_code':"MAD",
        'notify_url':'http://{}{}'.format(host, reverse("home:paypal-ipn")),
        'return_url':'http://{}{}'.format(host, reverse("home:payment-completed")),
        'cancel_url':'http://{}{}'.format(host, reverse("home:payment-failed")),
    }

    paypal_payment_button = PayPalPaymentsForm(initial = paypal_dict)

    total_price = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            total_price += float(item['price'])

    try:
        active_address = Address.objects.get(user = request.user, address_status = True)
    except:
        messages.warning(request, "Multiple addresses are selected as default at once. Please select only one as a default address.")  
        active_adress = None  
    
    # checkout_form = CheckoutForm()
    context = {
        "cart_data": request.session['cart_data_object'],
        'totalCartItems': len(request.session['cart_data_object']), 
        'total_price': total_price, 'paypal_payment_button':paypal_payment_button,
        "active_address":active_address,
        #'checkout_form':checkout_form
    }
    return render(request, "home/checkout.html", context) 



def save_checkout_info(request):
    total_price = 0

    if request.method=="POST":
        first_name = request.POST.get["first-name"] 
        last_name = request.POST.get["last-name"]
        address = request.POST.get["address"]
        zip = request.POST.get["zip"]
        country = request.POST.get["country"]
        city = request.POST.get["city"]

        request.session['first_name'] = first_name
        request.session['last-name'] = last_name
        request.session['address'] = address
        request.session['zip'] = zip
        request.session['country'] = country
        request.session['city'] = city

        if 'cart_data_object' in request.session:
            for product_id, item in request.session['cart_data_object'].items():
                total_price += float(item['price'])

    # checkout_form = CheckoutForm()
    
    return render(request, "home/checkout.html", {"cart_data": request.session['cart_data_object'], 'totalCartItems': len(request.session['cart_data_object']), 'total_price': total_price,}) #'checkout_form':checkout_form


def payment_completed_view(request):
    total_price = 0
    if 'cart_data_object' in request.session:
        for product_id, item in request.session['cart_data_object'].items():
            total_price += float(item['price'])
    
    context = {
        "cart_data": request.session['cart_data_object'],
        'totalCartItems': len(request.session['cart_data_object']),
        'total_price': total_price,
    }
    return render(request, 'home/payment/payment-completed.html', context)

def payment_failed_view(request):
    # context = {
    #     'context':context,
    # }
    return render(request, 'home/payment/payment-failed.html')


@login_required
def customer_dashboard(request):
    orders = CartOrder.objects.filter(user = request.user).order_by("-id")
    address = Address.objects.filter(user = request.user).order_by("-address_status")

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        new_address = Address.objects.create(
            user = request.user,
            address = address,
            phone = phone
        )
        messages.success(request,"Address added successfully!")
        return redirect("home:dashboard")

    context = {
        'orders':orders,
        'address':address,
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
    wishlist =WishList.objects.filter(user = request.user)
    wishlist_count = WishList.objects.filter(user = request.user).count()
    context = {
        'wishlist':wishlist,
        'wishlist_count':wishlist_count,
    }
    return render(request,"home/wishlist.html", context)


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
    
