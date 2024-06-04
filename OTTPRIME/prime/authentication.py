from django.contrib.auth.hashers import check_password
from .models import Customer

def authenticate_customer(email, password):
    try:
        user = Customer.objects.get(email=email)
        if check_password(password, user.password):
            return user
    except Customer.DoesNotExist:
        return None