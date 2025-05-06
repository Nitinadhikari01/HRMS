from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee_information.models import Employees, Department, Position, EmployeeLeave, Holiday


# Create your views here.

@login_required
def employee_dashboard(request):
    employee_list = Employees.objects.filter(emp_code=request.user)

    if not employee_list.exists():
        return render(request, '404_error.html')

    employee = employee_list.first()

    leave_record = EmployeeLeave.objects.filter(employee_id=employee.id).first()
    latest_pdf = Holiday.objects.order_by('-id').first()

    context = {
        'page_title': 'Employees Dashboard',
        'employees': employee_list,
        'leave_entitlement': leave_record.leave_entitlement if leave_record else 0,
        'leaves_availed': leave_record.leaves_availed if leave_record else 0,
        'leave_balance': leave_record.leave_balance if leave_record else 0,
        'latest_pdf': latest_pdf,
    }

    if request.user.groups.filter(name='Employee').exists():
        return render(request, 'employee_dashboard.html', context)
    else:
        return render(request, '404_error.html')





@login_required
def employee_details(request):
    employee = {}
    departments = Department.objects.all()
    positions = Position.objects.all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'departments': departments,
        'positions': positions
    }
    if request.user.groups.filter(name='Employee').exists():
        return render(request, 'employee_details.html', context)
    return render(request, '404_error.html')