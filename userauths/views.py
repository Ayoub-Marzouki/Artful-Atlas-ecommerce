from django.shortcuts import render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import redirect

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