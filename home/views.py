from django.shortcuts import render, HttpResponse
from django.db.models import Q, Avg
from home.models import Technique, Style, SubjectMatter, Philosophy, Product, Artist, ProductReview, ArtistReview
from home.forms import ProductReviewForm, ArtistReviewForm

def index(request):
    return render(request,'home/index.html')


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


