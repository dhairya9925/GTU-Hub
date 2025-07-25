"""
URL configuration for gtu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('contact', views.contact, name="contact"),
    path('courses', views.courses, name="courses"),
    path('papers', views.questionPaper, name="question-paper"),
    path('circular', views.circular, name="circular"),
    path('result', views.result, name="result"),
    path('timetable', views.timetable, name="timetable"),
]
