from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.user_logout, name="logout"),
    path("remove/<int:id>",  views.remove_task, name="remove"),
    path("", views.IndexView.as_view(), name="index"),
]
