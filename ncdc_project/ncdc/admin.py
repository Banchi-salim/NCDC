from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Blog)
admin.site.register(Department)
admin.site.register(HeadOfDepartment)
admin.site.register(LocalGovernmentArea)
admin.site.register(DiseaseAlert)
admin.site.register(Report_disease_weekly)
admin.site.register(Weekly_Epidemiological_Report)
admin.site.register(Situation_Report)
admin.site.register(SituationReportFile)
admin.site.register(ProjectReport)
admin.site.register(AnnualReport)
admin.site.register(Guideline)
admin.site.register(GuidelineFile)
admin.site.register(EstablishmentDocument)
admin.site.register(ResearchWork)
admin.site.register(StateIncidentActionPlan)
admin.site.register(Disease)
admin.site.register(DGPost)
admin.site.register(Project)
admin.site.register(SecurityRiskDocument)
admin.site.register(Job)
admin.site.register(Department_Project)
admin.site.register(Department_Research)
admin.site.register(FinanceTransactionDocument)
admin.site.register(Advisory_Note)
admin.site.register(Events)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at')
    search_fields = ('subject', 'content')
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={'style': 'width: 90%; height: 200px;'})},
    }

class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(NewsletterSubscriber, NewsletterSubscriberAdmin)

