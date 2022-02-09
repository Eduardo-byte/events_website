from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, UserPasswordResetForm
from events .forms import MyClubUserForm

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


def login_user(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        user_check = get_user_model().objects.filter(username=username).first()
        if user is not None:
            login(request, user)
            return redirect('home')            
        else:
            if user_check is None:
                messages.success(request, ("Username not registered"))
                return redirect('login')
            elif not user_check.is_active:
                messages.success(request, ("User not active"))
                return redirect('login')
            else:
                messages.success(request, ("incorrect password"))
                return redirect('login')
            # Return an 'invalid login' error message.
            #messages.success(request, ("There was an error logging in, Try again... "))
            #return redirect('login')  
        
    else:
        return render(request, 
            'authenticate/login.html', 
            {
                
            })
        
def logout_user(request):
    logout(request)
    messages.success(request, (" You were logged out "))
    return redirect('home')
    # return render(request, 
    #     'authenticate/login.html', 
    #     {
                
    #     })
    

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        myclub = MyClubUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, (" Registered successfull "))
            myclub.username = form.cleaned_data['username']
            myclub.first_name = form.cleaned_data['first_name']
            myclub.last_name = form.cleaned_data['last_name']
            myclub.email = form.cleaned_data['email']
            myclub.password1 = form.cleaned_data['password1']
            myclub.password2 = form.cleaned_data['password2']
            stock = myclub.save(commit=False)
            stock.id = 1
            stock.save()
            
            return redirect('home')
    else:
        form = RegisterUserForm()
        
    return render(request, 
    'authenticate/register.html', 
        {
        'form':form     
        })
    
def change_password(request):
    if request.method == 'POST':
        form = UserPasswordResetForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        
    else:
        form = UserPasswordResetForm(request.user)
    return render(request, 'authenticate/change_password.html', {
        'form': form
    })

