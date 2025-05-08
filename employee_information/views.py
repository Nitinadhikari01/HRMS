from django.http import HttpResponse
from employee_information.models import Department, Position, Employees, DocumentAccess,Asset, ExitDetails, EmployeeLeave
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
import logging
logger = logging.getLogger(__name__)
import csv
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Holiday
from django.http import FileResponse
from django.views.decorators.clickjacking import xframe_options_exempt

# ---------------------------- VIEW STARTS FOR THE LOGIN-LOGOUT


@csrf_exempt
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
                if user.groups.filter(name="Employee").exists():
                    resp['group'] = 'normal_employee'
                else:
                    resp['group'] = 'admin'
            else:
                logger.warning(f"Login denied for inactive user: {username}")
                resp['msg'] = "Account is inactive."
        else:
            resp['msg'] = "Incorrect username or password"

    return JsonResponse(resp)


#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# ---------------------------- VIEW END FOR THE LOGIN-LOGOUT



# ---------------------------- VIEW STARTS FOR THE HOME-PAGE
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf')
        if pdf_file:
            try:
                holiday = Holiday()
                holiday.holiday_file.save(pdf_file.name, pdf_file, save=False)
                holiday.save()
                messages.success(request, "PDF uploaded successfully.")
            except Exception as e:
                messages.error(request, f"Error uploading PDF: {e}")
        else:
            messages.warning(request, "No PDF file was selected.")
        return redirect('home-page')

    else:
        pdfs = Holiday.objects.all()
        total_department = Department.objects.count()
        total_position = Position.objects.count()
        total_employee = Employees.objects.count()
        active_employees = Employees.objects.filter(status=1).count()
        latest_pdf = Holiday.objects.order_by('-id').first()

        if not request.user.groups.filter(name='Employee').exists():
            context = {
                'page_title': 'Home',
                'total_department': total_department,
                'total_position': total_position,
                'total_employee': total_employee,
                'active_employees': active_employees,
                'pdfs': pdfs,
                'latest_pdf': latest_pdf,
            }
            return render(request, 'employee_information/home.html', context)
        else:
            employee_list = Employees.objects.filter(emp_code=request.user.username)
            employee = employee_list.first()

            leave_record = EmployeeLeave.objects.filter(employee_id=employee.id).first()
            context = {
                'page_title': 'Employees Dashboard',
                'leave_entitlement': leave_record.leave_entitlement if leave_record else 0,
                'leaves_availed': leave_record.leaves_availed if leave_record else 0,
                'leave_balance': leave_record.leave_balance if leave_record else 0,
                'employees': employee_list,
                'latest_pdf': latest_pdf,
            }
            return render(request, 'employee_dashboard.html', context)



@xframe_options_exempt
def serve_pdf(request, pdf_id):
    holiday = Holiday.objects.get(id=pdf_id)
    file_path = holiday.holiday_file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')




# ---------------------------- VIEW END FOR THE HOME-PAGE



# ---------------------------- VIEW STARTS FOR THE EMPLOYEE
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employees_list(request):
    employee_list = Employees.objects.all()
    context = {
        'page_title':'Employees',
        'employees':employee_list,
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'employee_information/employees.html',context)
    else:
        employee_list = Employees.objects.filter(emp_code=request.user.username)
        employee = employee_list.first()
        latest_pdf = Holiday.objects.order_by('-id').first()

        leave_record = EmployeeLeave.objects.filter(employee_id=employee.id).first()
        context = {
            'page_title': 'Employees Dashboard',
            'leave_entitlement': leave_record.leave_entitlement if leave_record else 0,
            'leaves_availed': leave_record.leaves_availed if leave_record else 0,
            'leave_balance': leave_record.leave_balance if leave_record else 0,
            'employees': employee_list,
            'latest_pdf': latest_pdf,
        }
        return render(request, 'employee_dashboard.html', context)



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def manage_employees(request):
    employee = {}
    departments = Department.objects.all()
    positions = Position.objects.all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employee,
        'departments' : departments,
        'positions' : positions
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'employee_information/manage_employee.html',context)
    else:
        employee_list = Employees.objects.filter(emp_code=request.user.username)
        employee = employee_list.first()
        latest_pdf = Holiday.objects.order_by('-id').first()

        leave_record = EmployeeLeave.objects.filter(employee_id=employee.id).first()
        context = {
            'page_title': 'Employees Dashboard',
            'leave_entitlement': leave_record.leave_entitlement if leave_record else 0,
            'leaves_availed': leave_record.leaves_availed if leave_record else 0,
            'leave_balance': leave_record.leave_balance if leave_record else 0,
            'employees': employee_list,
            'latest_pdf': latest_pdf,
        }
        return render(request, 'employee_dashboard.html', context)



