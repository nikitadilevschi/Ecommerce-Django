from django.shortcuts import render

# Create your views here.


def login(request):

    context = {
        'title': 'Login',
        'heading': 'Login',
        'subheading': 'Login to your account',
        'form': 'login',
    }
    return render(request, 'users/login.html', context)


def registration(request):
    context = {
        'title': 'Login',
        'heading': 'Login',
        'subheading': 'Login to your account',
        'form': 'login',
    }
    return render(request, 'users/registration.html', context)


def profile(request):
    context = {
        'title': 'Login',
        'heading': 'Login',
        'subheading': 'Login to your account',
        'form': 'login',
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    ...