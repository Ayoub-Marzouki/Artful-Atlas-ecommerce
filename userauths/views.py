from django.shortcuts import render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings

User = settings.AUTH_USER_MODEL

def register_view(request):
    
    if request.method == "POST": 
        form = UserRegisterForm(request.POST or None)
    
        if form.is_valid(): # cleaned means validated
            new_user = form.save()
            username = form.cleaned_data.get("username") 
            # or form.cleaned_data["username"] but .get() is better; it avoids key errors in case the field is missing
            messages.success(request,"Welcome {username} ! Your account has been created successfully.") #Just a simple message to confirm the success
            new_user = authenticate(username = form.cleaned_data.get('email'), password = form.cleaned_data.get('password1'))
            # password1 is a name convetion kanden
            login(request,new_user) # to log the user in
            return redirect("home:index") # redirect him to home page

    else:
        form = UserRegisterForm()
    context = { 
        'form':form
    }
    return render(request,"userauths/sign-up.html",context)



def login_view(request):
    # If the user is already logged in, simply redirect him to home page instead of making him log in again :
    if request.user.is_authenticated:
        return redirect("home:index")
    
    # We need to check if the user that's attempting to log in has already signed up. If so, then we'll simply check if the data he entered when trying to log in matches an existing data in our database.
    if request.method == "POST":
        # We'll be working with the usual html forms and inputs instead of django forms
        email = request.POST.get("email")
        # The line above will look for input tag whose name is "email" and store it in our variable called email. Same for the next line
        password = request.POST.get("password")

        try: # object.all() can be used to retrieve all data from database
            # In this case we only need to check if data match for 1 user, for example we chose to check if the emails match
            user = User.object.get(email=email)
            # User is the class we created earlier, .objects allows us to access its fields, .get to get one of the fields we choose, in this case "email"
        
        except: # f in there stands for formatted strings; mandatory when working with variables, try deleting it and the variable will turn red (error)
            messages.warning(request,f"No user with {email} exists. Try again?")
        # Now we'll log the user in, if the email and password match
        user = authenticate(request,email=email,password=password)

        if user is not None: # If there's a user, then :
            login(request,user)
            messages.success(request,"Success! You are logged in.")
            return redirect("home:index")
        else:
            messages.warning(request,"User does not exist. Try signing up?")
    
    return render(request,"userauths/login.html")


