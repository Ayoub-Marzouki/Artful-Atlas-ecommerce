from django.shortcuts import render, HttpResponse
from home.models import Technique, Style, Product, Artist


def index(request):
    return render(request,'home/index.html')


def product_list_view(request):
    products = Product.objects.filter(product_status = "published")
    
    context = {
        "products":products
    }
    return render(request,'store/store.html', context)


def artist_list_view(request):
    artists = Artist.objects.all()
    context = {
        "artists": artists,
    }
    return render(request, "artists/artists.html",context)

def artist_detail_view(request, aid):
    artist = Artist.objects.get(aid=aid)
    context = {
        "artist": artist,
    }
    return render(request, "artists/artists.html",context)

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


