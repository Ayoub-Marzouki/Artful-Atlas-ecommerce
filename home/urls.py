from django.urls import path
from home.views import index, product_list_view, artist_list_view, artist_detail_view, product_detail_view

app_name = "home"

urlpatterns = [
    path("",index, name="index"),

    path("store/",product_list_view, name="store"),
    path("store/<pid>/",product_detail_view, name="product-details"),

    path("artists/", artist_list_view, name = "artists"),
    path("artists/<aid>/",artist_detail_view, name="artist-details"),
]