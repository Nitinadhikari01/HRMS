from django.shortcuts import render
from django.http import HttpResponse
from employee_information.models import Department, Position, Employees, Holiday, EmployeeLeave
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.cache import cache_control


# ---------------------------- VIEW STARTS FOR THE DEPARTMENT
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def departments_list(request):
    department_list = Department.objects.all()
    context = {
        'page_title': 'Departments',
        'departments': department_list,
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'departments.html', context)
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
def manage_departments(request):
    department = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            department = Department.objects.filter(id=id).first()

    context = {
        'department': department
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'manage_department.html', context)
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
def save_department(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            Department.objects.filter(id=data['id']).update(name=data['name'], hod=data['hod'])
            resp['msg'] = 'Department Updated Successfully'
        else:
            save_department = Department(name=data['name'], hod=data['hod'])
            save_department.save()
            resp['msg'] = 'Department Saved Successfully'
        resp['status'] = 'success'

    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_department(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Department.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# ---------------------------- VIEW END FOR THE DEPARTMENT



# ---------------------------- VIEW STARTS FOR THE DESIGNATION
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def designation_list(request):
    position_list = Position.objects.all()
    context = {
        'page_title': 'Designations',
        'positions': position_list,
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'positions.html', context)
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
def manage_designations(request):
    position = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            position = Position.objects.filter(id=id).first()

    context = {
        'position': position
    }
    if not request.user.groups.filter(name='Employee').exists():
        return render(request, 'manage_position.html', context)
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
def save_designation(request):
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_position = Position.objects.filter(id=data['id']).update(name=data['name'])
            resp['msg'] = 'Designation Updated Successfully'
        else:
            save_position = Position(name=data['name'])
            save_position.save()
            resp['msg'] = 'Designation Saved Successfully'
        resp['status'] = 'success'

    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_designation(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Position.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# ---------------------------- VIEW END FOR THE DESIGNATION

