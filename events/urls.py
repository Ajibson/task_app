from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', home, name = 'home'),
   path('update_task/<int:task_no>', update_task, name = 'update_task'),
   path('delete_task/<int:task_no>', delete_task, name = 'delete_task'),
   path('task_reminder/<int:task_no>', task_reminder, name = 'task_reminder'),
   path('signup/', signup, name = 'signup'),
   path('activate/<uidb64>/<token>/', activate , name='activate'),
   path('login/', Login, name = 'login'),
   path('logout/', auth_views.LogoutView.as_view(),name='logout'),
]
