from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation
from .forms import LoginForm, RegisterForm
from .models import Profile 
from .forms import ProfileForm

def user_list(request):
    users = User.objects.all()
    
    return render(request, 'users/list.html', {'users': users})

    return redirect('home')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            return render(
                request,
                'users/login.html',
                {
                    'error': 'Nom utilisateur ou mot de passe incorrect'
                }
            )

    return render(
        request,
        'users/login.html'
    )
def logout_view(request):

    logout(request)

    return redirect('/')


def register_view(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    return render(
        request,
        'users/register.html',
        {'form': form}
    )


def home(request):
    return render(request,'cars/home.html')



@login_required
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    reservations = Reservation.objects.filter(
        user=request.user
    )

    return render(
        request,
        'users/profile.html',
        {
            'profile': profile,
            'reservations': reservations,
        }
    )

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'users/edit_profile.html',
        {
            'form': form
        }
    )