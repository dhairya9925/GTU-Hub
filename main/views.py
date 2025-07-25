import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
from .models import Branches, Course, Subjects, Semester, Year
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db.models import Count, Min
from .custom_logic.affiliatedClg import get_colleges, download_affiliated_college_list
from .custom_logic import data_fetcher
import schedule

schedule.every().second

# Create your views here.
def main(request):
    
    # get_colleges()
    # timeZone()
    # process_college_pdf()
    # courses = Course.objects.all()
    # for course in courses:
    #     print(course.name)
    context = {
        "1": "",
    }
    return render(request, "index.html", context)


def contact(request):
    context = {
        "1": "",
    }
    return render(request, "contact.html", context)


def courses(request):
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
        # 'branches': branches,
        # 'semesters': semesters,
        # 'years': years,
        # 'subjects': subjects,
    }
    return render(request, "courses.html", context)


def questionPaper(request):
    context = {
        "1": "",
    }
    return render(request, "questionPapers.html", context)


def circular(request):
    context = {
        "1": "",
    }
    return render(request, "circular.html", context)


def result(request):
    context = {
        "1": "",
    }
    return render(request, "result.html", context)


def timetable(request):
    context = {
        "1": "",
    }
    return render(request, "timetable.html", context)


# _______________________________________________________________________________________________________________________________________________________________________________


# def timeZone():
#     tnow = datetime.now()
#     tz = datetime.timetz(datetime.)
#     print(f"Time Now: {tnow}")
#     print(f"Current TZ Time: {tz}")
#     # timer = datetime.now(tz=datetime.tzinfo)




