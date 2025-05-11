from django.contrib import admin
from . models import User

class UserAdmin(admin.ModelAdmin):
    list_display=('id','username','password','admin_status')


admin.site.register(User,UserAdmin)

