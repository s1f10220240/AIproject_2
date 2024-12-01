from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ImageUpload
from django.contrib.auth.models import User


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']  # アップロードするフィールド


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']