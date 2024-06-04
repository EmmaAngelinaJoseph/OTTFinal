from django.contrib import admin

from .models import UserProfile, Customer, Movies,UserList,Plan

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Movies)
admin.site.register(UserList)
admin.site.register(Plan)