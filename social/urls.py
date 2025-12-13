from django.urls import path
from . import views

app_name = 'social'
urlpatterns = [
    path('',views.about_page,name='about_page'),
    path('dashboards/social/',views.dashboard_about_page,name='dashboard_about_page'),
    path('dashboards/<str:header>/about/',views.dashboard_about_edit,name='dashboard_about_edit'),
]
