import json
from django.core.mail import send_mail
import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
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


def get_user_lga(latitude, longitude):
    """
    Function to find the LGA based on user's latitude and longitude.
    Assumes LocalGovernmentArea model has latitude and longitude ranges defined.
    """
    return LocalGovernmentArea.objects.filter(
        latitude_min__lte=latitude,
        latitude_max__gte=latitude,
        longitude_min__lte=longitude,
        longitude_max__gte=longitude
    ).first()

def update_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Determine the user's LGA
        user_lga = get_user_lga(latitude, longitude)

        if user_lga:
            # Fetch any active disease alerts for the user's LGA
            disease_alerts = DiseaseAlert.objects.filter(lga=user_lga)
            if disease_alerts.exists():
                alerts = [alert.title for alert in disease_alerts]
                return JsonResponse({"alert": f"Disease Outbreaks in {user_lga.name}: {', '.join(alerts)}"})
            else:
                return JsonResponse({"alert": f"No disease outbreaks reported in {user_lga.name}."})

        return JsonResponse({"alert": "Unable to determine your local government area."})

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


def weekly_reports(request):
    # Fetch all reports from the database
    reports = Weekly_Epidemiological_Report.objects.prefetch_related('diseases').order_by('-year', '-month', '-week')

    # Generate filter options dynamically
    years = sorted(set(report.year for report in reports))
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    weeks = ["1", "2", "3", "4"]

    context = {
        "reports": reports,
        "years": years,
        "months": months,
        "weeks": weeks,
    }
    return render(request, "ncdc/Weekly_Epidemiological_Report.html", context)


def situation_report_list(request):
    reports = Situation_Report.objects.all()
    print(reports)
    return render(request, 'ncdc/situation_report.html', {'reports': reports})


def situation_report_details(request, report_id):
    situation_report = get_object_or_404(Situation_Report, id=report_id)
    reports = situation_report.reports.all()
    return render(
        request,
        "ncdc/situation_report_details.html",
        {"situation_report": situation_report, "reports": reports},
    )


def project_reports(request):
    reports = ProjectReport.objects.all()
    return render(request, 'ncdc/project_reports.html', {'reports': reports})


def annual_reports(request):
    reports = AnnualReport.objects.all().order_by('-uploaded_at')
    return render(request, 'ncdc/Annual_Report.html', {'reports': reports})


def guidelines_list(request):
    guidelines = Guideline.objects.all()
    return render(request, 'ncdc/guidelines.html', {'guidelines': guidelines})


def guideline_files(request, pk):
    guideline = get_object_or_404(Guideline, pk=pk)
    files = [{'name': f.file_name, 'url': f.pdf_file.url} for f in guideline.files.all()]
    return JsonResponse({'files': files})


def establishment_documents_list(request):
    documents = EstablishmentDocument.objects.all()
    return render(request, 'ncdc/establishment.html', {'documents': documents})


def research_list(request):
    research_works = ResearchWork.objects.all().order_by('-date')
    return render(request, 'ncdc/research_list.html', {'research_works': research_works})


def state_incident_action_plans(request):
    plans = StateIncidentActionPlan.objects.all().order_by('-upload_date')
    return render(request, 'ncdc/state_incident_action_plans.html', {'plans': plans})


def disease_list(request):
    # Get the filter parameter (e.g., A, B, C, or 'All')
    filter_letter = request.GET.get('filter', 'All')

    if filter_letter == 'All':
        diseases = Disease.objects.order_by('name')  # Fetch all diseases sorted by name
    else:
        diseases = Disease.objects.filter(name__istartswith=filter_letter).order_by('name')

    return render(request, 'ncdc/disease_list.html', {
        'diseases': diseases,
        'filter_letter': filter_letter,
    })


def news_home(request):
    blog_posts = Blog.objects.order_by('-created_at')[:6]
    dg_posts = DGPost.objects.order_by('-created_at')[:6]
    return render(request, 'ncdc/news_home.html', {'blog_posts': blog_posts, 'dg_posts': dg_posts})


def blog_posts_list(request):
    blog_posts = Blog.objects.order_by('-created_at')
    return render(request, 'ncdc/blog_posts_list.html', {'posts': blog_posts, 'title': "All Blog Posts"})


def dg_posts_list(request):
    dg_posts = DGPost.objects.order_by('-created_at')
    return render(request, 'ncdc/dg_posts_list.html', {'posts': dg_posts, 'title': "DG's Blog Posts"})


def training_nfetp(request):
    return render(request, 'ncdc/nfetp.html')


def internship_view(request):
    return render(request, 'ncdc/internship.html')


def ncdc_tour_view(request):
    return render(request, 'ncdc/tour.html')


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'ncdc/projects.html', {'projects': projects})


def security_risk_list(request):
    documents = SecurityRiskDocument.objects.all().order_by('-date_uploaded')
    return render(request, 'ncdc/security_risk_list.html', {'documents': documents})


def jobs_list(request):
    jobs = Job.objects.all()
    return render(request, 'ncdc/jobs.html', {'jobs': jobs})


def contact_page(request):
    return render(request, 'ncdc/contact.html')


def chat_room(request):
    """Renders the chat room page."""
    messages = ChatMessage.objects.order_by('-timestamp')[:50]  # Load recent 50 messages
    return render(request, 'ncdc/chat_room.html', {'messages': messages})

@csrf_exempt
def post_message(request):
    """Handles new chat messages."""
    if request.method == "POST":
        data = json.loads(request.body)
        user = data.get('user', 'Visitor')
        message = data.get('message', '')
        reply_to_id = data.get('reply_to')

        # Check if the user is authenticated (logged in admin)
        if request.user.is_authenticated:
            user = request.user.username  # Use the logged-in admin's username

        if message:
            # Check for parent message if it's a reply
            parent_message = ChatMessage.objects.filter(id=reply_to_id).first() if reply_to_id else None

            # Create a new message in the database
            new_message = ChatMessage.objects.create(user=user, message=message, reply_to=parent_message)

            # Notify the original message poster (if it's a reply and email exists)
            if parent_message and '@' in parent_message.user:  # Assuming email-like user input
                try:
                    send_mail(
                        subject=f"Reply to your message on NCDC Chat Room",
                        message=f"Hi {parent_message.user},\n\n"
                                f"{user} has replied to your message:\n\n"
                                f"\"{parent_message.message}\"\n\n"
                                f"Reply:\n\"{message}\"\n\n"
                                f"Visit the chat room for more details.",
                        from_email='no-reply@ncdc.gov.ng',
                        recipient_list=[parent_message.user],
                        fail_silently=True
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")

            # Notify admin or staff of new messages
            if not reply_to_id:  # Notify only for new (non-reply) messages
                notify_admin_or_staff(user, message)

            return JsonResponse({'status': 'success', 'message': 'Message posted!', 'message_id': new_message.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


from django.core.mail import send_mail
from django.core.mail import EmailMessage
import logging

logger = logging.getLogger(__name__)

def notify_admin_or_staff(user, message):
    """Notify admin/staff about a new message."""
    try:
        send_mail(
            subject='New Message in NCDC Chat Room',
            message=f'{user} sent a new message: "{message}"',
            from_email='iabdulsalim40@gmail.com',  # Replace with your email
            recipient_list=['usmanabdulsalim@gmail.com', 'mouhdbuharii@gmail.com'],  # Replace with admin email(s)
            fail_silently=False,  # Use False for debugging
        )
        logger.info(f"Notification sent to admin successfully.")
    except Exception as e:
        logger.error(f"Error sending notification to admin: {e}")
