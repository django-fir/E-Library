from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
from wsgiref.util import request_uri
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.


class Binding_Details(models.Model):
    Binding_Name = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Author


class Category_Details(models.Model):
    Category_Name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Category_Name


class Book_Details(models.Model):
    book_image = models.URLField(blank=True,null=True,help_text="add image url or leve blank")
    book_image_org = models.ImageField(upload_to="student/books/",blank=True,null=True,default="\student\default\profile.png",help_text="Choos Image")
    Isbn10 = models.CharField(max_length=15)
    Isbn13 = models.CharField(max_length=15)
    Book_Title = models.CharField(max_length=100, unique=True)
    Book_subtitle = models.CharField(max_length=30, blank=True, null=True)
    Publication_year = models.DateField()
    Language = models.CharField(max_length=100)
    Category_Type = models.ManyToManyField(
        Category_Details)  # Forign
    Binding_Id = models.ForeignKey(
        Binding_Details, on_delete=models.CASCADE)  # Forign
    No_Of_Copies_Actual = models.IntegerField(default=0)
    No_Of_Copies_Current = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    description = models.TextField(default=None)
    no_pages = models.IntegerField(blank=True, null=True)
    version = models.CharField(max_length=20)
    rating = models.IntegerField()
   

    def __str__(self) -> str:
        return self.Book_Title
    
    
    def save(self):
        if not self.book_image:
            self.book_image = self.book_image_org.url
        super(Book_Details, self).save()

        

    
    
    


class Shelf_Details(models.Model):
    Shelf_Id = models.CharField(max_length=100)
    Floor = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.Shelf_Id


class User(AbstractUser):
    email_verified = models.BooleanField(default=False)


class College(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Authe(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username


class student_detaiels(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    student_image = models.ImageField(
        upload_to='student/', default='\student\default\profile.png')
    choices = (("M", "Male"), ("F", "Female"), ("O", "Others"))
    Student_Usn = models.CharField(max_length=100, blank=True, null=True)
    Sex = models.CharField(max_length=2, choices=choices, default="M")
    Date_Of_Birth = models.DateField(blank=True, null=True)
    Department = models.CharField(
        max_length=100, blank=True, null=True)
    Contact_Number = models.CharField(
        max_length=100,  blank=True, null=True)
    College_Name = models.ForeignKey(
        College, on_delete=models.CASCADE, blank=True, null=True)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return self.student.username


class Borrower_Details(models.Model):
    student = models.ForeignKey(student_detaiels, on_delete=models.CASCADE)
    Book_ID = models.ManyToManyField(Book_Details, null=True, blank=True)
    Borrowed_From_Date = models.DateTimeField(null=True, blank=True)
    Borrowed_To_Date = models.DateTimeField(null=True, blank=True)
    Actual_Return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.student.student.username

class Testimonials(models.Model):
    student = models.ForeignKey(student_detaiels,on_delete=models.CASCADE)
    passion = models.CharField(max_length=100)
    review = models.TextField(max_length=600)

    def __str__(self):
        return self.student.student.get_full_name()
