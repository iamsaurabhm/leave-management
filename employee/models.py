import csv
from datetime import date
import datetime
from employee.utility import code_format
from django.db import models
from employee.managers import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# import os
# from twilio.rest import Client

# Create your models here.
class Designation(models.Model):
    '''
        Designation Table eg. Staff,Manager,H.R ...
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Designation')
        verbose_name_plural = _('Designations')
        ordering = ['name','created']


    def __str__(self):
        return self.name


class Department(models.Model):
    '''
     Department Employee belongs to. eg. Transport, Engineering.
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name','created']
    
    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=125)
    flag = models.ImageField(null=True,blank=True)#work on path

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationality')
        ordering = ['name','created']

    def __str__(self):
        return self.name


class Religion(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
    
    class Meta:
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')
        ordering = ['name','created']

    def __str__(self):
        return self.name




class Bank(models.Model):
    # access table: employee.bank_set.
    employee = models.ForeignKey('Employee',help_text='select employee(s) to add bank account',on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
    account = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
    branch = models.CharField(_('Branch'),help_text='which branch was the account issue',max_length=125,blank=True,null=True)
    salary = models.DecimalField(_('Starting Salary'),help_text='This is the initial salary of employee',max_digits=16, decimal_places=2,null=True,blank=False)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')
        ordering = ['-name','-account']


    def __str__(self):
        return ('{0}'.format(self.name))






class Emergency(models.Model):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    EMERGENCY_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )


    # access table: employee.emergency_set.
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    fullname = models.CharField(_('Fullname'),help_text='who should we contact ?',max_length=255,null=True,blank=False)
    tel = PhoneNumberField(default='+910000000000', null = False, blank=False, verbose_name='Phone Number (Example +910000000000)', help_text= 'Enter number with Country Code Eg. +910000000000')
    location = models.CharField(_('Place of Residence'),max_length= 125,null=True,blank=False)
    relationship = models.CharField(_('Relationship with Person'),help_text='Who is this person to you ?',max_length=8,default=FATHER,choices=EMERGENCY_RELATIONSHIP,blank=False,null=True)


    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergency'
        ordering = ['-created']


    def __str__(self):
        return self.fullname

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)








class Relationship(models.Model):
    MARRIED = 'Married'
    SINGLE = 'Single'
    DIVORCED = 'Divorced'
    WIDOW = 'Widow'
    WIDOWER = 'Widower'

    STATUS = (
    (MARRIED,'Married'),
    (SINGLE,'Single'),
    (DIVORCED,'Divorced'),
    (WIDOW,'Widow'),
    (WIDOWER,'Widower'),
    )

    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    NEXTOFKIN_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )




    # access table: employee.relationship_set.or related_name = 'relation' employee.relation.***
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(_('Marital Status'),max_length=10,default=SINGLE,choices=STATUS,blank=False,null=True)
    spouse = models.CharField(_('Spouse (Fullname)'),max_length=255,blank=True,null=True)
    occupation = models.CharField(_('Occupation'),max_length=125,help_text='spouse occupation',blank=True,null=True)
    tel = PhoneNumberField(default=None, null = True, blank=True, verbose_name='Spouse Phone Number (Example +233240000000)', help_text= 'Enter number with Country Code Eg. +233240000000')
    children = models.PositiveIntegerField(_('Number of Children'),null=True,blank=True,default=0)

    #recently added - 29/03/19
    nextofkin = models.CharField(_('Next of Kin'),max_length=255,blank=False,null=True,help_text='fullname of next of kin')
    contact = PhoneNumberField(verbose_name='Next of Kin Phone Number (Example +233240000000)',null=True,blank=True,help_text='Phone Number of Next of Kin')
    relationship = models.CharField(_('Relationship with Next of Person'),help_text='Who is this person to you ?',max_length=15,choices=NEXTOFKIN_RELATIONSHIP,blank=False,null=True)
    
    # close recent

    father = models.CharField(_('Father\'s Name'),max_length=255,blank=True,null=True)
    foccupation = models.CharField(_('Father\'s Occupation'),max_length=125,help_text='',blank=True,null=True)

    mother = models.CharField(_('Mother\'s Name'),max_length=255,blank=True,null=True)
    moccupation = models.CharField(_('Mother\'s Occupation'),max_length=125,help_text='',blank=True,null=True)


    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'
        ordering = ['created']


    def __str__(self):
        if self.status == 'Married':
            return self.spouse
        return self.status



