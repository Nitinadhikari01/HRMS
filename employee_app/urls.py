from . import views
from django.urls import path


urlpatterns = [
    path('dashboard', views.employee_dashboard, name="employee-dashboard-page"),
    path('employee_details', views.employee_details, name="employee-details-page"),
]