from django import forms
from .models import User, Movies,Plan


class MyLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="password",widget=forms.PasswordInput)
    password2= forms.CharField(label=" Confirm password", widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('username','first_name','email','password')
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('password does not match')
        return cd['password2']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'description', 'genres', 'director', 'main_actor', 'duration', 'image', 'video']
class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['plan_name']  # Assuming 'plan_name' is the only field user selects

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Customer

from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import Customer

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ['username', 'email', 'mobile', 'dob', 'password']
        widgets = {
            'password': forms.PasswordInput(),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email field is required.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile and (not mobile.isdigit() or len(mobile) != 10):
            raise ValidationError("Mobile number must be 10 digits.")
        return mobile

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob:
            age = (datetime.today().date() - dob).days // 365
            if age < 13:
                raise ValidationError("You must be at least 13 years old.")
        return dob

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data
