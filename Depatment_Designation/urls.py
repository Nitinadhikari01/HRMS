from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # urls for departments
    path('', views.departments_list, name="department-page"),
    path('manage_departments', views.manage_departments, name="manage_departments-page"),
    path('save_department', views.save_department, name="save-department-page"),
    path('delete_department', views.delete_department, name="delete-department"),

    # urls for positions
    path('designation', views.designation_list, name="designation-page"),
    path('manage_designation', views.manage_designations, name="manage_positions-page"),
    path('save_designation', views.save_designation, name="save-designation-page"),
    path('delete_designation', views.delete_designation, name="delete-designation"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

