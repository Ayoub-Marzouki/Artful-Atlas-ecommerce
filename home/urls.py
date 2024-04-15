from django.urls import path
from home.views import index, product_list_view, artist_list_view, artist_detail_view, product_detail_view, add_product_review, add_artist_review, artist_search_view, product_search_view, add_to_cart, cart_view, delete_item_from_cart

app_name = "home"

urlpatterns = [
    path("",index, name="index"),

    path("store/",product_list_view, name="store"),
    path("store/<pid>/",product_detail_view, name="product-details"),

    path("artists/", artist_list_view, name = "artists"),
    path("artists/<aid>/",artist_detail_view, name="artist-details"),

    path("add-product-review/<int:pid>/",add_product_review, name ="add-product-review"),
    path("add-artist-review/<int:aid>/",add_artist_review, name ="add-artist-review"),

    path("search/artists/", artist_search_view, name = "artist-search"),
    path("search/artworks/", product_search_view, name= "product-search"),

    path("add-to-cart/", add_to_cart, name = "add-to-cart"),
    path("cart/",cart_view, name="cart"),
    path("delete-from-cart/",delete_item_from_cart, name="delete-from-cart"),
]