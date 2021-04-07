from django.shortcuts import render, redirect
from django.views.generic import ListView


from django.views import View
from django.core.exceptions import PermissionDenied

from .models import Vacancy


# Create your views here.

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy/vacancy_list.html'
    context_object_name = 'vacancy_list'


class CreateVacancyView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_staff:
            raise PermissionDenied
        else:
            return render(request, 'vacancy/create_vacancy.html')

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        else:
            description = request.POST.get('description')
            v = Vacancy.objects.create(description=description, author=request.user)
            v.save()
            return redirect('/home')
