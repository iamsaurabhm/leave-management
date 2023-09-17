from urllib import request
from django import forms
from django.conf import settings
from employee.models import *
from django.contrib.auth.models import User

 
# EMPLOYEE
class EmployeeCreateForm(forms.ModelForm):
	employeeid = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'please enter 5 characters without ZP or slashes eg. A0025'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))
	
	class Meta:
		model = Employee
		exclude = ['is_blocked','is_deleted','created','updated']
		widgets = {
				'bio':forms.Textarea(attrs={'cols':5,'rows':5})
		}


	# def clean_user(self):
	# 	user = self.cleaned_data['user'] #returns <User object>,not id as in [views <-> templates]

	# 	qry = Employee.objects.filter(user = user)#check, whether any employee exist with username - avoid duplicate users - > many employees
	# 	if qry:
	# 		raise forms.ValidationError('Employee exists with username already')
	# 	return user



class EmergencyCreateForm(forms.ModelForm):

	class Meta:
		model = Emergency
		fields = ['employee','fullname','tel','location','relationship']





# FAMILY

class FamilyCreateForm(forms.ModelForm):

	class Meta:
		model = Relationship
		fields = ['employee','status','spouse','occupation','tel','children','nextofkin','contact','relationship','father','foccupation','mother','moccupation']



class BankAccountCreation(forms.ModelForm):

	class Meta:
		model = Bank
		fields = ['employee','name','branch','account','salary']



class ComplaintForm(forms.ModelForm):

	user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
	complaint = forms.Textarea()
    # switch_schedule_yes_or_no = forms.BooleanField()
    
	class Meta:
		model = Complaint 
		fields = ['user', 'complaint',]


	
# from django.forms import DateField

class EventForm(forms.ModelForm):
	# event_date = DateField(input_formats=settings.DATE_INPUT_FORMATS,widget=forms.widgets.DateInput(attrs={'class': 'form-control datepicker',}))
	class Meta:
		model = Event
		fields = ['title', 'event_date', 'event_time', 'event_place']
 
		labels = {'title': 'Title', 'event_date': 'Event Date',
                  'event_time': 'Event Time', 'event_place':'Event Place'}

		widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}),
            'event_date': forms.DateInput(attrs={'class': 'form-control datepicker',}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control timepicker',}),
			'event_place': forms.TextInput(attrs={'class': 'form-control',}),
            # 'desc': forms.Textarea(attrs={'class': 'form-control',}),
		}


class ClientCreateForm(forms.ModelForm):

	class Meta:
		model = Client
		fields = ['client', 'description']

# def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
       
#         self.fields['email'].widget.attrs.update(
#             {'placeholder': ('Email')})
#         self.fields['address'].widget.attrs.update(
#             {'placeholder': ('Address')})
#         self.fields['phonenumber'].widget.attrs.update(
#             {'placeholder': ('Phone number')})
#         self.fields['first_name'].widget.attrs.update(
#             {'placeholder': ('First name')})
#         self.fields['last_name'].widget.attrs.update(
#             {'placeholder': ('Last name')})
