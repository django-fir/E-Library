
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from app.models import User
from django.db.models import Q
from app.models import student_detaiels


class User_Login(AuthenticationForm):
    username = forms.CharField(label="UserName/Email",
                               widget=forms.EmailInput(attrs={'class': "form-control form-control-lg", 'id': "yourUsername", 'placeholder': "Enter Email OR UserName"}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': "form-control form-control-lg", 'id': "yourPassword", "placeholder": "Password"}))

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     user = User.objects.get(Q(username=username) | Q(
    #         email=username))
    #     if user:
    #         if user.email_verified:
    #             return username
    #         else:
    #             raise forms.ValidationError(
    #                 "Please Verife Yor Email",
    #                 code='password_mismatch',
    #             )
    #     else:
    #         return username


class User_Create(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "yourPassword", 'placeholder': "Password"}))
    password2 = forms.CharField(label="Password Conform", widget=forms.PasswordInput(
        attrs={'class': "form-control", 'id': "yourPassword", 'placeholder': "Conform-Password"}))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            try:
                user = User.objects.filter(email=email)
            except Exception as msg:
                pass
            if user:
                raise forms.ValidationError(
                    "Email Alredy Exists!!",
                    code='password_mismatch',
                )
        return email

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",
                  "email", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(attrs={'class': "form-control", 'id': "yourName", 'placeholder': "First Name"}),
            "last_name": forms.TextInput(attrs={'class': "form-control", 'id': "yourName", 'placeholder': "Last Name"}),
            "email": forms.EmailInput(attrs={'class': "form-control", 'id': "yourEmail", 'placeholder': "Email"}),
            "username": forms.EmailInput(attrs={'class': "form-control", 'id': "yourName", 'placeholder': "User Name"})
        }


class profileform(forms.ModelForm):

    class Meta:
        model = student_detaiels
        fields = ('student_image', 'College_Name', 'Student_Usn',
                  'Department', 'Date_Of_Birth', 'Contact_Number')
        widgets = {
            "student_image": forms.FileInput(attrs={'class': "form-control", 'id': "student_image", 'style': "visibility: hidden;", "onchange": "load(event)"}),
            "College_Name": forms.Select(attrs={'class': "form-control" }),
            "Student_Usn": forms.TextInput(attrs={'class': "form-control", }),
            "Department": forms.TextInput(attrs={'class': "form-control", }),
            "Date_Of_Birth": forms.DateInput(attrs={'class': "form-control",'id':'datetimepicker1',}),
            "Contact_Number": forms.TextInput(attrs={'class': "form-control", })

        }


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class ChangeUserPassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id': "currentPassword",
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id': "newPassword"
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control", 'id': "renewPassword",
    }))

    class Meta:
        fields = ("old_password", "new_password1", "new_password2")
