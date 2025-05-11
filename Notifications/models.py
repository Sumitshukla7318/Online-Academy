
from django.db import models
from users.models import User
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('order_update', 'Order Update'),
        ('admin_message', 'Admin Message'),
        ('system_alert', 'System Alert'),
        ('promotion', 'Promotion'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save()

    def __str__(self):
        return f"{self.title} - {self.user.username}"


# For system-wide notifications sent to multiple users
class NotificationRecipient(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notification_recipients")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notifications")
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification to {self.user.username}"


# For notifications sent specifically to Admins
# Keeps admin messages separate from normal users' notifications.
# Helps filter admin-related messages in a dashboard.
class AdminNotification(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_notifications")
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin Notification - {self.admin.username}"
