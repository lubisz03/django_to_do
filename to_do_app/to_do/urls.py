from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(next_page="login"), name="logout"),
    path("remove/<int:id>",  views.RemoveTaskView.as_view(), name="remove"),
    path("", views.IndexView.as_view(), name="index"),
]
