from django.contrib import admin
from django.urls import path

from day import views as day_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('day/<int:day>/', day_views.day, name='day'),
    path('day/', day_views.day, name='day'),
]
