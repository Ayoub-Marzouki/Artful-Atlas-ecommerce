from django.urls import path, include
from home.views import index, product_list_view, artist_list_view, artist_detail_view, product_detail_view, add_product_review, add_artist_review, artist_search_view, product_search_view, add_to_cart, cart_view, delete_item_from_cart, payment, payment_completed_view, payment_failed_view, customer_dashboard, order_details, update_address_status, delete_address, wishlist_view, add_to_wishlist, delete_item_from_wishlist, services_view, contact_view, about_view, faqs_view, checkout, update_order, make_offer

app_name = "home"

urlpatterns = [
    path("",index, name="index"),
    path("services/", services_view, name = "services"),
    path("contact/", contact_view, name = "contact"),
    path("about/", about_view, name = "about"),
    path("faqs/", faqs_view, name = "faqs"),

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

    path("payment/<oid>/", payment, name ="payment"),

    path("checkout/", checkout, name = "checkout"),

    path("paypal/", include('paypal.standard.ipn.urls')), 
    path("payment/payment-completed/<oid>/", payment_completed_view, name = "payment-completed"),
    path("payment/payment-failed/", payment_failed_view, name = "payment-failed"),
    path("update-order/", update_order, name = "update_order"),

    path("dashboard/", customer_dashboard, name="dashboard"),
    path("dashboard/order/<int:id>", order_details, name="order-details"),
    path("update-address-status/", update_address_status, name = "update-address-status"),
    path("delete-address/", delete_address, name = "delete-address"),

    path("wishlist/", wishlist_view, name = "wishlist"),
    path("add-to-wishlist/", add_to_wishlist, name = "add-to-wishlist"),
    path("delete-from-wishlist/", delete_item_from_wishlist, name ="delete-from-wishlist"),

    path('make-offer/<pid>/', make_offer, name='make-offer'),
]