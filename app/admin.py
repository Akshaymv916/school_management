from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, LibraryHistory, FeeHistory


# Customize User admin
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id','username', 'email', 'first_name', 'last_name', 'user_type', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


# Customize Student admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'roll_number', 'class_name', 'user')
    search_fields = ('name', 'roll_number', 'class_name')
    list_filter = ('class_name',)


# Customize LibraryHistory admin
class LibraryHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','book_name', 'student', 'borrow_date', 'return_date', 'status')
    search_fields = ('book_name', 'student__name')
    list_filter = ('status', 'borrow_date', 'return_date')
    ordering = ('-borrow_date',)


# Customize FeeHistory admin
class FeeHistoryAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'fee_type', 'amount', 'payment_date', 'remarks', 'created_at', 'updated_at')
    search_fields = ('student__name', 'fee_type', 'remarks')
    list_filter = ('fee_type', 'payment_date')
    ordering = ('-payment_date',)


# Register models with admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(LibraryHistory, LibraryHistoryAdmin)
admin.site.register(FeeHistory, FeeHistoryAdmin)
