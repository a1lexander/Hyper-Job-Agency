from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from django.core.exceptions import PermissionDenied

from .models import Resume


# Create your views here.
class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/base.html')


class ResumeListView(ListView):
    model = Resume
    context_object_name = 'resume_list'
    template_name = 'resume/resume_list.html'


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'resume/signup.html'


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'resume/login.html'


class ResumeVacancy(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/home.html')


class CreateResumeView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            return render(request, 'resume/create_resume.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            description = request.POST.get('description')
            r = Resume.objects.create(description=description, author=request.user)
            r.save()
            return redirect('/home')
