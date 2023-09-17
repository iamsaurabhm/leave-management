from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from employee.models import *
from hrsuit import settings
from .forms import UserLogin,UserAddForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


@login_required(login_url='/')
def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/')
	'''
	Please work on me -> success & error messages & style templates
	'''
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request,user)

			messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('accounts:changepassword')
		else:
			messages.error(request,'Error,changing password',extra_tags = 'alert alert-warning alert-dismissible show' )
			return redirect('accounts:changepassword')
			
	form = PasswordChangeForm(request.user)
	return render(request,'accounts/change_password_form.html',{'form':form})




def register_user_view(request):
	# WORK ON (MESSAGES AND UI) & extend with email field
	if request.method == 'POST':
		form = UserCreationForm(data = request.POST)
		if form.is_valid():
			# instance = form.save(commit = False)
			# instance.is_active = False  
			# instance.save()
			username = request.POST['username']
			password = request.POST['password1']
			email = request.POST['email']
			
			user = User.objects.create_user(username=username, email=email, password=password)
			user.save()

			# link = '127.0.0.1:8000'
			# subject = 'Welcome to Zedpath'
			# message = f'Hi {username}, You have been added to Zedpath Staff List. You can login by clicking on the given link. You Username: {username} and Password: {password}'
			# email_from = settings.EMAIL_HOST_USER
			# recipient_list = [email, ]
			# send_mail( subject, message, email_from, recipient_list, fail_silently = False )

			 
			htmly = get_template('accounts/email.html')

			context = { 'username': username, 'password':password }

			subject, from_email = 'Welcome to Zedpath', settings.EMAIL_HOST_USER
			recipient = [email]
			html_content = htmly.render(context)
			msg = EmailMultiAlternatives(subject, html_content, from_email, recipient)
			msg.attach_alternative(html_content, "text/html")
			msg.send()

			messages.success(request,'Account created for {0}!!!'.format(username),extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('accounts:register')
		else:
			messages.error(request,'Username or password is invalid',extra_tags = 'alert alert-warning alert-dismissible show')
			return redirect('accounts:register')


	form = UserAddForm()
	dataset = dict()
	dataset['form'] = form
	dataset['title'] = 'Register'
	return render(request,'accounts/register.html',dataset)




def login_view(request):
	
	form = UserLogin()
	login_user = request.user

	# user will redirect to home page if already login
	if request.user.is_authenticated:
		return redirect('dashboard:dashboard')

	if request.method == 'POST':
		form = UserLogin(data = request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username = username, password = password)
			
			if user and user.is_active:
				login(request,user)
				if user.is_authenticated:
					return redirect('dashboard:dashboard')
			else:
				messages.error(request,'Account is invalid',extra_tags = 'alert alert-error alert-dismissible show' )
				return redirect('accounts:login')
		else:
			return HttpResponse('data not valid')
 
	dataset=dict()
	form = UserLogin()

	dataset['form'] = form
	return render(request,'accounts/login.html',dataset)

@login_required(login_url='/')
def user_profile_view(request):
	'''
	user profile view -> staffs (No edit) only admin/HR can edit.
	'''
	user = request.user
	if user.is_authenticated:
		employee = Employee.objects.filter(user = user).first()
		emergency = Emergency.objects.filter(employee = employee).first()
		relationship = Relationship.objects.filter(employee = employee).first()
		bank = Bank.objects.filter(employee = employee).first()

		dataset = dict()
		dataset['employee'] = employee
		dataset['emergency'] = emergency
		dataset['family'] = relationship
		dataset['bank'] = bank
		dataset['title'] = 'Profile'

		return render(request,'dashboard/employee_detail.html',dataset)
	return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")



def logout_view(request):
	logout(request)
	return redirect('accounts:login')


@login_required(login_url='/')
def users_list(request):
	employees = Employee.objects.all()
	return render(request,'accounts/users_table.html',{'employees':employees,'title':'Users List'})

@login_required(login_url='/')
def users_unblock(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()

	emp.is_blocked = False
	emp.save()

	user.is_active = True
	user.save()

	return redirect('accounts:users')

@login_required(login_url='/')
def users_block(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()

	emp.is_blocked = True
	emp.save()
	
	user.is_active = False
	user.save()
	
	return redirect('accounts:users')


@login_required(login_url='/')
def users_blocked_list(request):
	blocked_employees = Employee.objects.all_blocked_employees()
	return render(request,'accounts/all_blocked_users.html',{'employees':blocked_employees,'title':'blocked users list'})