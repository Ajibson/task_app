from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('dashboard', home, name = 'home'),
   path('update_task/<int:task_no>', update_task, name = 'update_task'),
   path('delete_task/<int:task_no>', delete_task, name = 'delete_task'),
   path('task_reminder/<int:task_no>', task_reminder, name = 'task_reminder'),

   #User signup and login urls
   path('', signup, name = 'signup'),
   path('activate/<uidb64>/<token>/', activate , name='activate'),
   path('login/', Login, name = 'login'),
   path('logout/', auth_views.LogoutView.as_view(),name='logout'),
   path('profile_update', profile_update, name = 'profile_update'),

   #password reset urls
   path("password_reset/", password_reset_request, name="reset_password"),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),   
]
