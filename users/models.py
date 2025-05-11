from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
        ('superadmin', 'SuperAdmin'),
    )
    
    STATUS_CHOICES = [
    ("No Request",None),
    ("pending", "Pending"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ]

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150, default="")
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_instructor=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    admin_status=models.CharField(max_length=10,choices=STATUS_CHOICES,null=True,blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,null=True,blank=True) 
    is_verified = models.BooleanField(default=False)  # approve for instructor role
    is_banned = models.BooleanField(default=False)  # Implemeted Soft delete
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users') 
    approval_date = models.DateTimeField(null=True, blank=True)
    banned_date = models.DateTimeField(null=True, blank=True)  #
  
    #checking who creates admin
    date_joined = models.DateTimeField(auto_now_add=True)

    # Soft Delete Functionality
    def soft_delete(self):
        """Soft delete the user instead of permanently deleting them."""
        self.is_banned = True
        self.save()

    def restore_user(self):
        """Restore a banned user."""
        self.is_banned = False
        self.save()

    # Role Management
    def promote_to_admin(self, superadmin):
        """Promote a user to admin (Only SuperAdmin can do this)"""
        if superadmin.role == 'superadmin':
            self.role = 'admin'
            self.created_by = superadmin
            self.save()

    def promote_to_superadmin(self):
        """Only manually create the first SuperAdmin"""
        self.role = 'superadmin'
        self.save()

    def __str__(self):
        return f"{self.username} - {self.role}"
