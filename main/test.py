from django.shortcuts import render
from django.http import HttpResponseRedirect
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
from .models import Branches, Course, Subjects, Semester, Year
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# from django.http 

def get_remaining_course():
    all_courses = Course.objects.values_list("id")
    print(len(all_courses))
    courses_in_sem = set(list(Semester.objects.values_list("course")))
    print(courses_in_sem)
    # all_courses = []
    # courses_in_sem = []
    remaining = set()
    for course in all_courses:
        if course in courses_in_sem:
            pass
        else:
            remaining.add(course)
    # print(remaining)
    return remaining
    # for course in courses:
    #     all_courses.append(course.id)
    # for sem in sems:
    #     courses_in_sem.append(sem.course)
    

def get_courses():
    driver = webdriver.Chrome()
    driver.get("https://gtu.ac.in/Syllabus/Syllabus.aspx")


    time.sleep(2)

    courseSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddcourse")
    coursesAll = courseSelectElement.find_elements(By.TAG_NAME, "option")
    shortform_lst = []
    # dbCourse = Course.objects.all()
    # dbCourse.delete()
    # for course in coursesAll:
    #     shortform = course.get_attribute("value")        
    #     if shortform in shortform_lst:
    #         continue
    #     shortform_lst.append(shortform)
            
    #     dbCourse = Course( name =course.text, shortform= shortform)
    #     dbCourse.save()

    error_branch_list = set()
    courses = Course.objects.all()
    # sem = Semester.objects.all()
    # sem.delete()
    # year = Year.objects.all()
    # year.delete()
    remaining = get_remaining_course()
    print(f"Remaining Courses: {remaining}")
    for course in courses:
        print(f"Coruse = {course.name}")
        if len(course.shortform)>3:
            continue
        courseSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddcourse")
        courseSelect = Select(courseSelectElement)
        courseSelect.select_by_value(course.shortform)
        time.sleep(3)

        # dbBranch = Branches()
        try:
            print("Sem")
# ______________________________________________________________________________________________________________________________________________        
            semSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddsem")
            semestersAll = semSelectElement.find_elements(By.TAG_NAME, "option")
            for sem in semestersAll:
                
                value = sem.get_attribute("value")
                if value == "Sem":
                    continue
                print(f" {int(value)}", end=" ")
                dbSemester = Semester(semester = int(value), course = course)
                dbSemester.save()

            print("\nYear")
# ______________________________________________________________________________________________________________________________________________        
            yearSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddl_effFrom")
            yearsAll = yearSelectElement.find_elements(By.TAG_NAME, "option")
            for year in yearsAll:
                # print(f"-- Year : {year}")
                if year.text == "Academic Year":
                    continue
                print(f" {year.text}", end=" ")
                dbYear = Year(year = year.text, course = course)
                dbYear.save()

            print("\nBranch")
