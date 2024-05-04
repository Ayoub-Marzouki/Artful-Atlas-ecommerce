from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings

from home.models import Profile

User = settings.AUTH_USER_MODEL

def register_view(request):
    next_page = request.GET.get('next')  # Get the value of 'next' parameter
    # Check if the request method is POST
    if request.method == "POST": 
        # Create a form instance with the data from the POST request
        form = UserRegisterForm(request.POST or None)

        # Check if the form data is valid
        if form.is_valid():
            # Save the form data to create a new user
            new_user = form.save()
            # Create a profile instance for the new user
            Profile.objects.create(user=new_user)
            # Get the username from the form data
            username = form.cleaned_data.get("username") 
            # Display a success message indicating that the account was created
            messages.success(request, f"Welcome {username}! Your account has been created successfully.")
            # Authenticate the new user
            new_user = authenticate(username=form.cleaned_data.get('email'), password=form.cleaned_data.get('password1'))
            # Log in the new user
            login(request, new_user) 
            if next_page:
                return redirect(next_page)
            else:
                return redirect("home:index")
        else:
            # If form validation fails, loop through form errors and display error messages
            for field, errors in form.errors.items():
                for error in errors:
                    # Display error messages for each field
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        # If the request method is not POST, create an empty form instance
        form = UserRegisterForm()
    
    # Prepare the form context to pass to the template
    context = { 
        'form': form,
        "next_page":next_page,
    }
    # Render the sign-up page with the form context
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


