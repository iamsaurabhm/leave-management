from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class UserAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username', 'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email@gmail.com', 'class':'form-control'}))
	# password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))
	# password_confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password', 'class':'form-control'}))


	def __init__(self, *args, **kwargs):
		super(UserAddForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			if field.widget.attrs.get('class'):
				field.widget.attrs['class'] += ' form-control'
				field.widget.attrs['class'] += ' placeholder'
			else:
				field.widget.attrs['class'] = 'form-control'
				field.widget.attrs['placeholder'] = 'password'

	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		

	def clean_email(self):
		email = self.cleaned_data['email']
		qry = User.objects.filter(email = email)

		domain_list = ['gmail.com']
		get_zedpath_domain = email.split('@')[1]#get me whatever after @, eg. gmail.com

		print(get_zedpath_domain in domain_list)

		if qry.exists():
			'''
			True - Queryset exist run validation message here
			'''
			raise forms.ValidationError('email {0} already exists'.format(email))


		elif get_zedpath_domain not in domain_list:
			print('test - not in domain')
			raise forms.ValidationError('email does not contain domain')

		return email


class UserLogin(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))


