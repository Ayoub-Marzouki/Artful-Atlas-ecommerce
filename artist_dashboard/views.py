from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.db.models import Sum, Count
from home.models import CartOrder, Product, Technique, Style, Philosophy, SubjectMatter, CartOrderItems, Artist, ProductReview, ArtistReview
from .forms import addArtworkForm, UpdateOrderStatusForm, ProfileImageForm, CoverImageForm, SocialMediaForm, ArtistInfoForm, OrientationForm, DescriptionForm,BiographyForm

import datetime
from django.contrib import messages
from django.contrib.auth.hashers import check_password


def artist_dashboard(request):
    user = request.user

    try:
        # Retrieve data for the artist dashboard
        artist = Artist.objects.get(user=user)
        
        # Retrieve the number of orders involving the artist, through the artworks chosen by the buyer
        total_orders_count = CartOrder.objects.filter(cartorderitems__product__artist=artist).count()       

        # Revenue from orders involving the artist's artworks
        revenue = CartOrder.objects.filter(cartorderitems__product__artist=artist, paid_status=True).aggregate(total_revenue=Sum('price'))['total_revenue'] or 0

        # Artworks created by the artist
        artworks_number = Product.objects.filter(artist=artist).count()

        this_month = datetime.datetime.now().month

        monthly_revenue = CartOrder.objects.filter(cartorderitems__product__artist=artist, paid_status=True, order_date__month=this_month).aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
    
    except Artist.DoesNotExist:
        # If the user is not an artist, return a forbidden response
        return HttpResponseForbidden("You are not authorized yet to access this page as you are not an artist. Please go to your Account details in your account dashboard and become an artist.")

    context = {
        'artist': artist,
        'total_orders_count': total_orders_count,
        'revenue': revenue,
        'artworks_number': artworks_number,
        'this_month':this_month,
        'monthly_revenue':monthly_revenue,
    }

    return render(request, "artist-dashboard/dashboard.html", context)

def artworks(request):
    user = request.user 
    artist = Artist.objects.get(user=user)

    # Add Artwork
    form = addArtworkForm()
    if request.method == "POST" and "add-artwork-button-name" in request.POST:
        form = addArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.user = user
            new_form.artist = artist 
            new_form.save() 
            form.save_m2m() # many 2 many field
            form = addArtworkForm()


    # Artworks created by the artist
    artworks = Product.objects.filter(artist=artist).order_by("-id")

    context = {
        'artist':artist,
        'artworks':artworks,
        'form':form,
    }
    return render(request, "artist-dashboard/artworks.html", context)


def edit_artwork(request, pid):
    user = request.user 
    artist = Artist.objects.get(user=user)

    artworks = Product.objects.filter(artist=artist).order_by("-id")
    artwork = Product.objects.get(pid = pid)

    # Edit Artwork
    form = addArtworkForm(instance = artwork)
    if request.method == "POST":
        form = addArtworkForm(request.POST, request.FILES, instance = artwork)
        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.user = user
            new_form.artist = artist 
            new_form.save() 
            form.save_m2m() # many 2 many field
            return redirect("artist-dashboard:artworks")

    context = {
        'artist':artist,
        'artworks':artworks,
        'form':form,
    }

    return render(request, "artist-dashboard/edit-artwork.html", context)

def delete_artwork(request, pid):
    artwork = Product.objects.get(pid = pid)
    artwork.delete()
    return redirect("artist-dashboard:artworks")



def orders(request):
    user = request.user 
    artist = Artist.objects.get(user=user)
    
    # Same thing for orders associated with the artist
    orders = CartOrder.objects.filter(cartorderitems__product__artist=artist)

    context = {
        'artist':artist,
        'orders':orders,
        
    }
    return render(request, "artist-dashboard/orders.html", context)

def order_detail(request, id):
    order = CartOrder.objects.get(id = id)
    order_items = CartOrderItems.objects.filter(order = order)
    user = request.user 
    artist = Artist.objects.get(user=user)

    if request.method == 'POST':
        form = UpdateOrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status has been updated successfully.")
            return redirect('artist-dashboard:orders')
    else:
        form = UpdateOrderStatusForm()

    context = {
        'artist':artist,
        'order':order,
        'order_items':order_items,
        'form':form,
    }

    return render(request, "artist-dashboard/order-details.html", context)


