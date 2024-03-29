from django.urls import path
from home.views import index

app_name = "first_app_urls"

urlpatterns = [
    path("",index)
]