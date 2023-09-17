from ast import If
from itertools import count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from datetime import date
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from employee.forms import *
from leave.models import *
from employee.models import *
from leave.forms import LeaveCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


# from attendance.models import Attendance

# from leave.forms import CommentForm


@login_required(login_url='/')
def dashboard(request):
	
	'''
	Summary of all apps - display here with charts etc.
	eg.lEAVE - PENDING|APPROVED|RECENT|REJECTED - TOTAL THIS MONTH or NEXT MONTH
	EMPLOYEE - TOTAL | GENDER 
	CHART - AVERAGE EMPLOYEE AGES
	'''
	dataset = dict()
	user = request.user

	if not request.user.is_authenticated:
		return redirect('accounts:login')

	employees = Employee.objects.all()
	leaves = Leave.objects.all_pending_leaves()
	employees_birthday = Employee.objects.birthdays_current_month()
	staff_leaves = Leave.objects.filter(user = user)

	
	dataset['employees'] = employees
	dataset['leaves'] = leaves
	dataset['employees_birthday'] = employees_birthday
	dataset['staff_leaves'] = staff_leaves
	dataset['title'] = 'Summary' 
	

	return render(request,'dashboard/dashboard_index.html',dataset)



@login_required(login_url='/')
def dashboard_employees(request):
	# if not (request.user.is_authenticated and request.user.is_staff):
	# 	return redirect('/')

	dataset = dict()
	departments = Department.objects.all()
	employees = Employee.objects.all()

	#pagination
	query = request.GET.get('search')
	if query:
		employees = employees.filter(
			Q(firstname__icontains = query) |
			Q(lastname__icontains = query) |
			Q(reporting_to__icontains = query)
		)


	paginator = Paginator(employees, 10) #show 10 employee lists per page

	page = request.GET.get('page')
	employees_paginated = paginator.get_page(page)


	dataset['employee_list'] = employees_paginated
	dataset['departments'] = departments
	dataset['all_employees'] = Employee.objects.all_employees()

	blocked_employees = Employee.objects.all_blocked_employees()

	dataset['blocked_employees'] = blocked_employees
	dataset['title'] = 'Employees List'
	return render(request,'dashboard/employee_app.html',dataset)



