from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from users.models import User
from django.utils.timezone import now
from django.contrib import messages
from . models import InstructorVerification,AdminVerification
from Notifications.models import Notification,NotificationRecipient
# Create your views here.




class SuperAdminDashboard(View):
    def get(self,request):
        user_id=request.session.get('user_id')
        if not user_id:
            messages.error(request,"you need to login first!")
            return redirect("login")
        
        total_user=User.objects.all().count()
        return render(request,"superadmin/superadmin_dashboard.html",{'total_user':total_user})
    def post(self,request):
        pass


class UserManagementView(View):
    def get(self, request):
        users = User.objects.filter(role='student').order_by('-date_joined') 
        return render(request, "superadmin/user_management.html", {'users': users})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)  # Fetch the user
        action = request.POST.get('action')  # Get the action type

        if action == "change_role":
            new_role = request.POST.get('role')
            if new_role in ['student', 'instructor', 'admin']:
                user.role = new_role
                user.is_admin = (new_role == 'admin')
                user.is_instructor = (new_role == 'instructor')
                user.save()
                messages.success(request, f"Role updated to {new_role.capitalize()} for {user.full_name}")

        elif action == "ban_user":
            user.is_banned = not user.is_banned
            user.save()
            status = "unbanned" if not user.is_banned else "banned"
            messages.success(request, f"{user.full_name} has been {status}")

        return redirect('user_management') 

  

class InstructorManagementView(View):
    def get(self, request):
        # user_id=request.session.get('user_id')
        # if not user_id:
        #     messages.error(request,"you need to login first!")
        #     return redirect("login")
        instructors = InstructorVerification.objects.filter(status='pending')
        # for i in instructors:
        #     print(i.instructor.full_name)
        #     print(i.aadhar_number)
        return render(request, "superadmin/instructor_management.html", {"instructors": instructors})

    def post(self, request):
        instructor_id = request.POST.get("instructor_id")
        action = request.POST.get("action")
        instructor_verification = get_object_or_404(InstructorVerification,id=instructor_id)

        if action == "approve":
            instructor_verification.status = "approved"
            instructor_verification.reviewed_by = User.objects.get(id=request.session['user_id'])
            instructor_verification.reviewed_at = now()
            instructor_verification.save()

            instructor = instructor_verification.instructor
            instructor.is_verified = True
            instructor.save()

            messages.success(request, f"Instructor {instructor.get_full_name()} has been approved.")

        elif action == "reject":
            instructor_verification.status = "rejected"
            instructor_verification.reviewed_by = User.objects.get(id=request.session['user_id'])
            instructor_verification.reviewed_at = now()
            instructor_verification.save()

            instructor = instructor_verification.instructor
            instructor.is_verified = False
            instructor.save()

            messages.warning(request, f"Instructor {instructor.get_full_name()} has been rejected.")

        elif action == "ban":
            print("clicked ban")
            instructor = instructor_verification.instructor
            instructor.is_banned = not instructor.is_banned
            instructor.banned_date = now() if instructor.is_banned else None
            instructor.save()

            status = "banned" if instructor.is_banned else "unbanned"
            messages.warning(request, f"Instructor {instructor.full_name} has been {status}.")

        return redirect("instructor_management") 



class AdminManagementView(View):
    def get(self, request):
        # user_id=request.session.get('user_id')
        # if not user_id:
        #     messages.error(request,"you need to login first!")
        #     return redirect("login")
        admins = AdminVerification.objects.filter(admin_status="pending")
        return render(request, "superadmin/admin_management.html", {"admins": admins})

    def post(self, request):
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")

        if not user_id or not action:
            messages.error(request, "Invalid request!")
            return redirect("admin_management")

        admin_verification = get_object_or_404(AdminVerification, user_id=user_id)
        user = admin_verification.user

        if action == "approve_admin":
            admin_verification.admin_status = "approved"
            admin_verification.reviewed_by = User.objects.get(id=request.session['user_id'])
            admin_verification.reviewed_at = now()
            admin_verification.save()

            user.role = "admin"
            user.is_admin = True
            user.save()

            messages.success(request, f"{user.full_name} is now an admin!")

        elif action == "reject_admin":
            admin_verification.admin_status = "rejected"
            admin_verification.reviewed_by = User.objects.get(id=request.session['user_id'])
            admin_verification.reviewed_at = now()
            admin_verification.save()

            messages.warning(request, f"{user.full_name}'s admin request has been rejected.")

        elif action == "ban_admin":
            user.is_banned = not user.is_banned
            user.banned_date = now() if user.is_banned else None
            user.save()
            status = "banned" if user.is_banned else "unbanned"
            messages.success(request, f"{user.full_name} has been {status}.")

        return redirect("admin_management")


