from django.urls import path
from home.views import index, product_list_view, artist_list_view, artist_detail_view, product_detail_view, add_product_review, add_artist_review

app_name = "home"

urlpatterns = [
    path("",index, name="index"),

    path("store/",product_list_view, name="store"),
    path("store/<pid>/",product_detail_view, name="product-details"),

    path("artists/", artist_list_view, name = "artists"),
    path("artists/<aid>/",artist_detail_view, name="artist-details"),

    path("add-product-review/<int:pid>/",add_product_review, name ="add-product-review"),
    
    path("add-artist-review/<int:aid>/",add_artist_review, name ="add-artist-review"),
]