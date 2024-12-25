
from cgitb import handler
from email import message
from django import urls
from django.shortcuts import redirect, render, HttpResponseRedirect
from app.models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from app.forms import User_Login, User_Create, profileform, ChangeUserPassword
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import uuid
import requests as re


@login_required
def bookcards(request):
    uname = student_detaiels.objects.get(student=request.user)
    key1 = request.GET.get('address')
    key2 = request.GET.get('onlyisusingthw')
    key = None
    borrow = Borrower_Details.objects.get(
            student=uname)
    count = borrow.Book_ID.all().count
    if key1:
        key = key1
    if key2:
        key = key2
    books = []
    if key:
        book = Book_Details.objects.filter(
            Q(Book_Title__icontains=key) |
            Q(Category_Type__Category_Name__icontains=key) |
            Q(Binding_Id__Author__icontains=key) |
            Q(Isbn13__icontains=key) |
            Q(Isbn10__icontains=key))
        if key2:
            return render(request, "axios.html", {'books': book, 'user': uname,"boorw":borrow,"countb":count})
        for i in book:
            title = i.Book_Title + ", Author:  " + \
                i.Binding_Id.Author + "--"+str(i.id)
            books.append(title)
    return JsonResponse({'status': 200, 'books': books})


def getbook(request):
    if request.user.is_authenticated:
        uname = student_detaiels.objects.get(student=request.user)
        borrow = Borrower_Details.objects.get(
            student=uname)
        count = borrow.Book_ID.all().count
        key = request.GET.get("searchdbook")
        if key:
            book = Book_Details.objects.get(id=int(key))
            return render(request, "bookd.html", {'book': book, 'user': uname,"boorw":borrow,"countb":count})
        return render(request, "axios.html", {'books': Book_Details.objects.all(), 'user': uname,"boorw":borrow,"countb":count})
    else:
        return HttpResponseRedirect("/login")


def home(request):
    if request.user.is_authenticated:
        user = student_detaiels.objects.get(student=request.user)
        borrow = Borrower_Details.objects.get_or_create(
            student=user)
        count = borrow[0].Book_ID.all().count
        staff = student_detaiels.objects.filter(
            student__is_staff=True, student__is_superuser=False).order_by('-student__date_joined')
        testi = Testimonials.objects.all()
        return render(request, 'base.html', {"user": user, 'count': countall(), "staff": staff,"boorw":borrow[0],"countb":count,"testi":testi})
    else:
        return HttpResponseRedirect("/login")


def staffpr(request, id):
    user = student_detaiels.objects.get(id=int(id))
    return render(request, "profile.html", {'pr': True, 'usere': user, "formp": True, "user": student_detaiels.objects.get(student=request.user)})