@login_required
def save_employee(request):
    data = request.POST
    resp = {'status': 'failed'}

    if (data['id']).isnumeric() and int(data['id']) > 0:
        check = Employees.objects.exclude(id=data['id']).filter(emp_code=data['emp_code'])
    else:
        check = Employees.objects.filter(emp_code=data['emp_code'])
    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            dept = Department.objects.filter(id=data['department_id']).first()
            pos = Position.objects.filter(id=data['position_id']).first()

            # file uploads
            profile_photo = request.FILES.get('emp_img')
            appointment_document = request.FILES.get('appointment_document')
            offer_letter = request.FILES.get('offer_letter')
            company_policies = request.FILES.get('company_policies')

            aadhar_card = request.FILES.get('aadhar_card')
            pan_card = request.FILES.get('pan_card')
            edu_cert = request.FILES.get('edu_cert')

            if (data['id']).isnumeric() and int(data['id']) > 0:
                # Updating an existing employee
                # Updating an existing employee
                employee = Employees.objects.get(id=data['id'])
                employee.emp_code = data['emp_code']
                employee.firstname = data['firstname']
                employee.middlename = data['middlename']
                employee.lastname = data['lastname']
                employee.gender = data['gender']
                employee.dob = data['dob']
                employee.contact = data['contact']
                employee.email = data['email']
                employee.address = data['address']
                employee.department_id = dept
                employee.position_id = pos
                employee.date_hired = data['date_hired']
                # employee.salary = data['salary']
                employee.status = data['status']
                employee.reporting_mng = data['reporting_mng']
                employee.marital_status = data['marital_status']
                employee.education_qualification = data['education_qualification']
                employee.last_emp_details = data['last_emp_details']
                employee.emergency_contact_name = data['emergency_contact_name']
                employee.emergency_contact_number = data['emergency_contact_number']

                if profile_photo:
                    employee.emp_img = profile_photo

                # Handle documents
                if employee.document:
                    if appointment_document:
                        employee.document.appointment_document = appointment_document
                    if offer_letter:
                        employee.document.offer_letter = offer_letter
                    if company_policies:
                        employee.document.company_policies = company_policies
                    if aadhar_card:
                        employee.document.aadhar_card = aadhar_card
                    if pan_card:
                        employee.document.pan_card = pan_card
                    if edu_cert:
                        employee.document.edu_certificate = edu_cert
                    employee.document.save()
                else:
                    document = DocumentAccess.objects.create(
                        appointment_document=appointment_document,
                        offer_letter=offer_letter,
                        company_policies=company_policies,
                        aadhar_card = aadhar_card,
                        pan_card = pan_card,
                        edu_certificate = edu_cert
                    )
                    employee.document = document

                employee.save()  # Final save

                # Deactivate/Activate associated user based on employee status
                if employee.user:
                    employee.user.is_active = (employee.status == '1')  # or employee.status for BooleanField
                    employee.user.save(update_fields=['is_active'])

                resp['msg'] = 'Employee Details Updated Successfully'
            else:
                # for new employee
                document = DocumentAccess.objects.create(
                    appointment_document=appointment_document,
                    offer_letter=offer_letter,
                    company_policies=company_policies,
                    aadhar_card = aadhar_card,
                    pan_card = pan_card,
                    edu_certificate = edu_cert
                )
                employee = Employees(
                    emp_code=data['emp_code'],
                    firstname=data['firstname'],
                    middlename=data['middlename'],
                    lastname=data['lastname'],
                    gender=data['gender'],
                    dob=data['dob'],
                    contact=data['contact'],
                    email=data['email'],
                    address=data['address'],
                    department_id=dept,
                    position_id=pos,
                    date_hired=data['date_hired'],
                    # salary=data['salary'],
                    status=data['status'],
                    emp_img=profile_photo,
                    document=document,
                    reporting_mng = data['reporting_mng'],
                    marital_status = data['marital_status'],
                    education_qualification=data['education_qualification'],
                    last_emp_details=data['last_emp_details'],
                    emergency_contact_name=data['emergency_contact_name'],
                    emergency_contact_number=data['emergency_contact_number']
                )
                employee.save()
                resp['msg'] = 'Employee Details Saved Successfully'
            resp['status'] = 'success'
        except Exception as e:
            resp['status'] = 'failed'
            print(f"Error: {e}")
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_employee(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Employees.objects.filter(id = data['id']).delete()
        # ExitDetails.objects.filter(employee_id=data['id']).delete()

        resp['status'] = 'success'
        resp['msg'] = 'Employee Deleted Successfully'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_employee(request):
    employee = {}
    departments = Department.objects.all()
    positions = Position.objects.all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee' : employee,
        'departments' : departments,
        'positions' : positions
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'employee_information/view_employee.html',context)
    else:
        employee_list = Employees.objects.filter(emp_code=request.user.username)
        employee = employee_list.first()
        latest_pdf = Holiday.objects.order_by('-id').first()

        leave_record = EmployeeLeave.objects.filter(employee_id=employee.id).first()
        context = {
            'page_title': 'Employees Dashboard',
            'leave_entitlement': leave_record.leave_entitlement if leave_record else 0,
            'leaves_availed': leave_record.leaves_availed if leave_record else 0,
            'leave_balance': leave_record.leave_balance if leave_record else 0,
            'employees': employee_list,
            'latest_pdf': latest_pdf,
        }
        return render(request, 'employee_dashboard.html', context)


