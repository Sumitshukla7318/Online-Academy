from django.contrib import admin
from .models import Course,Enrollment

class EnrollmentAdmin(admin.ModelAdmin):
    list_display=('user','course','progress','enrolled_at')

admin.site.register(Enrollment,EnrollmentAdmin)

# Register your models here.