def countall():
    books = Book_Details.objects.all().count
    students = student_detaiels.objects.all().count
    staf = student_detaiels.objects.filter(
        student__is_staff=True,
        student__is_superuser=False
    ).count
    lib = 10
    return {"books": books, "students": students, "staf": staf, "lib": lib}


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login")


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = User_Login(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            upass = form.cleaned_data.get('password')
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                
                messages.success(request, f"Welcome {user.username}",extra_tags="success")
                
                return HttpResponseRedirect("/")

    else:
        form = User_Login()
    return render(request, "login.html", {"fm": form})


def sign_user_up(request):
    if request.user.is_authenticated:
        return redirect(urls.reverse(home))
    if request.method == "POST":
        form = User_Create(request.POST)
        if form.is_valid():
            form.save()
            fname = form.cleaned_data.get("first_name")
            lname = form.cleaned_data.get("last_name")
            token = uuid.uuid4()
            email = form.cleaned_data.get("email")
            Authe.objects.create(
                user=User.objects.get(email=email), auth_token=token)
            user = Authe.objects.get(auth_token=token)
            user.user.email_verified = True
            user.user.save()
            student_detaiels.objects.get_or_create(student=user.user)
            url = request.get_host()
            status = sendmail(token, fname+lname, email,url)
            status = True
            if status:
                messages.success(
                    request, f"A Link Is Sent To Your Email Plesse Check Mail",extra_tags="success")
                return HttpResponseRedirect("/login")
            else:
                messages.success(request, "You Are Email Is Not Valid",extra_tags="danger")
                return HttpResponseRedirect("/signup")
            messages.success(request, "Your Account Created Please Login !",extra_tags="success")
            return HttpResponseRedirect("/login")
    else:
        form = User_Create()
    return render(request, "signup.html", {'form': form})


def sendmail(token, user, email,url):
    subj = f'Welocme To RanjithRakshith Libraryes {user}'
    msg = f'{url}/verify/{token}'
    text_content = 'This is an important message.'
    html_content = f'<h2>Welcome {user}</h2><br><p>Be A Part Of Our RR Lib (RanjithRakshit Librarres)</p><br><p>Click hear To Authenticate Your Email:</p><a href="{msg}"><button>Authenticate:button></a><h1>-------------OR---------------</h1><br><p>Past This Link In The Browser: </p><br><a>{msg}</a>'
    msg = EmailMultiAlternatives(
        subj, text_content, f"RR Lib <{settings.EMAIL_HOST_USER}>", [email])
    msg.attach_alternative(html_content, "text/html")
    sent = msg.send()
    return sent


def verify(request, token):
    user = Authe.objects.get(auth_token=token)
    if user:
        user.user.email_verified = True
        user.user.save()
        student_detaiels.objects.get_or_create(student=user.user)
        messages.success(
            request, f"Welcome {user.user} : You are Authenticated",extra_tags="primary")
        return render(request, 'verify.html', {'user': user})
    else:
        messages.success(request, "User Cant Authenticate",extra_tags="dark")
        return render(request, 'verify.html', {'user': None})


def token(request):
    return render(request, 'token.html')


def profile(request):
    if request.user.is_authenticated: 
        apples = True  
        forme = ChangeUserPassword(user=request.user)
        stu = student_detaiels.objects.get(student=request.user)
        borrow = Borrower_Details.objects.get(
            student=stu)
        count = borrow.Book_ID.all().count
        if "renewpasswordsubmit" in request.POST:
            forme = ChangeUserPassword(user=request.user, data=request.POST)
            if forme.is_valid():
                forme.save()
                messages.success(
                    request, "Your Password Changed Succesfully ! Plese Login",extra_tags="success")
                return redirect('home')
            else:
                messages.success(request, f"Check Your Password :  Not Changed !",extra_tags="secondary")
                apples = False
        form = profileform(instance=stu)
        if apples:                
            form = profileform(request.POST or None,
                        request.FILES or None, instance=stu)
            if form.is_valid():
                form.save()
                messages.warning(request, "Your Detailes Changed Succcesfully",extra_tags="primary")
        apples = True
        return render(request, "profile.html", {"user": stu, 'formp': form, 'formpp': forme, "pr": False,"boorw":borrow,"countb":count})
    else:
        return redirect('home')


def addbook(request, title):
    if request.user.is_staff:
        if gett(title):
            messages.success(request, f"{title} added succespully!",extra_tags="success")
            return redirect("book")
    messages.success(request, f"{title} not Found",extra_tags="danger")
    return redirect("book")

import random as rd
def gett(title):
    books = {}
    p = 0
    r = re.get(
        f"https://www.googleapis.com/books/v1/volumes?q={title}+intitle")
    data = r.json()
    for i in data.get("items", "no"):
        if i == "no":
            break
        try:
            book = {
                "title": i["volumeInfo"]["title"],
                "Sub-title": i["volumeInfo"].get("subtitle", "None") or "None",
                "Pub-date": i["volumeInfo"]["publishedDate"],
                "Publisher": i["volumeInfo"].get("publisher", "indivisual") or "None",
                "page-count": i["volumeInfo"].get("pageCount", 0) or 0,
                "ISBN": i["volumeInfo"]["industryIdentifiers"],
                "images": i["volumeInfo"]["imageLinks"],
                "version": i["volumeInfo"]["contentVersion"] or "None",
                "description": i["volumeInfo"].get("description", "no-description"),
                "category": i["volumeInfo"]["categories"] or "None",
                "authors": i["volumeInfo"]["authors"],
                "rating": i["volumeInfo"].get("averageRating", 0) or 0,
                "price": i["saleInfo"].get("retailPrice", dict()).get("amount", 0) or 0,
                "read":i['volumeInfo'].get('previewLink') or "None",
            }
            books[f"book{p}"] = book
            print(book["title"],book["read"])
            p += 1
        except Exception as msg:
            print(msg)
    
    for i in books.values():
        try:
            date = i["Pub-date"]
            if len(date) < 10:
                date = "2020-12-12"
            catogory = Category_Details.objects.get_or_create(
                Category_Name=i["category"][0])
            binding = Binding_Details.objects.get_or_create(
                Binding_Name=i['Publisher'], Author=i["authors"][0])
            # print(catogory)
            book = Book_Details(
                book_image=i['images']['smallThumbnail'],
                Isbn10=i["ISBN"][1]['identifier'],
                Isbn13=i["ISBN"][0]['identifier'],
                Book_Title=i["title"],
                Book_subtitle=i["Sub-title"],
                Publication_year=date,
                Language='english',
                No_Of_Copies_Actual=100,
                No_Of_Copies_Current=90,
                price=i["price"],
                description=i["description"],
                no_pages=i["page-count"],
                version=i["version"],
                rating=i["rating"],
                # Category_Type=catogory[0],
                Binding_Id=binding[0],
                read_url = i["read"]
            )
            book.save()
            book.Category_Type.set([catogory[0]])
        except Exception as msg:
            print(msg)
    return len(books)

from django.db.models import Sum
def cart(request):
    if request.user.is_authenticated:
        ip = request.META.get("HTTP_REFERER")
        print(ip,end='\n\n\n\n\n\n')
        stu = student_detaiels.objects.get(student=request.user)
        borrow = Borrower_Details.objects.get_or_create(
            student=stu)
        key = request.GET.get("addtocart")
        key1 = request.GET.get("deletecart")
        if key:
            book = Book_Details.objects.get(
                id=int(key), No_Of_Copies_Current__gt=0)
            if not book:
                messages.warning(request, f"Not Possible to add To cart!",extra_tags="danger")
            else:
                borrow[0].Book_ID.add(book)                
                borrow[0].save()
                book.No_Of_Copies_Current -= 1
                book.save()
                messages.success(
                    request, f"{book.Book_Title} added succesfully !",extra_tags="success")
                return HttpResponseRedirect(ip)
        if key1:
            book = Book_Details.objects.get(
                id=int(key1), No_Of_Copies_Current__gt=0)
            borrow[0].Book_ID.remove(book)
            borrow[0].save()
            book.No_Of_Copies_Current += 1
            book.save()
            messages.warning(
                request, f"{book.Book_Title} removed succesfully !",extra_tags="warning")
            return HttpResponseRedirect(ip)
        count = borrow[0].Book_ID.all().count
        totals = borrow[0].Book_ID.all().aggregate(Sum('price'))["price__sum"]
        total = totals + 20
        
        

        return render(request, "cart.html", {'boorw': borrow[0], "countb": count,"total":total ,"totals":totals ,"user": stu,"cart":True})

def embed(request,id):
    if request.user.is_authenticated:
        user = student_detaiels.objects.get(student=request.user)
        borrow = Borrower_Details.objects.get_or_create(
            student=user)
        count = borrow[0].Book_ID.all().count  
        book = Book_Details.objects.get(id=id).Isbn10      
        return render(request, 'embend.html', {"user": user, 'count': countall(),"boorw":borrow[0],"countb":count,"emb":book})
    else:
        return HttpResponseRedirect("/login")



def contact(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            messages.warning(
                request, f"Thank You For Sending Email We Will Check For You !",extra_tags="success")            
            return HttpResponseRedirect("/")
        user = student_detaiels.objects.get(student=request.user)
        borrow = Borrower_Details.objects.get_or_create(
            student=user)
        count = borrow[0].Book_ID.all().count        
        return render(request, 'contact.html', {"user": user, 'count': countall(), "boorw":borrow[0],"countb":count,"contact":True,})

    else:
        return HttpResponseRedirect("/login")










# Handeling Errors
def handel404(request,exception):
    return render(request,'pages-error-404.html',{"exc":exception,'error':404})
def handel500(request):
    return render(request,'pages-error-404.html',{"error":500})
