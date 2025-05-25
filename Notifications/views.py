from django.shortcuts import render,get_object_or_404
from django.views import View
from .models import NotificationRecipient,AdminNotification,Notification
from django.http import JsonResponse
from users.models import User


class ManageNotifications(View):
    def get(self,request):
        return render(request,"notification/manage_notifications.html")
    def post(self,request):
        pass

    
class GetUserNotifications(View):
    def get(self, request):
        if 'user_id':
        
            notifications = Notification.objects.filter(user=User.objects.get(id=request.session['user_id'])).order_by("created_at")
            data = [
        
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "timestamp": n.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for n in notifications if not n.is_deleted
            ]
            return JsonResponse({"notifications": data})


class MakeNotificationsAsRead(View):
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=User.objects.get(id=request.session['user_id']))
            notification.is_read = True
            notification.save()
            return JsonResponse({"status": "success", "message": "Notification marked as read."})
        except Notification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Notification not found."}, status=404)

class MarkAllNotificationAsRead(View):
    def post(self, request):
        notifications = NotificationRecipient.objects.filter(user=User.objects.get(id=request.session['user_id']), is_read=False)
        notifications.update(is_read=True)
        return JsonResponse({"success": True, "message": "All notifications marked as read."})


class HideNotification(View):
   def post(self, request,notification_id):
        print("yes notification hiden")
        notification = Notification.objects.get(id=notification_id)
        notification.is_deleted=True
        notification.save()
        return JsonResponse({"success": True, "message": "Notification deleted."})


class GetUnreadNotificationCount(View):
    def get(self, request):
        unread_count = NotificationRecipient.objects.filter(user=request.user, is_read=False).count()
        notifications = NotificationRecipient.objects.filter(user=request.user, is_read=False).values("notification__title")[:5]
        return JsonResponse({"count": unread_count, "notifications": list(notifications)})


# Admin
class SendNotificationToUser(View):
    def post(self, request):
        user_id = request.POST.get("user_id")
        title = request.POST.get("title")
        message = request.POST.get("message")
        notification_type = request.POST.get("notification_type")

        user = get_object_or_404(User, id=user_id)
        notification = Notification.objects.create(
            user=user, title=title, message=message, notification_type=notification_type
        )
        NotificationRecipient.objects.create(notification=notification, user=user)

        return JsonResponse({"success": True, "message": "Notification sent to user."})


class SendNotificationToAll(View):
    def post(self, request):
        print("sended msg to all")
        title = request.POST.get("title")
        message = request.POST.get("message")
        notification_type = request.POST.get("notification_type")
        print(title)

        users = User.objects.all()
        for user in users:
            notification = Notification.objects.create(
                user=user, title=title, message=message, notification_type=notification_type
            )
            NotificationRecipient.objects.create(notification=notification, user=user)

        return JsonResponse({"success": True, "message": "Notification sent to all users."})



class SendNotificationToinstructor(View):
    def post(self, request):
        instructor_id = request.POST.get("instructor_id")
        title = request.POST.get("title")
        message = request.POST.get("message")
        notification_type = request.POST.get("notification_type")

        instructor = get_object_or_404(User, id=instructor_id)
        notification = Notification.objects.create(
            user=instructor, title=title, message=message, notification_type=notification_type
        )
        NotificationRecipient.objects.create(notification=notification, user=instructor)

        return JsonResponse({"success": True, "message": "Notification sent to instructor."})


class SendNotificationsToAllInstructor(View):
    def post(self, request):
        title = request.POST.get("title")
        message = request.POST.get("message")
        notification_type = request.POST.get("notification_type")

        instructors = User.objects.filter(role="Instructor")  # Assuming 'role' field exists
        for instructor in instructors:
            notification = Notification.objects.create(
                user=instructor, title=title, message=message, notification_type=notification_type
            )
            NotificationRecipient.objects.create(notification=notification, user=instructor)

        return JsonResponse({"success": True, "message": "Notification sent to all instructors."})


class GetAllNotifications(View):
    def get(self, request):
        notifications = Notification.objects.all().order_by("-created_at")
        return render(request, "notifications/admin_dashboard.html", {"notifications": notifications})



#Instrucotr
# Fetch all notifications for an instructor.
class GetInstrucotrNotification(View):
    def get(self, request):
        notifications = NotificationRecipient.objects.filter(user=request.user).order_by("-notification__created_at")
        return render(request, "notifications/instructor_notifications.html", {"notifications": notifications})





#superadmin
class GetSuperAdminNotifications(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class SendNotificationToSuperadmin(View):
    def get(self,request):
        pass
    def post(self,request):
        pass




class LiveNotificationStream(View):
    def get(self,request):
        pass
    def post(self,request):
        pass
