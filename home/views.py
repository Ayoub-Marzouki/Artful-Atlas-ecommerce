from django.shortcuts import render, HttpResponse
from django.db.models import Q, Avg
from home.models import Technique, Style, Product, Artist, ProductReview, ArtistReview
from home.forms import ProductReviewForm, ArtistReviewForm
from django.http import JsonResponse

def index(request):
    return render(request,'home/index.html')


def product_list_view(request):
    products = Product.objects.filter(product_status = "published")
    
    context = {
        "products":products
    }
    return render(request,'store/store.html', context)


def product_detail_view(request, pid):
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
    }
    return render(request, "store/product-details.html",context)


def artist_list_view(request):
    artists = Artist.objects.all()
    context = {
        "artists": artists,
    }
    return render(request, "artists/artists.html",context)

def artist_detail_view(request, aid):
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



# def technique_list_view(request):
#     techniques = Technique.objects.all()
    
#     context = {
#         "techniques":techniques
#     }
#     return render(request,'home/')

# def style_list_view(request):
#     styles = Style.objects.all()
    
#     context = {
#         "styles":styles
#     }
#     return render(request,'home/')


