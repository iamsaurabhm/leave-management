from django.contrib import admin
from employee.models import *
import datetime
import calendar
from django.urls import reverse
from django.utils.safestring import mark_safe
# from .utils import EventCalendar


admin.site.register(Designation)
admin.site.register(Department)
# admin.site.register(Nationality)
# admin.site.register(Religion)
admin.site.register(Employee)
admin.site.register(Bank)
admin.site.register(Emergency)
admin.site.register(Relationship)
admin.site.register(Event)
admin.site.register(Complaint)
admin.site.register(Client)


# class ComplaintAdmin(admin.ModelAdmin):
#     model = Complaint
#     list_display = ['user']
#     search_fields = ['user']
# admin.site.register(Complaint, ComplaintAdmin)