class Client(models.Model):
    client = models.CharField(max_length=100)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['client','-created']
    
    def __str__(self):
        return self.client


class Employee(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    (NOT_KNOWN,'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
    (MR,'Mr'),
    (MRS,'Mrs'),
    (MSS,'Mss'),
    (DR,'Dr'),
    (SIR,'Sir'),
    (MADAM,'Madam'),
    )


    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
        (FULL_TIME,'Full-Time'),
        (PART_TIME,'Part-Time'),
        (CONTRACT,'Contract'),
        (INTERN,'Intern'),
    )


    SELECT = 'Select'
    HIGHSCHOOL = 'High School'
    INTERMEDIATE = 'Intermediate'
    GRADUATION = 'Graduation'
    POSTGRADUATION = 'Post Graduation'

    EDUCATIONAL_LEVEL = (
        (SELECT,'Select'),
        (HIGHSCHOOL,'High School'),
        (INTERMEDIATE,'Intermediate'),
        (GRADUATION,'Graduation'),
        (POSTGRADUATION, 'Post Graduation')
    )

    SELECT = "Select"

    REGIONS = ( ("SELECT","Select"),
                ("Andhra Pradesh","Andhra Pradesh"),
                ("Arunachal Pradesh","Arunachal Pradesh "),
                ("Assam","Assam"),
                ("Bihar","Bihar"),
                ("Chhattisgarh","Chhattisgarh"),
                ("Goa","Goa"),
                ("Gujarat","Gujarat"),
                ("Haryana","Haryana"),
                ("Himachal Pradesh","Himachal Pradesh"),
                ("Jammu and Kashmir ","Jammu and Kashmir "),
                ("Jharkhand","Jharkhand"),
                ("Karnataka","Karnataka"),
                ("Kerala","Kerala"),
                ("Madhya Pradesh","Madhya Pradesh"),
                ("Maharashtra","Maharashtra"),
                ("Manipur","Manipur"),
                ("Meghalaya","Meghalaya"),
                ("Mizoram","Mizoram"),
                ("Nagaland","Nagaland"),
                ("Odisha","Odisha"),
                ("Punjab","Punjab"),
                ("Rajasthan","Rajasthan"),
                ("Sikkim","Sikkim"),
                ("Tamil Nadu","Tamil Nadu"),
                ("Telangana","Telangana"),
                ("Tripura","Tripura"),
                ("Uttar Pradesh","Uttar Pradesh"),
                ("Uttarakhand","Uttarakhand"),
                ("West Bengal","West Bengal"),
                ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
                ("Chandigarh","Chandigarh"),
                ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
                ("Daman and Diu","Daman and Diu"),
                ("Lakshadweep","Lakshadweep"),
                ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
                ("Puducherry","Puducherry"))


    SELECT = "Select"
    AKSHAY = 'Akshay'
    AVNI = 'Avni'
    SANDEEP = 'Sandeep'

    REPORTING_TO = (
    (SELECT,"Select"),
    (AKSHAY,'Akshay'),
    (AVNI,'Anvi'),
    (SANDEEP,'Sandeep'),
    )


    # PERSONAL DATA
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    title = models.CharField(_('Title'),max_length=20,default=MR,choices=TITLE,blank=False,null=True)
    image = models.FileField(_('Profile Image'),upload_to='profiles',default='',blank=True,null=True,help_text='upload image size less than 2.0MB')#work on path username-date/image
    firstname = models.CharField(_('Firstname'),max_length=125,null=False,blank=False)
    lastname = models.CharField(_('Lastname'),max_length=125,null=False,blank=False)
    # othername = models.CharField(_('Othername (optional)'),max_length=125,null=True,blank=True)
    # sex = models.CharField(_('Gender'),max_length=20,default=MALE,choices=GENDER,blank=False)
    email = models.CharField(_('Email'),max_length=255,default=None,blank=False,null=True)
    alter_email = models.CharField(_('Alternate Email'),max_length=255,default=None,blank=False,null=True)
    tel = PhoneNumberField(default='', null = False, blank=False, verbose_name='Phone Number (Example +91-0000000000)', help_text= 'Enter number with Country Code Eg. +91-0000000000')
    bio = models.CharField(_('Bio'),help_text='your biography,tell me something about yourself eg. i love working ...',max_length=255,default='',null=True,blank=True)
    birthday = models.DateField(_('Birthday'),blank=False,null=False)
    address = models.CharField(_('Address'),help_text='address of current residence',max_length=125,null=True,blank=True)  
    education = models.CharField(_('Education'),help_text='highest educational standard ie. your last level of schooling',max_length=20,default=SELECT,choices=EDUCATIONAL_LEVEL,blank=False,null=True)
    reporting_to = models.CharField(_('Reporting to'),help_text='your reporting manager',max_length=20,default=SELECT,choices=REPORTING_TO,blank=False,null=True)
        
    # COMPANY DATA
    client = models.ForeignKey(Client,verbose_name =_('Client'),on_delete=models.SET_NULL,null=True,default=None )
    department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
    designation =  models.ForeignKey(Designation,verbose_name =_('Designation'),on_delete=models.SET_NULL,null=True,default=None)
    startdate = models.DateField(_('Employement Date'),help_text='date of employement',blank=False,null=True)
    employeetype = models.CharField(_('Employee Type'),max_length=15,default=FULL_TIME,choices=EMPLOYEETYPE,blank=False,null=True)
    employeeid = models.CharField(_('Employee ID Number'),max_length=10,null=True,blank=True)
    dateissued = models.DateField(_('Date Issued'),help_text='date staff id was issued',blank=False,null=True)

    #app related
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)
 
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    #PLUG MANAGERS
    objects = EmployeeManager()

    
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']



    def __str__(self):
        return self.get_full_name

    

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        # othername = self.othername

        if (firstname and lastname) is None:
            fullname = firstname +' '+ lastname
            return fullname
        else:
            fullname = firstname + ' '+ lastname
            return fullname
        


    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return



    @property
    def can_apply_leave(self):
        pass


    @property
    def get_pretty_birthday(self):
        if self.birthday:
            return self.birthday.strftime('%A,%d %B') # Thursday,04 May -> staffs age privacy
        return


    @property
    def birthday_today(self):
        '''
        returns True, if birthday is today else False
        '''
        return self.birthday.day == date.today().day



    @property
    def days_check_date_fade(self):
        '''
        Check if Birthday has already been celebrated ie in the Past     ie. 4th May  & today 8th May 4 < 8 -> past else present or future '''
        return self.birthday.day < date.today().day #Assumption made,If that day is less than today day,in the past




    def birthday_counter(self):
        '''
        This method counts days to birthday -> 2 day's or 1 day
        '''
        today = date.today()
        current_year = today.year

        birthday = self.birthday # eg. 5th May 1995

        future_date_of_birth = date(current_year,birthday.month,birthday.day)#assuming born THIS YEAR ie. 5th May 2019

        if birthday:
            if (future_date_of_birth - today).days > 1:

                return str((future_date_of_birth - today).days) + ' day\'s'

            else:

                return ' tomorrow'

        return





    def save(self,*args,**kwargs):
        '''
        overriding the save method - for every instance that calls the save method 
        perform this action on its employee_id
        added : March, 03 2019 - 11:08 PM

        '''
        get_id = self.employeeid #grab employee_id number from submitted form field
        data = code_format(get_id)
        self.employeeid = data #pass the new code to the employee_id as its orifinal or actual code
        super().save(*args,**kwargs) # call the parent save method
        # print(self.employeeid)


