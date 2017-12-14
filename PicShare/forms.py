from django import forms
from models import Picture, PicShurUser


class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = (
            'caption',
            'description',
            'image'
        )


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = PicShurUser
        fields = (
            'username',
            'password',
            'first_name',
            'profile_pic',
            'last_name',
            'email'
        )