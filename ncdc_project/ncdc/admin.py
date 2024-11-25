from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Blog)
admin.site.register(Department)
admin.site.register(HeadOfDepartment)
admin.site.register(DiseaseAlert)
admin.site.register(Report_disease_weekly)
admin.site.register(Weekly_Epidemiological_Report)
