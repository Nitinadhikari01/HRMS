from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home', views.home, name="home-page"),
    path('pdf/<int:pdf_id>/', views.serve_pdf, name='serve_pdf'),

    # for authentication

    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),

    path('', auth_views.LoginView.as_view(template_name = 'employee_information/login.html',redirect_authenticated_user=True), name="login"),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('userlogin', views.login_user, name="login-user"),
    path('logoutuser', views.logoutuser, name="logoutuser"),

    # urls for employees:
    path('employees', views.employees_list, name="employee-page"),
    path('manage_employees', views.manage_employees, name="manage_employees-page"),
    path('save_employee', views.save_employee, name="save-employee-page"),
    path('delete_employee', views.delete_employee, name="delete-employee"),
    path('view_employee', views.view_employee, name="view-employee-page"),


    path('save-leave/', views.save_leave, name='save_leave'),
    path('get-leave-details/', views.get_leave_details, name='get_leave_details'),



    path('save-asset/', views.save_asset, name='save_asset'),
    path('load-assets/', views.load_assets, name='load_assets'),
    path('get-asset-details/', views.get_asset_details, name='get_asset_details'),
    path('delete-asset/', views.delete_asset, name='delete_asset'),

    path('save-exit-details/', views.save_exit_details, name='save_exit_details'),
    # path('delete-exit-details/', views.delete_exit_details, name='delete_exit_details'),
    path('get-exit-details/', views.get_exit_details, name='get_exit_details'),


    path('get_emp_bnk_details/', views.get_emp_bnk_details, name='get_emp_bnk_details'),
    path('save_emp_bnk_details/', views.save_emp_bnk_details, name='save_emp_bnk_details'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

