from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import CustomUserForm

# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # TODO: Redirect to the dashboard page
            return redirect('index')
    else:
        form = CustomUserForm()

    context = {
        'form': form
    }
        
    return render(request, 'signup.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)  

        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('index')