# ---------------------------- VIEW END FOR THE EMPLOYEE



# ---------------------------- VIEW STARTS FOR THE ASSETS
@login_required
@csrf_exempt
def save_asset(request):
    if request.method == 'POST':
        try:
            employee_id = request.POST.get('employee_id')
            asset_id = request.POST.get('asset_id')
            name = request.POST.get('name')
            serial_number = request.POST.get('serial_number')
            issue_date = request.POST.get('issue_date')
            asset_code = request.POST.get('asset_code')

            employee = Employees.objects.get(id=employee_id)

            if asset_id:
                asset = Asset.objects.get(id=asset_id)
                asset.name = name
                asset.serial_number = serial_number
                asset.issue_date = issue_date
                asset.asset_code = asset_code
                asset.save()
            else:
                asset = Asset.objects.create(
                    name=name,
                    serial_number=serial_number,
                    issue_date=issue_date,
                    asset_code=asset_code,
                    employee=employee
                )
            assets = Asset.objects.filter(employee_id=employee_id).values()

            return JsonResponse({
                'status': 'success',
                'message': 'Asset saved successfully.',
                'assets': list(assets)
            })
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})


@login_required
def get_asset_details(request):
    if request.method == 'GET':
        try:
            asset_id = request.GET.get('asset_id')
            asset = Asset.objects.filter(id=asset_id).values().first()
            if asset:
                return JsonResponse({'status': 'success', 'asset': asset})
            else:
                return JsonResponse({'status': 'failed', 'message': 'Asset not found.'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})


@login_required
def load_assets(request):
    if request.method == 'GET':
        try:
            employee_id = request.GET.get('employee_id')
            assets = Asset.objects.filter(employee_id=employee_id).values()
            return JsonResponse({'status': 'success', 'assets': list(assets)})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})


