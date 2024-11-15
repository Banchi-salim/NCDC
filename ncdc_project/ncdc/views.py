from django.shortcuts import render
from .models import Blog, Department, HeadOfDepartment
import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

openai.api_key = settings.OPENAI_API_KEY


@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a health assistant chatbot for the NCDC."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message['content']
        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid request method."}, status=400)


# Create your views here.
def index(request):
    return render(request, 'ncdc/index.html')


def about(request):
    blogs = Blog.objects.all()[:3]
    return render(request, 'ncdc/about.html', {'blogs': blogs})


def deparments(request):
    departments = Department.objects.all()
    return render(request, 'ncdc/departments.html', {'departments': departments})


def heads_of_departments(request):
    hods = HeadOfDepartment.objects.all()
    return render(request, 'ncdc/leadership.html', {'hods': hods})


def office_of_dg(request):
    blogs = Blog.objects.all()[:3]
    return render(request, 'ncdc/dg.html', {'blogs':blogs})
