from django import template
from users.models import User
from SuperAdmin.models import InstructorVerification,AdminVerification

register = template.Library()

@register.filter
def is_instructor(user_id):
    # print("user_id=>",user_id)
    if user_id:
        # print("yes")
        user = User.objects.get(id=user_id)
        # i=InstructorVerification.objects.get(instructor=user)
        # print(i.instructor.username,i.instructor.role)
        print(user.username,user.role)
        try:
            if  user.role.lower()=='instructor':
                print(user.role)
                return True
        except User.DoesNotExist:
            return False
    return False


@register.filter
def is_admin(user_id):
    if user_id:
        # print("yes")
        user = User.objects.get(id=user_id)
        try:
            if user.role.lower()=='admin':
                return True
        except User.DoesNotExist:
            return False
    return False

@register.filter
def is_superadmin(user_id):
    if user_id:
        # print("yes")
        user = User.objects.get(id=user_id)
        try:
            if user.role.lower()=='superadmin':
                return True
        except User.DoesNotExist:
            return False
    return False