@csrf_exempt
def delete_asset(request):
    if request.method == 'POST':
        try:
            asset_id = request.POST.get('asset_id')
            asset = Asset.objects.get(id=asset_id)
            asset.delete()

            return JsonResponse({'status': 'success', 'message': 'Asset deleted successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})

# ---------------------------- VIEW END FOR THE ASSETS



# ---------------------------- VIEW STARTS FOR THE EXIT EMPLOYEE DETAILS
@login_required
@csrf_exempt
def save_exit_details(request):
    if request.method == 'POST':
        try:
            employee_id = request.POST.get('employee_id')
            reason = request.POST.get('reason')
            asset_handover = request.POST.get('asset_handover') == 'on'
            no_dues_submission = request.POST.get('no_dues_submission') == 'on'
            clearance_chk_bx = request.POST.get('clearance_chk_bx') == 'on'

            employee = Employees.objects.get(id=employee_id)

            exit_details, created = ExitDetails.objects.update_or_create(employee=employee)

            exit_details.reason = reason
            exit_details.asset_handover = asset_handover
            exit_details.no_dues_submission = no_dues_submission
            exit_details.clearance_chk = clearance_chk_bx

            if 'clearance_form' in request.FILES:
                exit_details.clearance_form = request.FILES['clearance_form']
            if 'experience_letter' in request.FILES:
                exit_details.experience_letter = request.FILES['experience_letter']
            if 'relieving_letter' in request.FILES:
                exit_details.relieving_letter = request.FILES['relieving_letter']
            if 'no_dues_form' in request.FILES:
                exit_details.no_dues_form = request.FILES['no_dues_form']

            exit_details.save()

            return JsonResponse({'status': 'success', 'message': 'Exit details saved successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})


# @csrf_exempt
# def delete_exit_details(request):
#     if request.method == 'POST':
#         try:
#             employee_id = request.POST.get('employee_id')
#             exit_details = ExitDetails.objects.get(employee_id=employee_id)
#             exit_details.delete()
#
#             return JsonResponse({'status': 'success', 'message': 'Exit Details deleted successfully.'})
#         except Exception as e:
#             return JsonResponse({'status': 'failed', 'message': str(e)})
#     else:
#         return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})


@login_required
@csrf_exempt
def get_exit_details(request):
    if request.method == 'GET':
        try:
            employee_id = request.GET.get('employee_id')
            exit_details = ExitDetails.objects.filter(employee_id=employee_id).values().first()
            if exit_details:
                return JsonResponse({'status': 'success', 'exit_details': exit_details})
            else:
                return JsonResponse({'status': 'failed', 'message': 'No exit details found.'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})

# ---------------------------- VIEW END FOR EXIT EMPLOYEE DETAILS


# ---------------------------- VIEW START FOR EMPLOYEE LEAVE DETAILS


@csrf_exempt
def save_leave(request):
    if request.method == 'POST':
        try:
            employee_id = request.POST.get('employee_id')
            leave_entitlement = int(request.POST.get('leave_entitlement', 20))

            months = [
                'april', 'may', 'june', 'july',
                'august', 'september', 'october', 'november',
                'december', 'january', 'february', 'march'
            ]
            leaves_availed = {}

            for month in months:
                value = request.POST.get(month, '0')
                leaves_availed[month] = int(value) if value.isdigit() else 0

            total_availed = sum(leaves_availed.values())
            leave_balance = leave_entitlement - total_availed

            try:
                employee = Employees.objects.get(id=employee_id)

                leave_record, created = EmployeeLeave.objects.update_or_create(
                    employee=employee,
                    defaults={
                        'leave_entitlement': leave_entitlement,
                        'leaves_availed': leaves_availed,
                        'leave_balance': leave_balance
                    }
                )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Leave data saved successfully.',
                    'data': {
                        'leave_entitlement': leave_record.leave_entitlement,
                        'leaves_availed': leave_record.leaves_availed,
                        'leave_balance': leave_record.leave_balance
                    }
                })

            except Employees.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Employee not found.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server error: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def get_leave_details(request):

    employee_id = request.GET.get('employee_id')

    try:
        leave_record = EmployeeLeave.objects.get(employee_id=employee_id)
        name  = Employees.objects.filter(id=employee_id).values('firstname', 'middlename', 'lastname')
        if name:
            full_name = f"{name[0]['firstname']} {name[0]['middlename']} {name[0]['lastname']}"
        else:
            full_name = ''

        return JsonResponse({
            'status': 'success',
            'full_name': full_name,
            'leave_entitlement': leave_record.leave_entitlement,
            'leaves_availed': leave_record.leaves_availed,
            'leave_balance': leave_record.leave_balance
        })

    except EmployeeLeave.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'No leave record found for this employee.'
        })







def save_emp_bnk_details(request):
    if request.method == 'POST':
        try:
            employee_id = request.POST.get('employee_id')

            pan_card_number = request.POST.get('pan_card_number')
            acc_holder_name = request.POST.get('acc_holder_name')
            acc_no = request.POST.get('acc_no')
            IFSC = request.POST.get('IFSC')
            bnk_name = request.POST.get('bnk_name')

            employee = Employees.objects.get(id=employee_id)

            if employee.pan_num:
                if pan_card_number:
                    employee.pan_num = pan_card_number
            else:
                employee.pan_num = pan_card_number

            employee.save()

            save_details, created = BankDetails.objects.update_or_create(employee=employee)

            save_details.acc_holder_name = acc_holder_name
            save_details.account_num = acc_no
            save_details.ifsc = IFSC
            save_details.bank_name = bnk_name

            save_details.save()

            return JsonResponse({'status': 'success', 'message': 'Bank details Added successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})


def get_emp_bnk_details(request):
    if request.method == 'GET':
        try:
            employee_id = request.GET.get('employee_id')
            if not employee_id:
                return JsonResponse({'status': 'failed', 'message': 'Employee ID not provided.'})

            save_details = Employees.objects.filter(id=employee_id).first()

            if not save_details:
                return JsonResponse({'status': 'failed', 'message': 'Employee not found.'})

            bnk_details = BankDetails.objects.filter(employee_id=employee_id).values().first()

            if bnk_details:
                employee_data = {
                    "id": save_details.id,
                    "pan_num": save_details.pan_num,
                }

                return JsonResponse({
                    'status': 'success',
                    'save_details': employee_data,
                    'bnk_details': bnk_details
                })
            else:
                return JsonResponse({'status': 'failed', 'message': 'Bank details not found.'})

        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed', 'message': 'An error occurred: ' + str(e)})

    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method.'})