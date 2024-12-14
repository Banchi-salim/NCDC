from django.utils.timezone import now
from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # New field for image

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class DGPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)  # Excerpt field
    created_at = models.DateTimeField(default=timezone.now)  # Date created
    image = models.ImageField(upload_to='dg_blog_images/', blank=True, null=True)  # Optional image field

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class HeadOfDepartment(models.Model):
    name = models.CharField(max_length=100)
    department_name = models.CharField(max_length=100)  # Explicitly store department name
    image = models.ImageField(upload_to='hod_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="departments/", blank=True, null=True)
    description = models.TextField()
    head_of_department = models.OneToOneField(
        HeadOfDepartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="department"
    )

    def __str__(self):
        return self.name


class LocalGovernmentArea(models.Model):
    name = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name}, {self.state}"


class Events(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now().time())
    image = models.ImageField(upload_to='events_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.title}"


class DiseaseAlert(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_issued = models.DateField(auto_now_add=True)
    lga = models.ForeignKey(LocalGovernmentArea, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Donation(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation from {self.name} - {self.amount} NGN"


class Report_disease_weekly(models.Model):
    name = models.CharField(max_length=100)
    points = models.TextField(help_text="Key points about the disease")
    image = models.ImageField(upload_to='disease_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Weekly_Epidemiological_Report(models.Model):
    year = models.PositiveIntegerField()
    month = models.CharField(max_length=20)
    week = models.PositiveIntegerField()
    summary = models.TextField()
    diseases = models.ManyToManyField(Report_disease_weekly, related_name='reports')

    def __str__(self):
        return f"Week {self.week} of {self.month}, {self.year}"


class Situation_Report(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class SituationReportFile(models.Model):
    situation_report = models.ForeignKey(Situation_Report, on_delete=models.CASCADE, related_name="reports")
    pdf_file = models.FileField(upload_to="reports/")
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.situation_report.title} - {self.pdf_file.name}"


class ProjectReport(models.Model):
    file_name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='project_reports/')

    def __str__(self):
        return self.file_name


class AnnualReport(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='annual_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Guideline(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class GuidelineFile(models.Model):
    guideline = models.ForeignKey(Guideline, related_name='files', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='guidelines/')

    def __str__(self):
        return self.file_name


class EstablishmentDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='establishment_documents/')

    def __str__(self):
        return self.title


class ResearchWork(models.Model):
    title = models.CharField(max_length=255)
    authors = models.TextField()
    abstract = models.TextField()
    article_url = models.URLField()
    date = models.DateField()

    def __str__(self):
        return self.title


class StateIncidentActionPlan(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='incident_action_plans/')
    upload_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Disease(models.Model):
    name = models.CharField(max_length=255)
    background = models.TextField()
    transmission = models.TextField()
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatments = models.TextField()

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='project_images/')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_created']


class SecurityRiskDocument(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='security_risk_documents/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Job(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ChatMessage(models.Model):
    user = models.CharField(max_length=100, blank=True)  # Visitor or staff/admin name
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )  # For threaded replies

    def __str__(self):
        return f"{self.user}: {self.message[:50]}"

    @staticmethod
    def clear_old_messages():
        """Clear messages older than 24 hours."""
        ChatMessage.objects.filter(timestamp__lt=now() - timedelta(hours=24)).delete()


class Department_Project(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='department_project/', null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Department_Research(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='Department_research/', null=True)
    uploaded_at = models.DateTimeField(default=timezone.now)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class FinanceTransactionDocument(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to="transaction_documents/")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Advisory_Note(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='Advisory_Note/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

