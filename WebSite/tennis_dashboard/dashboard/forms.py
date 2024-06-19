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
        user = kwargs.pop('user', None)
        super(FavoriteForm, self).__init__(*args, **kwargs)
        if user is not None:
            favorited_players = UserFavorite.objects.filter(user=user).values_list('player__player_id', flat=True)
            self.fields['player'].queryset = Player.objects.exclude(player_id__in=favorited_players).order_by('name')
        self.fields['player'].label = "Select Player to Add to Favorites\n"
