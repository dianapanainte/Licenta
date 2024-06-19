from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_required(views.dashboard_view), name='dashboard'),
    path('favourites/', login_required(views.favourites_view), name='favourites'),
    path('add_favourite/', login_required(views.add_favourite_view), name='add_favourite'),
    path('account/', login_required(views.account_view), name='account'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('password_change/',
         login_required(auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html')),
         name='password_change'),
    path('password_change/done/', login_required(
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')),
         name='password_change_done'),
    path('delete_account/', login_required(views.delete_own_account_view), name='delete_own_account'),
    path('account_deleted/', login_required(views.account_deleted_view), name='account_deleted'),
    path('login_first/', views.login_first_view, name='login_first'),
]
