from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player, UserFavorite


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['player']

    def __init__(self, *args, **kwargs):
        super(FavoriteForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.order_by('name')
        self.fields['player'].label = "Select Player to add to Favourites:\n"
