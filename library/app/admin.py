
from django.contrib import admin
from .models import *
from app.forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User role',
            {
                'fields': (
                    'email_verified',
                )
            }
        )
    )

class BookSearchAdmin(admin.ModelAdmin):
    list_display = ('Book_Title','Binding_Id',"Publication_year","price","Isbn10","Isbn13")
    search_fields = ('Book_Title',"Binding_Id__Author","Publication_year","price","Isbn10","Isbn13")
    list_filter = ("Publication_year","Category_Type","rating",)
    list_per_page = 20

class BindingAdmin(admin.ModelAdmin):
    list_display = ('Binding_Name',"Author")
    
    
    



admin.site.register(Book_Details,BookSearchAdmin)
admin.site.register(Borrower_Details)
admin.site.register(Category_Details)
admin.site.register(Shelf_Details)
admin.site.register(Binding_Details,BindingAdmin)
admin.site.register(Authe)
admin.site.register(College)
admin.site.register(student_detaiels)
admin.site.register(Testimonials)
admin.site.register(User, CustomUserAdmin)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton

# class EmployeeInline(admin.StackedInline):
#     model = User
#     can_delete = False
#     verbose_name_plural = 'employee'

# # Define a new User admin


# class UserAdmin(BaseUserAdmin):
#     inlines = (EmployeeInline,)


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
