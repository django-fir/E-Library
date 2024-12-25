"""proto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,re_path
from app import views
from django.views.static import serve

from django.conf.urls import handler400,handler404,handler500

admin.site.site_header = "E - Lib Admin"
admin.site.site_title = "E - Lib Admins"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("search/", views.bookcards),
    path("books/", views.getbook, name="book"),
    path("", views.home, name='home'),
    path("contact/",views.contact,name="contact"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path('signup/', views.sign_user_up, name="signup"),
    path('verify/<slug:token>', views.verify),
    path('token/', views.token),
    path("profile/", views.profile, name="profile"),
    path('addbook/<title>', views.addbook),
    path("staffpr/<id>", views.staffpr),
    path("cart/", views.cart, name='cart'), 
    path("book/embend/<id>",views.embed,name="embed"), 
    re_path(r'static/media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

]

handler404 = 'app.views.handel404'
handler500 = 'app.views.handel500'

