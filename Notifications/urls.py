from django.urls import path
from . import views
urlpatterns = [

    # path('',views)
    path('manage_notifications/',views.ManageNotifications.as_view(),name='manage_notifications'),
    
    path("user/", views.GetUserNotifications.as_view(), name="user_notifications"),
    path("mark-as-read/<int:notification_id>/", views.MakeNotificationsAsRead.as_view(), name="mark_as_read"),
    path("mark-all-read/", views.MarkAllNotificationAsRead.as_view(), name="mark_all_read"),
    path("hide/<int:notification_id>", views.HideNotification.as_view(), name="hide_notification"),
    path("unread-count/", views.GetUnreadNotificationCount.as_view(), name="unread_count"),
    
    # url for admin
    path("admin/send-user/", views.SendNotificationToUser.as_view(), name="send_notification_user"),
    path("admin/send-all/", views.SendNotificationToAll.as_view(), name="send_notification_all"),
    path("admin/all/", views.GetAllNotifications.as_view(), name="get_all_notifications"),

    # url for instructor
    path("instructor/", views.GetInstrucotrNotification.as_view(), name="get_instructor_notification"),
    path("instructor/send/", views.SendNotificationToinstructor.as_view(), name="send_notification_instructor"),
    path("instructor/send-all/", views.SendNotificationsToAllInstructor.as_view(), name="send_notifications_all_instructors"),
]