class Event(models.Model):
    title = models.CharField(max_length=100)
    event_date = models.DateField(null=True, blank=True, auto_now=False,auto_now_add=False)
    event_time = models.TimeField(null=True, auto_now_add=False, auto_now=False)
    event_place = models.CharField(max_length=500, default='')
    # desc = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-created']
        managed = True

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     account_sid = 'AC8b85dc7c94ed62efd957ba1ae711109f'
    #     auth_token = '4a91a810ed0108dc0f2ad84cf517a02e'
    #     client = Client(account_sid, auth_token)

    #     # Open the people CSV and get all the numbers out of it
    #     number = 'employee/phones.csv'
    #     with open(number, 'r') as csvfile:
    #         numbers = csvfile.readlines()
    #         # numbers = set([p[0] for p in peoplereader]) # remove duplicate numbers
        
    #     for num in numbers:
    #     # Send the sms text to the number from the CSV file:
    #         print("Sending to " + num)
		
    #     message = client.messages.create(
    #                  body=f"{self.title} on {self.event_date} , {self.event_time}  at {self.event_place}",
    #                  from_='+18596952727',
    #                  to=num
    #              )
    #     # print("############")
    #     return super().save(*args, **kwargs)



class Complaint(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    complaint = models.TextField(max_length=1000, default='')
    created = models.DateTimeField(auto_now_add=True,  null=True)
    # switch_schedule_yes_or_no = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) 

    class Meta:
        ordering = ['-created']