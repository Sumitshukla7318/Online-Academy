from django import template
from users.models import User

register = template.Library()

@register.filter
def is_instructor(user_id):
    # print("user_id=>",user_id)
    if user_id:
        # print("yes")
        user = User.objects.get(id=user_id)
        print(user.username,user.is_instructor)
        try:
            if user.is_instructor:
                return True
        except User.DoesNotExist:
            return False
    return False

