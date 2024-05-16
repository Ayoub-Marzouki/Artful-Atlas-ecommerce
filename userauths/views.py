from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

from home.models import Profile, Artist

User = settings.AUTH_USER_MODEL

def register_view(request):
    next_page = request.GET.get('next')  
    
    if request.method == "POST": 
        form = UserRegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save()
            
            Profile.objects.create(user=new_user)

            username = form.cleaned_data.get("username") 

            if new_user.user_type == 'artist':
                Artist.objects.create(user=new_user, name=new_user.username)
            
            messages.success(request, f"Welcome {username}! Your account has been created successfully.")
            
            new_user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))

            login(request, new_user) 
            if next_page:
                return redirect(next_page)
            else:
                return redirect("home:index")
            
        else:   
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    
    else:
        form = UserRegisterForm()
 
    context = { 
        'form': form,
        "next_page":next_page,
    }
    return render(request, "userauths/sign-up.html", context)




def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:index")

    next_page = request.GET.get('next')  # Get the value of 'next' parameter

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Success! You are logged in.")
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect("home:index")
            else:
                messages.warning(request, "User does not exist. Try signing up?")
                
        except User.ObjectDoesNotExist:
            messages.warning(request, f"No user with {email} exists. Try again?")
            
    context = {
        'next_page':next_page,
    }
    return render(request, "userauths/login.html", context)



def logout_view(request):
    logout(request)
    messages.success(request, "You logged out successfully. See you next time!")
    return redirect("userauths:login")