@login_required(login_url='/')
def dashboard_employees_create(request):
	if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
		return redirect('/')

	if request.method == 'POST':
		form = EmployeeCreateForm(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.POST.get('user')
			assigned_user = User.objects.get(id = user)

			instance.user = assigned_user 

			instance.title = request.POST.get('title')
			instance.image = request.FILES.get('image')
			instance.firstname = request.POST.get('firstname')
			instance.lastname = request.POST.get('lastname')
			instance.bio = request.POST.get('bio')
			instance.birthday = request.POST.get('birthday')

			department_id = request.POST.get('department')
			department = Department.objects.get(id = department_id)
			instance.department = department

			instance.address = request.POST.get('address')
			instance.education = request.POST.get('education')

			instance.reporting_to = request.POST.get('reporting_to')

			client_id = request.POST.get('client')
			client = Client.objects.get(id = client_id)
			instance.client = client

			designation = request.POST.get('designation')
			designation_instance = Designation.objects.get(id = designation)
			instance.Designation = designation_instance

			instance.startdate = request.POST.get('startdate')
			instance.employeetype = request.POST.get('employeetype')
			instance.employeeid = request.POST.get('employeeid')
			instance.dateissued = request.POST.get('dateissued')

			instance.save()
			
			messages.success(request,'Account Created Successfully!!',extra_tags = 'alert alert-warning alert-dismissible show')
			return  redirect('dashboard:employees')
		else:
			messages.error(request,'Trying to create dublicate employees with a single user account ',extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('dashboard:employeecreate')


	dataset = dict()
	form = EmployeeCreateForm()
	dataset['form'] = form
	dataset['title'] = 'Register Employee'
	return render(request,'dashboard/employee_create.html',dataset)


@login_required(login_url='/')
def employee_edit_data(request, id):
	if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
		return redirect('/')

	# employee = Employee.objects.get(id=id)
	employee = get_object_or_404(Employee, id = id)

	if request.method == 'POST':
		form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee, )
		
		if form.is_valid():
			instance = form.save()

			user = request.POST.get('user')
			assigned_user = User.objects.get(id = user)
			instance.user = assigned_user
			
			instance.title = request.POST.get('title')
			instance.image = request.FILES.get('image')
			instance.firstname = request.POST.get('firstname')
			instance.lastname = request.POST.get('lastname')
			instance.bio = request.POST.get('bio')
			instance.birthday = request.POST.get('birthday')

			department_id = request.POST.get('department')
			department = Department.objects.get(id = department_id)
			instance.department = department

			instance.address = request.POST.get('address')
			instance.education = request.POST.get('education')

			instance.reporting_to = request.POST.get('reporting_to')

			client_id = request.POST.get('client')
			client = Client.objects.get(id = client_id)
			instance.client = client

			designation = request.POST.get('designation')
			designation_instance = Designation.objects.get(id = designation)
			instance.Designation = designation_instance

			instance.startdate = request.POST.get('startdate')
			instance.employeetype = request.POST.get('employeetype')
			instance.employeeid = request.POST.get('employeeid')
			instance.dateissued = request.POST.get('dateissued')

			instance.save()

			messages.success(request,'Account Updated Successfully!!',extra_tags = 'alert alert-warning alert-dismissible show')
			return  redirect('dashboard:employees')
		else:
			messages.error(request,'Error Updating account',extra_tags = 'alert alert-warning alert-dismissible show')
			return HttpResponse("Form data not valid")
	
	dataset = dict()
	form = EmployeeCreateForm(request.POST or None,request.FILES or None, instance = request.user)
	dataset['form'] = form
	dataset['title'] = 'Edit - {0}'.format(employee.get_full_name)
	return render(request,'dashboard/employee_create.html',dataset)



@login_required(login_url='/')
def dashboard_employee_info(request,id):
	if not request.user.is_authenticated:
		return redirect('/')
	
	employee = get_object_or_404(Employee, id = id)
	employee_emergency_instance = Emergency.objects.filter(employee = employee).first()
	employee_family_instance = Relationship.objects.filter(employee = employee).first()
	bank_instance = Bank.objects.filter(employee = employee).first()
	
	dataset = dict()
	dataset['employee'] = employee
	dataset['emergency'] = employee_emergency_instance
	dataset['family'] = employee_family_instance
	dataset['bank'] = bank_instance
	dataset['title'] = 'Profile - {0}'.format(employee.get_full_name)
	return render(request,'dashboard/employee_detail.html',dataset)




# ------------------------- EMERGENCY --------------------------------

@login_required(login_url='/')
def dashboard_emergency_create(request):
	if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
		return redirect('/')
	if request.method == 'POST':
		form = EmergencyCreateForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			employee_id = request.POST.get('employee')

			employee_object = Employee.objects.get(id = employee_id)
			emp_name = employee_object.get_full_name
			
			instance.employee = employee_object
			instance.fullname = request.POST.get('fullname')
			instance.tel = request.POST.get('tel')
			instance.location = request.POST.get('location')
			instance.relationship = request.POST.get('relationship')

			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

			instance.save()

			messages.success(request,'Emergency Successfully Created for {0}'.format(emp_name),extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:emergencycreate')

		else:
			employee_id = request.POST.get('employee')

			employee_object = Employee.objects.get(id = employee_id)
			emp_name = employee_object.get_full_name
			messages.error(request,'Error Creating Emergency for {0}'.format(emp_name),extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('dashboard:emergencycreate')

	dataset = dict()
	form = EmergencyCreateForm()
	dataset['form'] = form
	dataset['title'] = 'Create Emergency'
	return render(request,'dashboard/emergency_create.html',dataset)



@login_required(login_url='/')
def dashboard_emergency_update(request,id):
	if not (request.user.is_authenticated and request.user.is_superuser):
		return redirect('/')

	emergency = get_object_or_404(Emergency, id = id)
	employee = emergency.employee
	if request.method == 'POST':
		form = EmergencyCreateForm( data = request.POST, instance = emergency)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.employee = employee
			instance.fullname = request.POST.get('fullname')
			instance.tel = request.POST.get('tel')
			instance.location = request.POST.get('location')
			instance.relationship = request.POST.get('relationship')

			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

			instance.save()


			messages.success(request,'Emergency Details Successfully Updated',extra_tags = 'alert alert-success alert-dismissible show')
			'''
				NB: redirect() will try to use its given arguments to reverse a URL. 
				This example assumes your URL patterns contain a pattern like this 
				redirect(assumed_url_name,its_assuemed_whatever_instance id)
			'''
			return redirect('dashboard:employeeinfo',id = employee.id)# worked on redirect to profile and message success and error

	dataset = dict()
	form = EmergencyCreateForm(request.POST or None,instance = emergency)
	dataset['form'] = form
	dataset['title'] = 'Updating Emergency Details for {0}'.format(employee.get_full_name)
	return render(request,'dashboard/emergency_create.html',dataset)





# ----------------------------- FAMILY ---------------------------------#



# YOU ARE HERE ---- creation form for Family
# def dashboard_family_create(request):
# 	if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
# 		return redirect('/')
# 	if request.method == 'POST':
# 		form = FamilyCreateForm(data = request.POST or None)
# 		if form.is_valid():
# 			instance = form.save(commit = False)
# 			employee_id = request.POST.get('employee')
# 			employee_object = get_object_or_404(Employee,id = employee_id)
# 			instance.employee = employee_object
# 			instance.status = request.POST.get('status')
# 			instance.spouse = request.POST.get('spouse')
# 			instance.occupation = request.POST.get('occupation')
# 			instance.tel = request.POST.get('tel')
# 			instance.children = request.POST.get('children')
# 			instance.father = request.POST.get('father')
# 			instance.foccupation = request.POST.get('foccupation')
# 			instance.mother = request.POST.get('mother')
# 			instance.moccupation = request.POST.get('moccupation')

# 			# now = datetime.datetime.now()
# 			# instance.created = now
# 			# instance.updated = now

# 			instance.save()

# 			messages.success(request,'Relationship Successfully Created for {0}'.format(employee_object),extra_tags = 'alert alert-success alert-dismissible show')
# 			return redirect('dashboard:familycreate')
# 		else:
# 			employee_id = request.POST.get('employee')
# 			employee_object = get_object_or_404(Employee,id = employee_id)
# 			messages.error(request,'Failed to create Relationship for {0}'.format(employee_object),extra_tags = 'alert alert-warning alert-dismissible show')
# 			return redirect('dashboard:familycreate')




# 	dataset = dict()

# 	form = FamilyCreateForm()

# 	dataset['form'] = form
# 	dataset['title'] = 'RELATIONSHIP CREATE FORM'
# 	return render(request,'dashboard/family_create_form.html',dataset)




# # HERE FAMILY EDIT
# def dashboard_family_edit(request,id):
# 	if not (request.user.is_authenticated and request.user.is_authenticated):
# 		return redirect('/')
# 	relation = get_object_or_404(Relationship, id = id)
# 	employee = relation.employee

# 	#submitted form - bound form
# 	if request.method == 'POST':
# 		form = FamilyCreateForm(data = request.POST, instance = relation)
# 		if form.is_valid():
# 			instance = form.save(commit = False)
# 			instance.employee = employee
# 			instance.status = request.POST.get('status')
# 			instance.spouse = request.POST.get('spouse')
# 			instance.occupation = request.POST.get('occupation')
# 			instance.tel = request.POST.get('tel')
# 			instance.children = request.POST.get('children')

# 			# Recently added 29/03/19
# 			instance.nextofkin = request.POST.get('nextofkin')
# 			instance.contact = request.POST.get('contact')
# 			instance.relationship = request.POST.get('relationship')

# 			instance.father = request.POST.get('father')
# 			instance.foccupation = request.POST.get('foccupation')
# 			instance.mother = request.POST.get('mother')
# 			instance.moccupation = request.POST.get('moccupation')

# 			# now = datetime.datetime.now()
# 			# instance.created = now
# 			# instance.updated = now

# 			instance.save()

# 			messages.success(request,'Relationship Successfully Updated for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
# 			return redirect('dashboard:familycreate')

# 		else:
# 			messages.error(request,'Failed to update Relationship for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
# 			return redirect('dashboard:familycreate')



# 	dataset = dict()

# 	form = FamilyCreateForm(request.POST or None,instance = relation)

# 	dataset['form'] = form
# 	dataset['title'] = 'RELATIONSHIP UPDATE FORM'
# 	return render(request,'dashboard/family_create_form.html',dataset)





# BANK 
@login_required(login_url='/')
def dashboard_bank_create(request):
	if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
		return redirect('/')
	if request.method == 'POST':
		form = BankAccountCreation(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			employee_id = request.POST.get('employee')
			employee_object = get_object_or_404(Employee,id = employee_id)

			instance.employee = employee_object
			instance.name = request.POST.get('name')
			instance.branch = request.POST.get('branch')
			instance.account = request.POST.get('account')
			instance.salary = request.POST.get('salary')

			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

			instance.save()

			messages.success(request,'Account Successfully Created for {0}'.format(employee_object.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:bankaccountcreate')
		else:
			employee_id = request.POST.get('employee')
			employee_object = get_object_or_404(Employee,id = employee_id)
			messages.error(request,'Error Creating Account for {0}'.format(employee_object.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('dashboard:bankaccountcreate')


	dataset = dict()

	form = BankAccountCreation()
	
	dataset['form'] = form
	dataset['title'] = 'Bank Account Creation Form'
	return render(request,'dashboard/bank_account_create_form.html',dataset)



@login_required(login_url='/')
def employee_bank_account_update(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	bank_instance_obj = get_object_or_404(Bank, id = id)
	employee = bank_instance_obj.employee

	if request.method == 'POST':
		form = BankAccountCreation(request.POST, instance = bank_instance_obj)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.employee = employee

			instance.name = request.POST.get('name')
			instance.branch = request.POST.get('branch')
			instance.account = request.POST.get('account')
			instance.salary = request.POST.get('salary')

			# now = datetime.datetime.now()
			# instance.created = now
			# instance.updated = now

			instance.save()

			messages.success(request,'Account Successfully Edited for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:bankaccountcreate')
		else:
			messages.error(request,'Error Updating Account for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('dashboard:bankaccountcreate')


	dataset = dict()

	form = BankAccountCreation(request.POST or None,instance = bank_instance_obj)
	
	dataset['form'] = form
	dataset['title'] = 'Update Bank Account'
	return render(request,'dashboard/bank_account_create_form.html',dataset)


@login_required(login_url='/')
def events(request):
	if not (request.user.is_authenticated and request.user.is_superuser):
		return redirect('/')
	form = EventForm(request.POST,request.FILES)

	if form.is_valid():
		event = form.save(commit=False)  #don't commit to DB
		event.user = request.user  #access the user
		event.save()   # save and commit to DB
		form = EventForm()
		
		htmly = get_template('dashboard/event_email.html')

		title = request.POST['title']
		date = request.POST['event_date']
		time = request.POST['event_time']
		place = request.POST['event_place']

		email = User.objects.all()
		recipient = []
		for user in email:
			recipient.append(user.email)

		context = { 'email': email, 'title':title, 'date':date, 'time':time, 'place':place}
		subject, from_email = 'Welcome to Zedpath', settings.EMAIL_HOST_USER
		
		html_content = htmly.render(context)
		msg = EmailMultiAlternatives(subject, html_content, from_email, recipient)
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		
		messages.info(request,'Event Created',extra_tags = 'alert alert-info alert-dismissible show' )
		return redirect('dashboard:events')

	dataset = dict()
	dataset['form'] = form
	dataset['title'] = 'Create Event'
	return render(request, 'dashboard/events.html', dataset)


@login_required(login_url='/')
def complaint_view(request):
	com = Complaint.objects.all()
	form = ComplaintForm(request.POST)
	if form.is_valid():
		complaint = form.save(commit=False)  #don't commit to DB
		complaint.user = request.user  #access the user
		complaint.save()   # save and commit to DB
		form = ComplaintForm()

		messages.success(request,'Your Complaint has been Registered', extra_tags = 'alert alert-warning alert-dismissible show' )
		return redirect('dashboard:complain')

	query = request.GET.get('search')
	if query:
		com = com.filter(Q(created__icontains = query))
		# com = com.filter(Q(user__contains=query))

	context = {
        'form': form,
		'title': 'Complain',
		'com' : com
    	} 

	return render(request, 'dashboard/complain.html', context)


@login_required(login_url='/')
def complain_detail(request, pk):
	com = Complaint.objects.get(pk=pk)
	return render(request, 'dashboard/complain_detail.html', {'com': com, })


@login_required(login_url='/')
def policy(request):
	return render(request, 'dashboard/policy.html') 



#######################################################################
# -----------------------------LEAVE-----------------------------------
#######################################################################


@login_required(login_url='/')
def leave_creation(request):
	if not request.user.is_authenticated:
		return redirect('accounts:login')
	user = request.user
	my_user = Leave.objects.filter(user=user)
	list1 = []
	for user in my_user:
		user_leave = user.leave_days
		list1.append(user_leave)
	count_leaves = sum(list1)

	# if count_leaves <= 30:
	if request.method == 'POST':
		form = LeaveCreationForm(data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			user = request.user
			instance.user = user
			instance.save()


			# print(instance.defaultdays)
			messages.success(request,'Leave Request Sent,wait for Human Resource Managers response',extra_tags = 'alert alert-success alert-dismissible show')
			return redirect('dashboard:createleave')

		messages.error(request,'failed to Request a Leave,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
		return redirect('dashboard:createleave')
	# else:
	# 	messages.info(request,'You have reached your leave limit',extra_tags = 'alert alert-warning alert-dismissible show')
	# 	# return redirect('dashboard:createleave')
		


	dataset = dict()
	form = LeaveCreationForm()
	dataset['count_leaves'] = count_leaves
	dataset['form'] = form
	dataset['title'] = 'Apply for Leave'
	return render(request,'dashboard/create_leave.html',dataset)
	# return HttpResponse('leave creation form')



@login_required(login_url='/')
def leaves_list(request):
	if not (request.user.is_staff and request.user.is_superuser):
		return redirect('/')
	leaves = Leave.objects.all_pending_leaves()
	return render(request,'dashboard/leaves_recent.html',{'leave_list':leaves,'title':'Leaves List - Pending'})


@login_required(login_url='/')
def leaves_approved_list(request):
	if not (request.user.is_superuser and request.user.is_staff):
		return redirect('/')
	leaves = Leave.objects.all_approved_leaves() #approved leaves -> calling model manager method
	return render(request,'dashboard/leaves_approved.html',{'leave_list':leaves,'title':'Approved Leave List'})


@login_required(login_url='/')
def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/')

	leave = get_object_or_404(Leave, id = id)
	employee = Employee.objects.filter(user = leave.user)[0]
	print("#########")
	print(employee)
	print("#########")
	return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(leave.user.username,leave.status)})

@login_required(login_url='/')
def approve_leave(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	user = leave.user
	employee = Employee.objects.filter(user = user)[0]
	# emp = Employee.objects.all()
	leave.approve_leave

	messages.info(request,'Leave successfully approved for {0} '.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:userleaveview', id = id)

@login_required(login_url='/')
def cancel_leaves_list(request):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leaves = Leave.objects.all_cancel_leaves()
	return render(request,'dashboard/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel Leave List',})


@login_required(login_url='/')
def unapprove_leave(request,id):
	if not (request.user.is_authenticated and request.user.is_superuser):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.unapprove_leave
	return redirect('dashboard:leaveslist') #redirect to unapproved list



@login_required(login_url='/')
def cancel_leave(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.leaves_cancel

	messages.success(request,'Leave is canceled',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
@login_required(login_url='/')
def uncancel_leave(request,id):
	if not (request.user.is_superuser and request.user.is_authenticated):
		return redirect('/')
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


@login_required(login_url='/')
def leave_rejected_list(request):

	dataset = dict()
	leave = Leave.objects.all_rejected_leaves()

	dataset['leave_list_rejected'] = leave
	return render(request,'dashboard/rejected_leaves_list.html',dataset)


@login_required(login_url='/')
def reject_leave(request,id):
	dataset = dict()
	leave = get_object_or_404(Leave, id = id)
	leave.reject_leave
	messages.success(request,'Leave is rejected',extra_tags = 'alert alert-success alert-dismissible show')
	return redirect('dashboard:leavesrejected')

	# return HttpResponse(id)

@login_required(login_url='/')
def unreject_leave(request,id):
	leave = get_object_or_404(Leave, id = id)
	leave.status = 'pending'
	leave.is_approved = False
	leave.save()
	messages.success(request,'Leave is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')

	return redirect('dashboard:leavesrejected')



# Zedpath staffs leaves table user only
@login_required(login_url='/')
def view_my_leave_table(request):
	# work on the logics
	if request.user.is_authenticated:
		user = request.user
		leaves = Leave.objects.filter(user = user)
		employee = Employee.objects.filter(user = user).first() 
		m = Leave.objects.filter(user=user)
		b= []
		for n in m:
			c = n.leave_days
			b.append(c)
		count_leaves = sum(b)
		leave_left = DAYS - count_leaves

		dataset = dict()
		dataset['count_leaves'] = count_leaves
		dataset['leave_left'] = leave_left
		dataset['leave_list'] = leaves
		dataset['employee'] = employee
		dataset['title'] = 'Leaves List'
	else:
		return redirect('accounts:login')
	return render(request,'dashboard/staff_leaves_table.html',dataset , )



# Birthday
@login_required(login_url='/')
def birthday_this_month(request):	
	if not request.user.is_authenticated:
		return redirect('/')

	employees = Employee.objects.birthdays_current_month()
	month = date.today().strftime('%B')#am using this to get the month for template rendering- making it dynamic
	context = {
	'birthdays':employees,
	'month':month,
	'count_birthdays':employees.count(),
	'title':'Birthdays'
	}
	return render(request,'dashboard/birthdays_this_month.html',context)


# def show_attendance(request):
	
# 	return render(request,'dashboard/attendance_table.html')

# def attendance_creation(request):
	
# 	return render(request,'dashboard/mark_attendance.html')