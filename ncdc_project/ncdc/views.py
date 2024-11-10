from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'ncdc/index.html')

def about(request):
    return render(request, 'ncdc/about.html')