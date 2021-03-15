from django.contrib import admin
from django.urls import path,include



#Admin Configuration 

admin.site.site_header = 'Events Planner'
admin.site.site_title = "My Event Planner"
admin.site.index_title = "Welcome to Event Planner"


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('events.urls')),
    
]
