
from django.contrib.auth.models import User


# Create your models here.
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()



class Customer(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    password=models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.email
        

class UserProfile(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    subscription_plan = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    action = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.subscription_plan
class Movies(models.Model):
        title = models.CharField(max_length=150, unique=True)
        description = models.TextField(blank=True, null=True)
        genres = models.CharField(max_length=100, blank=True, null=True)
        director = models.CharField(max_length=100, blank=True, null=True)
        main_actor = models.CharField(max_length=100, blank=True, null=True)
        duration = models.IntegerField(blank=True, null=True)  # Duration in minutes
        image = models.ImageField(upload_to='movie/images/', blank=True, null=True)
        video = models.FileField(upload_to='movie/videos/', blank=True, null=True)
        Languages = models.CharField(max_length=150,blank=True)
        disabled = models.BooleanField(default=False)

        def __str__(self):
            return self.title
        
class UserList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movies, related_name='user_lists') 
class Plan(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic Plan'),
        ('Standard', 'Standard Plan'),
        ('Premium', 'Premium Plan')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=10, choices=PLAN_CHOICES)
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.plan_name}"