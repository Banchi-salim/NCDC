from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Blog)
admin.site.register(Department)
admin.site.register(HeadOfDepartment)
admin.site.register(DiseaseAlert)
admin.site.register(Report_disease_weekly)
admin.site.register(Weekly_Epidemiological_Report)
admin.site.register(Situation_Report)
admin.site.register(SituationReportFile)
admin.site.register(ProjectReport)
admin.site.register(AnnualReport)