def reviews(request):
    user = request.user 
    artist = Artist.objects.get(user=user)

    product_reviews = ProductReview.objects.filter(product__in = artist.product.all())
    artist_reviews = ArtistReview.objects.filter(artist = artist)


    context = {
        'artist':artist,
        'product_reviews':product_reviews,
        'artist_reviews':artist_reviews,
        
    }
    return render(request, "artist-dashboard/reviews.html", context)



def update_profile(request, aid):
    artist = Artist.objects.get(aid=aid)
    reviews = ArtistReview.objects.filter(artist=artist).order_by("-date")


    cover_image_form = CoverImageForm(instance=artist)
    profile_image_form = ProfileImageForm(instance=artist)
    social_media_form = SocialMediaForm(instance=artist)
    artist_info_form = ArtistInfoForm(instance=artist)
    biography_form = BiographyForm(instance=artist)
    description_form = DescriptionForm(instance=artist)
    orientation_form = OrientationForm(instance=artist)
    
    if request.method == 'POST':
            
        if 'cover-photo-name' in request.POST:
            cover_image_form = CoverImageForm(request.POST, request.FILES, instance=artist)
            if cover_image_form.is_valid():
                cover_image_form.save()
                messages.success(request, "Your cover photo has been successfully modified!")
                return redirect('home:artist-details', artist.aid)
        
        elif 'profile-image-name' in request.POST:
            profile_image_form = ProfileImageForm(request.POST, request.FILES, instance=artist)
            if profile_image_form.is_valid():
                profile_image_form.save()
                messages.success(request, "Your profile photo has been successfully modified!")
                return redirect('home:artist-details', artist.aid)

        elif 'social-media-name' in request.POST:
            social_media_form = SocialMediaForm(request.POST, instance=artist)
            if social_media_form.is_valid():
                social_media_form.save()
                messages.success(request, "Your social media links have been successfully modified!")
                return redirect('home:artist-details', artist.aid)
        
        elif 'artist-info-name' in request.POST:
            artist_info_form = ArtistInfoForm(request.POST, instance=artist)
            if artist_info_form.is_valid():
                artist_info_form.save()
                messages.success(request, "Your information have been successfully modified!")
                return redirect('home:artist-details', artist.aid)
        
        elif 'biography-name' in request.POST:
            biography_form = BiographyForm(request.POST, instance=artist)
            if biography_form.is_valid():
                biography_form.save()
                messages.success(request, "Your biography has been successfully modified!")
                return redirect('home:artist-details', artist.aid)

        elif 'description-name' in request.POST:
            description_form = DescriptionForm(request.POST, instance=artist)
            if description_form.is_valid():
                description_form.save()
                messages.success(request, "Your description has successfully modified!")
                return redirect('home:artist-details', artist.aid)
            
        elif 'orientation-name' in request.POST:
            orientation_form = OrientationForm(request.POST, instance=artist)
            if orientation_form.is_valid():
                orientation_form.save()
                messages.success(request, "Your orientation has been successfully modified!")
                return redirect('home:artist-details', artist.aid)
        

    context = {
        'artist': artist,
        'profile_image_form': profile_image_form,
        'cover_image_form': cover_image_form,
        'social_media_form': social_media_form,
        'artist_info_form': artist_info_form,
        'orientation_form': orientation_form,
        'description_form': description_form,
        'biography_form': biography_form,
        'reviews': reviews,
    }

    return render(request, 'artist-dashboard/update-profile.html', context)



def account_details(request):
    user = request.user 
    artist = Artist.objects.get(user=user)


    if request.method == "POST":
        if 'info-name' in request.POST:
            artist.name = request.POST.get("name")
            artist.email = request.POST.get("email")
            user.email = request.POST.get("email")
            artist.address = request.POST.get("address")
            artist.phone = request.POST.get("phone")
            artist.save()
            messages.success(request, "Information updated successfully.")
            return redirect("artist-dashboard:account-details")

        elif 'password-name' in request.POST:
            old_password =  request.POST.get("old_password")
            new_password =  request.POST.get("new_password")
            confirm_new_password =  request.POST.get("confirm_new_password")

            if confirm_new_password != new_password:
                messages.error(request, "New password doesn't match confirm password")
                return redirect("artist-dashboard:account-details")
            
            if check_password(old_password, user.password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password is changed successfully.")
                return redirect("userauths:sign-up")
            
            else:
                messages.error(request, "Old password is incorrect.")
                return redirect("artist-dashboard:account-details")

    context = {
        'artist':artist,
        
    }
    return render(request, "artist-dashboard/account-details.html", context)


