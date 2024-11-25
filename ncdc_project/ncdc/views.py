import json

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body.decode('utf-8'))
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"error": "Message is empty or missing"}, status=400)

            # Rasa server endpoint
            rasa_url = "http://localhost:5005/webhooks/rest/webhook"

            # Send the user message to Rasa server
            payload = {"sender": "user", "message": user_message}
            headers = {"Content-Type": "application/json"}
            response = requests.post(rasa_url, json=payload, headers=headers)

            # Check Rasa server response
            if response.status_code == 200:
                reply = response.json()

                # Log full response for debugging (optional)
                print("Rasa Response:", reply)

                if reply and isinstance(reply, list) and len(reply) > 0:
                    bot_reply = reply[0].get("text", "Sorry, I couldn't understand that.")
                    return JsonResponse({"reply": bot_reply}, status=200)
                else:
                    return JsonResponse({"reply": "Sorry, I couldn't understand that."}, status=200)
            else:
                # Log the error details for debugging
                print("Rasa Server Error:", response.text)
                return JsonResponse(
                    {
                        "error": "Rasa server error",
                        "details": response.text,
                        "status_code": response.status_code,
                    },
                    status=500,
                )
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format in request body", "details": str(e)}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": "Failed to connect to Rasa server", "details": str(e)}, status=500)
        except Exception as e:
            return JsonResponse({"error": "Unexpected server error", "details": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


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


def update_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Logic to check if there's an outbreak near the user's location
        nearby_alert = DiseaseAlert.objects.filter(
            latitude__range=(latitude - 0.5, latitude + 0.5),
            longitude__range=(longitude - 0.5, longitude + 0.5)
        ).first()

        if nearby_alert:
            return JsonResponse({"alert": f"Outbreak Alert: {nearby_alert.title}"})

        return JsonResponse({"alert": None})

    return JsonResponse({"error": "Invalid request method."}, status=400)


def process_donation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            transaction_id = data.get("transaction_id")
            name = data.get("name")
            email = data.get("email")
            amount = data.get("amount")

            if not (transaction_id and name and email and amount):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Save the donation details
            donation = Donation.objects.create(
                name=name,
                email=email,
                amount=amount,
                transaction_id=transaction_id,
                status="Success",
            )
            return JsonResponse({"message": "Donation processed successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def donate_page(request):
    return render(request, "ncdc/donate.html")