# ______________________________________________________________________________________________________________________________________________        
        # branchSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddlbrcode")
        # branchesAll = branchSelectElement.find_elements(By.TAG_NAME, "option")
        # for branch in branchesAll:
        #     if branch.text == "Select Branch":
        #         continue

        #     dbBranch = Branches(
        #         branchCode = branch.get_attribute("value"),
        #         name = " ".join(branch.text.split(" - ")[1:]),
        #         course = course,
        #     )
        #     dbBranch.save()
        #     branchSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddlbrcode")
        #     branchSelect = Select(branchSelectElement)
        #     branchSelect.select_by_value(branch.get_attribute("value"))
        #     time.sleep(.5)
        #     print(f"Current Branch = {branch.text}")
            
        #     branches = Branches.objects.filter(course = course)
        #     print(f"Course = {course.name}")
        #     for b in branches:
        #         print(f"Branches : {b.name}")
        except Exception as e:
            print(f"You Have Gotten the following error!!!\n\n {e}")
            
    #     for branch in branches:
    #         print(f"Current Branch = {branch.name}")
                

    #         if branch.branchCode == "Select Branch":
    #             continue
    #         # dbBranch = Branches(
    #         #     branchCode = branch.get_attribute("value"),
    #         #     name = " ".join(branch.text.split(" - ")[1:]),
    #         #     course = course,
    #         # )
    #         # dbBranch.save()

    #         print("Selecting Branch")
    #         branchSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddlbrcode")
    #         branchSelect = Select(branchSelectElement)
    #         branchSelect.select_by_value(branch.branchCode)
    #         time.sleep(.5)
    # # ______________________________________________________________________________________________________________________________________________        
    #         print("Search")
    #         serchButton = driver.find_element(By.ID, "ContentPlaceHolder1_btn_search")
    #         serchButton.click()

    #         subject_table = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='myGrid']")))
    #         time.sleep(2)
    #         # table = subjects.find_element(By.ID, "ContentPlaceHolder1_GridViewToCategory")
    #         # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "tr")))
    #         try:
                    
    #             rows = subject_table.find_elements(By.TAG_NAME, "tr")
    #             for row in rows:
    #                 try:
    #                     if not row.text:
    #                         continue
                        
    #                     print(f"\nrows = {row.text}")
    #                     cols = row.find_elements(By.TAG_NAME, "td")
    #                     fields = [
    #                         "subjectCode",
    #                         "effectiveFrom",
    #                         "name",
    #                         "category",
    #                         "sem",
    #                         "credit",
    #                     ]
    #                     inc_lst = [1,3,4,5,6,11]
    #                     data_dict = {}
    #                     count = 1
    #                     for col, field in zip(cols,fields):
    #                         if not col.text:
    #                             continue
    #                         if count in inc_lst:
    #                             data_dict.update({field: col})
    #                             count += 1
    #                         else:
    #                             count += 1
                        

    #                     subject = Subjects(**data_dict)
    #                     subject.branch = dbBranch
    #                     # print(f"--- Sub => {data_dict["name"]}")
    #                     # subject.save()
    #                 except Exception as e:
    #                     print(f"Some Error Occured!!!!!!\nCourse: {course}, Branch: {branch.name} \n\nError: {e}")
    #                     time.sleep(5)
    #         except Exception as e:
    #             print(f"Error in Rows !!!!!!\nCourse: {course}, Branch: {branch.name} \n\nError: {e}")
    #             error_branch_list.add(branch)
    #             time.sleep(5)

    #     print("List Of Branches with error")    
    #     for branch in error_branch_list:
    #         print(f"\t{branch}")

    
        print("\n\n\n---- Over One ----")
        continue
            # subject.objects.all()
            # subject.delete()


    driver.close()
    return 1


# Create your views here.
def main(request):
    get_courses()
    context = {
        "1": "",
    }
    return render(request, "index.html", context)


def courses(request):
    context = {
        "1": "",
    }
    return render(request, "courses.html", context)


def questionPaper(request):
    context = {
        "1": "",
    }
    return render(request, "questionPapers.html", context)




# # ______________________________________________________________________________________________________________________________________________        
# # ______________________________________________________________________________________________________________________________________________        
# # ______________________________________________________________________________________________________________________________________________        
def get_courses():
    driver = webdriver.Chrome()
    driver.get("https://gtu.ac.in/Syllabus/Syllabus.aspx")

    time.sleep(2)

    # sub = Subjects.objects.all()
    # sub.delete()

    error_list = {}

    remaining = get_remaining_course()
    print(f"Error List: {error_list}")
    for course in courses:
        print(f"\n\nCourse: {course}")
        if len(course.shortform)>3:
            continue
        courseSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddcourse")
        courseSelect = Select(courseSelectElement)
        courseSelect.select_by_value(course.shortform)

        time.sleep(3)

# ______________________________________________________________________________________________________________________________________________        
        print("Sem")
        # save_sem(course, driver)

# ______________________________________________________________________________________________________________________________________________        
        print("\nYear")
        # save_year(course, driver)
# ______________________________________________________________________________________________________________________________________________        
        print("\nBranches")
        # save_branch(course, driver)
