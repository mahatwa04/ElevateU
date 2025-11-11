from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	fieldsets = UserAdmin.fieldsets + (
		("Additional", {'fields': ('field_of_interest', 'bio', 'campus_verified')}),
	)
	list_display = ('username', 'email', 'field_of_interest', 'campus_verified', 'is_staff', 'is_active')
