"""Video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from Video import settings
from mySite import views
from mySite.views import loginPage, registerPage, userGetInf, doLogout, get_video_rating, ourinfo

urlpatterns = (
    path('admin/', admin.site.urls),
    path('catalog', views.index2, name="Каталог"),
    path('video', views.index3, name="Поиск по актерам"),
    path('', views.dopoln, name="Главная страница"),
    re_path(r'^videos/(?P<video_id>[0-9])+/$', views.show_video, name='videos'),
    path('login', loginPage, name='login'),
    path('register', registerPage, name='register'),
    path('userInfo', userGetInf, name='userinfo'),
    path('logout', doLogout, name='logout'),
    path('addrating',get_video_rating, name="add_rating"),
    path('ourinfo', ourinfo, name='Информация о нас'),
    path('search', views.search, name='search')
)

