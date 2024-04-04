from django.shortcuts import render
from home.models import Technique, Style, Product


def index(request):
    return render(request,'home/index.html')


def product_list_view(request):
    products = Product.objects.filter(product_status = "published")
    
    context = {
        "products":products
    }
    return render(request,'store/store.html', context)


def technique_list_view(request):
    techniques = Technique.objects.all()
    
    context = {
        "techniques":techniques
    }
    return render(request,'home/')

def style_list_view(request):
    styles = Style.objects.all()
    
    context = {
        "styles":styles
    }
    return render(request,'home/')


