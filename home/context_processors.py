from .models import WishList

def default(request):
    if request.user.is_authenticated:
        wishlist_count = WishList.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0

    context = {
        'wishlist_count':wishlist_count,
    }
    return (context)
