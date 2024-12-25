from django.shortcuts import render, HttpResponse

# Create your views here.
import requests as re

from .models import Book_Details, Category_Details, Binding_Details
from bs4 import BeautifulSoup


books = {}


def gett(request):
    p = 0
    r = re.get(
        f"https://www.googleapis.com/books/v1/volumes?q=Haking+intitle")
    data = r.json()
    for i in data.get("items", "no"):
        if i == "no":
            break
        try:
            book = {
                "title": i["volumeInfo"]["title"],
                "Sub-title": i["volumeInfo"].get("subtitle", "None"),
                "Pub-date": i["volumeInfo"]["publishedDate"],
                "Publisher": i["volumeInfo"].get("publisher", "indivisual"),
                "page-count": i["volumeInfo"].get("pageCount", 0),
                "ISBN": i["volumeInfo"]["industryIdentifiers"],
                "images": i["volumeInfo"]["imageLinks"],
                "version": i["volumeInfo"]["contentVersion"],
                "description": i["volumeInfo"].get("description", "no-description"),
                "category": i["volumeInfo"]["categories"],
                "authors": i["volumeInfo"]["authors"],
                "rating": i["volumeInfo"].get("averageRating", 0),
                "price": i["saleInfo"].get("retailPrice", dict()).get("amount", 0),
            }

            books[f"book{p}"] = book
            p += 1
        except Exception as msg:
            print(msg)
    return HttpResponse("ok")


def add(request):
    # print(books)

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
                No_Of_Copies_Current=100,
                price=i["price"],
                description=i["description"],
                no_pages=i["page-count"],
                version=i["version"],
                rating=i["rating"],
                # Category_Type=catogory[0],
                Binding_Id=binding[0]
            )
            book.save()
            book.Category_Type.set([catogory[0]])
        except Exception as msg:
            print(msg)
    return HttpResponse("ok")
