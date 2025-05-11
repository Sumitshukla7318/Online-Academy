from django.db import models
from users.models import User


class AdminVerification(models.Model):
    STATUS_CHOICES = [
        ('no_request', 'No Request'),
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin_request")
    aadhar_number = models.CharField(max_length=12, unique=True)  # For simplicity, using Aadhar No
    admin_status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='no_request')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="admin_reviews")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.status}"

class AdminActivityLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_logs")
    action = models.CharField(max_length=255)  # Example: "Banned user", "Approved instructor"
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="target_user_logs")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.action} - {self.timestamp}"
    

#this model allow admin and instructors to report users base on Violence
class UserReport(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_by")
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_user")
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('resolved', 'Resolved')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reported_by.username} against {self.reported_user.username}"


class InstructorVerification(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor_verification")
    aadhar_number = models.CharField(max_length=12, unique=True,default=None)
    pan_number = models.CharField(max_length=10, unique=True,default=None) 
    account_number = models.CharField(max_length=20, unique=True,default=None) 
    
    status = models.CharField(
        max_length=20,
        choices=[('no_request', 'No Request'), ('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='no_request'
    )

    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_instructors")
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.instructor.username} - {self.status.capitalize()}"



class SystemLog(models.Model):
    superadmin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="system_logs")
    action = models.CharField(max_length=255)  # Example: "Changed site settings", "Created new admin"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.timestamp}"


class RevenueTracking(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20,
        choices=[('purchase', 'Course Purchase'), ('payout', 'Instructor Payout')],
        default='purchase'
    )
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.transaction_type} - {self.status}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}"


class GlobalSettings(models.Model):
    site_name = models.CharField(max_length=100, default="My Learning Platform")
    maintenance_mode = models.BooleanField(default=False)  # If True, only SuperAdmin can access the site
    terms_of_service = models.TextField(blank=True, null=True)
    privacy_policy = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.site_name

