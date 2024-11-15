from django.shortcuts import render
from .models import Blog, Department, HeadOfDepartment
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .secrets import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


#@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            # Parse incoming request data
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "I didn't catch that. Could you rephrase your question?"}, status=400)

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a health assistant chatbot for the NCDC. Provide clear and concise answers to health-related questions."},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = response.choices[0].message['content']
            return JsonResponse({"reply": reply}, status=200)

        except openai.error.OpenAIError as e:
            # Handle OpenAI API errors
            return JsonResponse({"reply": "I'm having trouble connecting to the AI server. Please try again later."}, status=500)

        except json.JSONDecodeError:
            # Handle JSON parsing errors
            return JsonResponse({"reply": "Invalid input. Please send a valid JSON request."}, status=400)

        except Exception as e:
            # Log unexpected errors for debugging
            print(f"Unexpected error: {e}")
            return JsonResponse({"reply": "An error occurred. Please try again later."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


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
