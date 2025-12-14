from django.urls import path
from . import views

app_name = 'social'
urlpatterns = [
    path('',views.about_page,name='about_page'),
    path('dashboards/social/',views.dashboard_about_page,name='dashboard_about_page'),
    path('dashboards/create/social/',views.dashboard_social_create,name='dashboard_social_create'),
    path('dashboards/<str:header>/about/',views.dashboard_about_edit,name='dashboard_about_edit'),
    path('dashboards/<str:name>/social/',views.dashboard_social_edit,name='dashboard_social_edit'),
    path('dashboards/<str:name>/delete/',views.dashboard_social_delete,name='dashboard_social_delete'),
]
