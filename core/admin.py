from django.contrib import admin
from courses.models import Course

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

admin.site.register(Course, CourseAdmin)
