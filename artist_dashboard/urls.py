from django.urls import path, include

from artist_dashboard.views import artist_dashboard, update_profile, artworks, edit_artwork, orders, reviews, account_details, delete_artwork, order_detail

app_name = "artist-dashboard"


urlpatterns = [
    path("", artist_dashboard, name="artist-dashboard"),
    path("update-profile/<aid>/", update_profile, name= "update-profile"),
    path("artworks/", artworks, name="artworks"),
    path("edit-artwork/<pid>/", edit_artwork, name="edit-artwork"),
    path("delete-artwork/<pid>/", delete_artwork, name = "delete-artwork"),
    path("orders/", orders, name="orders"),
    path("orders/order-details/<id>", order_detail, name = "order-details"),
    path("reviews/", reviews, name="reviews"),
    path("account-details/", account_details, name="account-details"),

]