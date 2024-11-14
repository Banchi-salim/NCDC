from django.shortcuts import render
from .models import Blog


# Create your views here.
def index(request):
    return render(request, 'ncdc/index.html')


def about(request):
    blogs = Blog.objects.all()[:3]
    return render(request, 'ncdc/about.html', {'blogs': blogs})


def deparments(request):
    return render(request, 'ncdc/departments.html')


def leadership(request):
    return render(request, 'leadership.html')


def office_of_dg(request):
    return render(request, 'office_of_dg.html')
