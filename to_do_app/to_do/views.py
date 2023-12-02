from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import RegisterForm, TaskForm
from django.views.generic.list import ListView
from django.views.generic import FormView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import Task

# # Create your views here.


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "to_do/register.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(LoginView):
    template_name = "to_do/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class IndexView(LoginRequiredMixin, ListView):
    login_url = "login"
    context_object_name = "tasks"
    template_name = "to_do/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()
        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect(reverse_lazy('index'))
        else:
            user_tasks = Task.objects.filter(user=request.user)
            return render(request, "to_do/index.html", {"tasks": user_tasks, "form": form})


class RemoveTaskView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, id):
        task = Task.objects.get(id=id)
        task.delete()
        return redirect(reverse_lazy("index"))