class ActivityReports(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class CourseConrol(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class Analytics(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class Notifications(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class RevenueAndTransaction(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class FeedBackControl(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

class RoleBasedAcess(View):
    def get(self,request):
        pass
    def post(self,request):
        pass



class PromoteToAdmin(View):
    def get(self,request,user_id):
        
        
        superadmin_id=request.session['user_id']
        
        if not user_id:
            return redirect('login')
        
        superadmin=User.objects.get(id=superadmin_id)
        if not superadmin.is_superadmin:
            return redirect("not_authorized")
        
        user=User.objects.get(id=user_id)
        user.is_admin=True
        user.save()

        messages.success(request,f"{user.full_name} is now Admin!")
        return redirect("superadmin_dashboard")

    def post(self,request):
        pass





#admin options
class AdminDashboard(View):
    def get(self,request):
        return render(request,"admin/admin_dashboard.html")
    def post(self,request):
        pass


class InstructorApprovalView(View):
    template_name = 'admin/instructor_approval.html'

    def get(self, request, *args, **kwargs):
        instructor_requests = InstructorVerification.objects.filter(status="pending")
        return render(request, self.template_name, {'instructor_requests': instructor_requests})

class ApproveInstructorView(View):
    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        instrucotr=InstructorVerification.objects.get(instructor=user)
        instrucotr.status = 'approved'
        instrucotr.instructor.role='instructor'
        instrucotr.save()
        instrucotr.instructor.save()
        
         
        notification = Notification.objects.create(
            user=user,
            title="Instructor Request Approved",
            message="Your request to become an instructor has been approved.",
            notification_type='admin_message'
        )

        NotificationRecipient.objects.create(
            notification=notification,
            user=user,
            is_read=False,
            reviewed_by =User.objects.get(id=request.session['user_id']),
            reviewed_at=now(),
        )


        messages.success(request, f'{user.username} has been approved as an instructor.')
        return redirect('instructor_approval')

class RejectInstructorView(View):
    def post(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        instrucotr=InstructorVerification.objects.get(instructor=user)
        instrucotr.status = 'rejected'
        instrucotr.save()

        notification = Notification.objects.create(
            user=user,
            title="Instructor Request Rejected",
            message="Your request to become an instructor has been Rejected.",
            notification_type='admin_message'
        )

        NotificationRecipient.objects.create(
            notification=notification,
            user=user,
            is_read=False,
            reviewed_by =User.objects.get(id=request.session['user_id']),
            reviewed_at=now(),
        )


        messages.warning(request, f'{user.username} has been rejected as an instructor.')
        return redirect('instructor_approval')


class Instructor_management(View):
    def get(self,request):
        active_instructors = InstructorVerification.objects.filter(status='approved')
        rejected_instructors = InstructorVerification.objects.filter(status='rejected')
        
        context = {
            'active_instructors': active_instructors,
            'rejected_instructors': rejected_instructors,
        }
        return render(request, 'admin/manage_instructors.html', context)

class UserManagement(View):
    def get(self,request):
        users = User.objects.filter(role__in=['student', 'instructor'])

        context = {
            'users': users
        }
        return render(request, 'admin/user_management.html', context)

class EditUserView(View):
    def get(self, request, user_id, *args, **kwargs):
        pass
    def post(self, request, user_id, *args, **kwargs):
        pass

class DeleteUserView(View):
    def post(self,request):
         user_id=request.POST.get('user_id')
         user = get_object_or_404(User, id=user_id)
         user.is_banned=True
         user.save()
         return redirect('manage_users')

class RestoreUser(View):
    def post(self,request):
         user_id=request.POST.get('user_id')
         user = get_object_or_404(User, id=user_id)
         user.is_banned=False
         user.save()
         return redirect('manage_users')
