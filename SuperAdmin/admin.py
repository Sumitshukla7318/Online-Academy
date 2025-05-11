from django.contrib import admin
from . models import InstructorVerification

class Instrctor_VRFY(admin.ModelAdmin):
    list_display=('id','instructor')

admin.site.register(InstructorVerification,Instrctor_VRFY)
# Register your models here.
