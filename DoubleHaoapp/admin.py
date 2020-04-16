from django.contrib import admin

# Register your models here.
from DoubleHaoapp.models import Student, PersonalInformation


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['pk', 'Sid', 'Spassword']

@admin.register(PersonalInformation)
class StudentAdmin(admin.ModelAdmin):
    list_per_page = 10
