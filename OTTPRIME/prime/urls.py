
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import adminindex, register, customer_list, movie_list, upload_movie, delete_movie, toggle_disable_movie, \
    base, custom_login, signup, plans, signup_success_view, movies, custom_logout, select_plan, \
    payment_details, payment_success,movie_detail,GenreMoviesView,search_movies,add_to_list

urlpatterns = [
    path('registration/register',register,name='register'),
    path('Emma/', LoginView.as_view(), name='adminlogin'),
    path('logoutadmin/', LogoutView.as_view(), name='logoutadmin'),
    path('customer_list/', customer_list, name='customer_list'),
    path('movie_list/', movie_list, name='movie_list'),
    path('delete_movie/<int:id>/', delete_movie, name='delete_movie'),
    path('toggle_disable_movie/<int:id>/', toggle_disable_movie, name='toggle_disable_movie'),
    path('upload_movie/', upload_movie, name='upload_movie'),
    path('adminbase/', adminindex, name='adminindex'),
    path('',base,name='base'),
    path('login/', custom_login, name='userlogin'),
    
    path('signup/', signup, name='signup'),
    path('cards/',plans,name='cards'),
    path('signup/success/', signup_success_view, name='signup_success'),
    path('movies/<int:id>/', movie_detail, name='movie_detail'),
    path('movies/', movies, name='movies'),
      path('select_plan/<str:plan_name>/', select_plan, name='select_plan'),
    path('payment_details/', payment_details, name='payment_details'),
   
    path('genre/<str:genre>/', GenreMoviesView.as_view(), name='genre_movies'),
    path('add-to-list/<int:movie_id>/', add_to_list, name='add_to_list'),
    path('search/', search_movies, name='search_movies'),
    path('logout/',custom_logout,name='logout')
]