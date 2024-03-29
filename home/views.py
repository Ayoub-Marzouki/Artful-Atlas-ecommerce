from django.shortcuts import render
from django.http import HttpResponse  # manually imported it to use it in index view

# Create your views here.
def index(request):
    # return HttpResponse("meow")
    return render(request,'home/index.html')
