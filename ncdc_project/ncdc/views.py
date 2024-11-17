import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Blog, Department, HeadOfDepartment
from django.http import JsonResponse
import json


@csrf_exempt  # Ensure you have CSRF protection in production; this is for testing
def chatbot_api(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"error": "Message is empty"}, status=400)

            # Rasa server endpoint
            rasa_url = "http://localhost:5005/webhooks/rest/webhook"

            # Send the user message to Rasa server
            response = requests.post(rasa_url, json={"sender": "user", "message": user_message})

            if response.status_code == 200:
                reply = response.json()
                if reply and len(reply) > 0:
                    return JsonResponse({"reply": reply[0].get("text", "Sorry, I didn't understand that.")})
                else:
                    return JsonResponse({"reply": "Sorry, I didn't understand that."})
            else:
                return JsonResponse({"error": "Rasa server error", "details": response.text}, status=500)
        except Exception as e:
            return JsonResponse({"error": "Server error", "details": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)

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
    return render(request, 'ncdc/dg.html', {'blogs': blogs})
