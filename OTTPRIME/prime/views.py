from django.db.models import Q
from django.forms import models
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from .forms import MyLoginForm, UserRegisterForm, MovieForm
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import UserProfile,  Movies,UserList
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages



# from .models import UserProfile


# Create your views here.
def adminindex(request):
    return render(request, 'adminbase.html')

def user_login(request):
    if request.method == 'POST':
        login_form = MyLoginForm(request.POST)
        if login_form.is_valid():
            cleaned_data = login_form.cleaned_data
            auth_user = authenticate(request, username=cleaned_data['username'],
                                     password=cleaned_data['password'])
            if auth_user is not None:
                login(request, auth_user)
                return HttpResponse('Authenticated')
    else:
        login_form = MyLoginForm()
    return render(request, 'useraccount/login_form.html',
                  {'login_form': login_form})
def register(request):
    if request.method=='POST':
        user_reg_form=UserRegisterForm(request.POST)
        if user_reg_form.is_valid():
            new_user=user_reg_form.save(commit=False)
            new_user.set_password(user_reg_form.cleaned_data['password'])
            new_user.save()
            return render(request,'registration/register_done.html',{'user_reg_form':user_reg_form})
    else:
        user_reg_form=UserRegisterForm()
    return render (request,'registration/register.html',
                   {'user_reg_form':user_reg_form})
# views.py


def customer_list(request):
    query = request.GET.get('q')
    if query:
        users = UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__mobile__icontains=query)
        )
    else:
        users = UserProfile.objects.all()
    return render(request, 'customer_list.html', {'users': users})
def movie_list(request):
    query = request.GET.get('q')
    if query:
        movies_list = Movies.objects.filter(
            Q(title__icontains=query) |
            Q(main_actor__icontains=query) |
            Q(director__icontains=query)
        )
    else:
        movies_list = Movies.objects.all()
    return render(request, 'movie_list.html', {'movies': movies_list})
def upload_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'upload_movie.html', {'form': form})

def delete_movie(request, id):
    movie = get_object_or_404(Movies, id=id)
    if request.method == 'DELETE':
        movie.delete()
        return JsonResponse({'message': 'Movie deleted successfully.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def toggle_disable_movie(request, id):
    movie = get_object_or_404(Movies, id=id)
    if request.method == 'POST':
        movie.disabled = not movie.disabled
        movie.save()
        return JsonResponse({'message': 'Movie status updated successfully.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
class GenreMoviesView(View):
    def get(self, request, genre):
        movies = Movies.objects.filter(genres__icontains=genre)
        return render(request, 'genre_movies.html', {'movies': movies, 'genre': genre})
    
def search_movies(request):
    query = request.GET.get('query', '')
    if query:
        movies = Movies.objects.filter(
            Q(title__icontains=query) | 
            Q(main_actor__icontains=query) | 
            Q(director__icontains=query) |
             Q(Languages__icontains=query)
        )
    else:
        movies = Movies.objects.all()
    
    return render(request, 'search_results.html', {'movies': movies, 'query': query})


@login_required(login_url='userlogin')
def add_to_list(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    user = request.user

    if not user.is_authenticated:
        return redirect('userlogin')

    user_list, created = UserList.objects.get_or_create(user=user)
    user_list.movies.add(movie)
    return redirect('movies')

from cProfile import Profile

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import SignupForm
from .authentication import authenticate_customer

# Create your views here.
def base(request):
    return render(request,'base.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate_customer(email, password)  # Use the custom authentication function

        if user is not None:
            # Manually create the session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.username
            # Optionally set the session expiry
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)

            messages.success(request, f'Welcome {user.username}')
            return redirect('base')  # Redirect to a homepage or dashboard
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'registration/userlogin.html')


def custom_logout(request):
    request.session.flush()  # Clear the session
    return redirect('base')

from django.shortcuts import render

def signup_success_view(request):
    return render(request, 'signup_success.html')


def movies(request):
    query = request.GET.get('q')
    if query:
        movies_list = Movies.objects.filter(
            Q(title__icontains=query) |
            Q(main_actor__icontains=query) |
            Q(director__icontains=query)
        )
    else:
        movies_list = Movies.objects.all()
    return render(request, 'movies.html', {'movies': movies_list})
def movie_detail(request, id):
    movie = get_object_or_404(Movies, id=id)
    return render(request, 'movie_detail.html', {'movie': movie})




  
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
# from .forms import SignupForm, MyLoginForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.password = make_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Signup successful!')
            return render(request, 'registration/signup_success.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def plans(request):
    return render(request, 'cards.html')
# views.py
from django.shortcuts import render, redirect

# def select_plan(request, plan_name):
#     # Store the selected plan in the session or pass it to the template
#     request.session['selected_plan'] = plan_name
#     return redirect('payment')


from django.shortcuts import render, redirect

def select_plan(request, plan_name):
    # You might want to save the selected plan to the session or handle it in some other way
    request.session['selected_plan'] = plan_name
    return redirect('payment_details')

def payment_details(request):
    if request.method == 'POST':
        # Process payment details here
        # After processing, redirect to success page
        return redirect('payment_details')
    return render(request, 'payment.html')

def payment_success(request):
    return render(request, 'payment_success.html')






