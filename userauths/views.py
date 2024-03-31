from django.shortcuts import render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
# from userauths.models import User

User = settings.AUTH_USER_MODEL

def register_view(request):
    
    if request.method == "POST": 
        form = UserRegisterForm(request.POST or None)
    
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username") 
            messages.success(request,"Welcome {username} ! Your account has been created successfully.")
            new_user = authenticate(username = form.cleaned_data.get('email'), password = form.cleaned_data.get('password1'))
            login(request,new_user) 
            return redirect("home:index")

    else:
        form = UserRegisterForm()
    context = { 
        'form':form
    }
    return render(request,"userauths/sign-up.html",context)



def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.object.get(email=email)
        except:
            messages.warning(request,f"No user with {email} exists. Try again?")
    user = authenticate(request,email=email,password=password)

    if user is not None:
            login(request,user)
            messages.success(request,"Success! You are logged in.")
            return redirect("home:index")
    else:
        messages.warning(request,"User does not exist. Try signing up?")
    
    return render(request,"userauths/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You logged out successfully. See you next time!")
    return redirect("userauths:login")


