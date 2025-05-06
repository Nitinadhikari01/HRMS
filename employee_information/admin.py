from django.contrib import admin
from employee_information.models import Department, Position, Employees

# Register your models here.

# my superuser - hp
# password - admin

admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employees)