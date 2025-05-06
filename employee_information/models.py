from datetime import datetime
from django_jsonfield_backport.models import JSONField
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone

# Create your models here.
class Department(models.Model):
    name = models.TextField()
    hod = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.TextField()
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class DocumentAccess(models.Model):
    appointment_document = models.FileField(upload_to='documents/appointment_document/', blank=True, null=True)
    offer_letter = models.FileField(upload_to='documents/offer_letter/', blank=True, null=True)
    company_policies = models.FileField(upload_to='documents/company_policies', blank=True, null=True)

    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document {self.id}"


class Holiday(models.Model):
    holiday_file = models.FileField(upload_to='documents/holiday_file/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Employees(models.Model):
    emp_code = models.CharField(max_length=100,blank=True)
    firstname = models.TextField() 
    middlename = models.TextField(blank=True,null= True) 
    lastname = models.TextField()

    emp_img = models.ImageField(upload_to='profile_photo/', blank=True, null=True)

    gender = models.TextField(blank=True,null= True) 
    dob = models.DateField(blank=True,null= True) 
    contact = models.TextField()
    address = models.TextField() 
    email = models.TextField()

    reporting_mng = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)

    education_qualification = models.CharField(max_length=100, blank=True)
    last_emp_details = models.TextField(blank=True, null=True)

    emergency_contact_name = models.TextField(blank=True, null=True)
    emergency_contact_number = models.TextField(blank=True, null=True)

    document = models.OneToOneField(DocumentAccess, on_delete=models.CASCADE, blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee")

    # pay compensation

    department_id = models.ForeignKey(Department, on_delete=models.CASCADE) 
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE) 
    date_hired = models.DateField() 
    salary = models.FloatField(default=0) 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *arg, **kwargs):

        super().save(*arg, **kwargs)

        if self.status and not self.user:
            username = self.emp_code
            password = f"{self.firstname.lower()}@{self.emp_code}"

            # Create User
            user = User.objects.create_user(
                username=username,
                email=self.email,
                password=password,
                is_active=True
            )

            group, created = Group.objects.get_or_create(name="Employee")
            user.groups.add(group)

            self.user = user
            self.save(update_fields=['user'])

        elif not self.status:
            if self.user:
                self.user.is_active = False
                self.user.save(update_fields=['is_active'])

    def delete(self, *arg, **kwargs):
        if self.user:
            self.user.delete()
        super().delete(*arg, **kwargs)

    def __str__(self):
        return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '


class EmployeeLeave(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    leave_entitlement = models.PositiveIntegerField(default=20)
    leaves_availed = JSONField(default=dict)
    leave_balance = models.PositiveIntegerField()



class Asset(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    asset_code = models.CharField(max_length=50)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.asset_code})"


class ExitDetails(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=[
        ('Resignation', 'Resignation'),
        ('Termination', 'Termination'),
        ('Absconding', 'Absconding')
    ])
    clearance_form = models.FileField(upload_to='clearance_forms/', blank=True, null=True)
    experience_letter = models.FileField(upload_to='experience_letters/', blank=True, null=True)
    relieving_letter = models.FileField(upload_to='relieving_letters/', blank=True, null=True)
    no_dues_form = models.FileField(upload_to='no_dues_form/', blank=True, null=True)
    asset_handover = models.BooleanField(default=False)
    no_dues_submission = models.BooleanField(default=False)
    clearance_chk = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.reason}"
