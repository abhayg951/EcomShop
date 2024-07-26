from django.urls import path
from . import views
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup', views.signup, name='signup'), 
    path('login', views.sign_in, name='login'),
    path("logout", views.logout_user, name="logout")
]

