from django.urls import path
from home.views import index, product_list_view

app_name = "home"

urlpatterns = [
    path("",index, name="index"),
    path("store/",product_list_view, name="store")
]