from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import RegisterForm, TaskForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

# # Create your views here.


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'to_do/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('index'))

        return render(request, 'to_do/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'to_do/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('index'))

        return render(request, 'to_do/login.html', {'form': form})


class IndexView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request):
        form = TaskForm()
        user_tasks = Task.objects.filter(user=request.user)
        return render(request, "to_do/index.html", {"tasks": user_tasks, "form": form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse('index'))
        else:
            user_tasks = Task.objects.filter(user=request.user)
            return render(request, "to_do/index.html", {"tasks": user_tasks, "form": form})


def user_logout(request):
    logout(request)
    return redirect(reverse("login"))


def remove_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect(reverse("index"))
