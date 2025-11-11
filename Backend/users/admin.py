from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmailVerification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Additional", {'fields': ('field_of_interest', 'bio', 'campus_verified')}),
    )
    list_display = ('username', 'email', 'field_of_interest', 'campus_verified', 'is_staff', 'is_active')


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    model = EmailVerification
    list_display = ('user', 'otp_code', 'created_at', 'is_verified')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at',)