# ______________________________________________________________________________________________________________________________________________        

        remaining_subjects = remaining_subs()
        print(remaining_subjects)
        save_subjects(driver, remaining_subjects)
        break
        # branches = Branches.objects.filter(course = course)
        for branch in branches:
            try:
                print(f"Branch Code: {branch.branchCode}")
                branchSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddlbrcode")
                branchSelect = Select(branchSelectElement)
                branchSelect.select_by_value(branch.branchCode)
                # print(f"Current Branch = {branch.name}")
                
                serchButton = driver.find_element(By.ID, "ContentPlaceHolder1_btn_search")
                serchButton.click()

                subject_table = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='myGrid']")))
                time.sleep(2)
                rows = subject_table.find_elements(By.TAG_NAME, "tr")
                data_dict = {}
                for index, row in enumerate(rows):

                    if not row.text:
                        continue

                    #                         1                  3           4          5        6                      11   
                    # if row.text == "Exp. Subcode Branch code Eff_from SubjectName Category Sem /Year L. T. P. TW/SL Total E M I V Total":
                    #     continue
                    cols = row.find_elements(By.XPATH, "./td") # selects td elements with align attribute
                    headings = row.find_elements(By.TAG_NAME, "th")

                    if index == 0:
                        for heading in headings:
                            if heading.text:
                                if heading.text in data_dict.keys():
                                    data_dict.update({heading.text.lower(): ""})
                                data_dict.update({heading.text: ""})
                        continue
                    # print(f"cols:{len(cols)}\nDict:{len(data_dict)}")
                    for field, col in zip(data_dict,cols):
                        # print(f"{field} -> {col.text}")
                        data_dict.update({field: col.text})

                    print(f"Data dict -> {data_dict}")
                    required_fields = {
                        "Subcode": "subjectCode",
                        "Eff_from": "effectiveFrom",
                        "SubjectName": "name",
                        "Category": "category",
                        "Sem /Year": "sem",
                        "Total": "credit"
                    }
                    subject = Subjects()

                    for field_from_table, model_field in required_fields.items():
                        setattr(subject, model_field, data_dict[field_from_table])

                    subject.branch = branch
                    # print(f"subjectCode: {subject.subjectCode}")
                    # print(f"branch: {subject.branch}")
                    # print(f"effectiveFrom: {subject.effectiveFrom}")
                    # print(f"name: {subject.name}")
                    # print(f"category: {subject.category}")
                    # print(f"sem: {subject.sem}")
                    # print(f"credit: {subject.credit}\n\n")
                    subject.save()

            except Exception as e:
                if course in error_list.keys():
                    error_list[course].append(branch)
                else:
                    error_list.update({course: [branch]})
                print(f"Error While Fetching rows, in Branch: {branch.name}!!!\n\n{e}")

        print("\n\n\n---- Over One ----")
            # subject.objects.all()
            # subject.delete()
    
    
    # print(f"Errors in -> {error_list}")
    # count = 0
    # while error_list or count == 3:
    #     error_list = save_subjects(driver, error_list.keys(), branches_lst = error_list.values())
    #     count += 1
    driver.close()
    return 1



B.Arch Intake 2024-25_418010
B.Design Intake 2024-25_106386
B.E. Intake 2024-25_879761
B.Pharm Intake 2024-25_958340
B.Voc Intake 2024-25_129040
BBA Intitutes Intake 2024-25_660959
BCA Institutes Intake 2024-25_319218
BID Intake 2024-25_509063
D.Pharm Intake 2024-25.1_661352
D.Voc Intake 2024-25_918653
Diploma Architecture Intake 2024-25_378221
Diploma Intake 2024-25_507005
HMCT Intake 2024-25_211297
Integrated M.Sc IT Intake 2024-25_942303
M.Arch Intake 2024-25_883953
M.E._226751
M.Pharm Intake 2024-25_833266
MBA Intake 2024-25_900043
MBA Integrated Intake 2024-25_847919
MCA Intake 2024-25_954724 (1)_586941
MCA Integrated Intake 2024-25_839700
Pharm.D Intake 2024-25_426229