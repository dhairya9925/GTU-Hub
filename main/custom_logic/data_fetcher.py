import requests
from bs4 import BeautifulSoup
from schemas import Result
from datetime import datetime
from typing import List



results: List[Result] = []

def get_results():
    url = "https://gtu.ac.in/result.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    }
    page = requests.get(url, headers=headers)


    
    soup = BeautifulSoup(page.content, "html.parser")
    all_results = soup.find(id="result1").find_all("li") + soup.find(id="result2").find_all("li") 

    for index, tag in enumerate(all_results):
        try:
            print(f"\t\t---{index}---") 
            id = index + 1
            name = tag.a.get_text()
            date = tag.find("div", {"class": "date-in"}).get_text()
            category = name.split(" - ")[-1].split()[0]
            link = tag.a["href"]
            recheck_deadline = tag.h3.span.get_text()
            if recheck_deadline.strip() == "":
                raise ValueError("Value Not Found")
        except Exception as e:
            recheck_deadline = None
            print(f"\nError {e}: \n")    
        finally:
            print(f"ID: {id}\nName: {name}\nDate: {date}\nCategory: {category}\nLink: {link}\nLast Date: {recheck_deadline}\n")
            result = Result(
                id = id,
                name = name,
                date = datetime.strptime(date, "%d %b %Y"),
                category = category.lower(),
                link = link,
                recheck_deadline = recheck_deadline
            )
            results.append(result)
    return results


def get_circular():
    pass


# GET REMAINING COURSES
def get_remaining_course():
    all_courses = Course.objects.values_list("id")
    # print(len(all_courses))
    courses_in_sem = set(list(Branches.objects.values_list("course")))
    print(courses_in_sem)
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


# REMOVE ALL DATA FROM DB
def remove_data(exclude: list):
    
    fields = {
        "courses": Course.objects.all(),
        "branches": Branches.objects.all(),
        "sems": Semester.objects.all(),
        "year": Year.objects.all(),
        "subjects": Subjects.objects.all(),
    }

    for key, obj in fields.items():
        if key not in exclude:
            obj.delete()


# GET ALL SUBJECTS AND SAVE 'EM
def save_subjects(driver, branches, count = 0):
    
    rem_branch_list = []
    courses = Course.objects.all()
    print(f"\n\nCount: {count}")
    for course in courses:
        print(f"\n\nCourse: {course}")
        if len(course.shortform)>3:
            continue
        courseSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddcourse")
        courseSelect = Select(courseSelectElement)
        courseSelect.select_by_value(course.shortform)
        
        curr_course_branches = list(Branches.objects.filter(course=course).values_list("id"))
        filtered_branches = []
        for id in branches:
            if id in curr_course_branches:
                filtered_branches.append(id)
        for id in filtered_branches:
            branch = Branches.objects.get(id = id[0])
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
                rem_branch_list.append(branch.id)
                print(f"Error While Fetching rows, in Branch: {branch.name}!!!\n\n{e}")
        
    while rem_branch_list:
        if count >= 3:
            break
        count += 1
        save_subjects(driver, rem_branch_list, count)

    # error_list = {}
    # for course in courses:
    #     print(f"\n\nCourse: {course}")
    #     if len(course.shortform)>3:
    #         continue
    #     courseSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddcourse")
    #     courseSelect = Select(courseSelectElement)
    #     courseSelect.select_by_value(course.shortform)

    #     time.sleep(3)

    #     branches = Branches.objects.filter(course = course)
    #     for branch in branches:
    #         if branch not in branches_lst:
    #             continue
    #         try:
    #             print(f"Branch Code: {branch.branchCode}")
    #             branchSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddlbrcode")
    #             branchSelect = Select(branchSelectElement)
    #             branchSelect.select_by_value(branch.branchCode)
    #             # print(f"Current Branch = {branch.name}")
                
    #             serchButton = driver.find_element(By.ID, "ContentPlaceHolder1_btn_search")
    #             serchButton.click()

    #             subject_table = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, "//table[@class='myGrid']")))
    #             time.sleep(2)
    #             rows = subject_table.find_elements(By.TAG_NAME, "tr")
    #             data_dict = {}
    #             for index, row in enumerate(rows):

    #                 if not row.text:
    #                     continue

    #                 #                         1                  3           4          5        6                      11   
    #                 # if row.text == "Exp. Subcode Branch code Eff_from SubjectName Category Sem /Year L. T. P. TW/SL Total E M I V Total":
    #                 #     continue
    #                 cols = row.find_elements(By.XPATH, "./td") # selects td elements with align attribute
    #                 headings = row.find_elements(By.TAG_NAME, "th")

    #                 if index == 0:
    #                     for heading in headings:
    #                         if heading.text:
    #                             if heading.text in data_dict.keys():
    #                                 data_dict.update({heading.text.lower(): ""})
    #                             data_dict.update({heading.text: ""})
    #                     continue
    #                 # print(f"cols:{len(cols)}\nDict:{len(data_dict)}")
    #                 for field, col in zip(data_dict,cols):
    #                     # print(f"{field} -> {col.text}")
    #                     data_dict.update({field: col.text})

    #                 print(f"Data dict -> {data_dict}")
    #                 required_fields = {
    #                     "Subcode": "subjectCode",
    #                     "Eff_from": "effectiveFrom",
    #                     "SubjectName": "name",
    #                     "Category": "category",
    #                     "Sem /Year": "sem",
    #                     "Total": "credit"
    #                 }
    #                 subject = Subjects()

    #                 for field_from_table, model_field in required_fields.items():
    #                     setattr(subject, model_field, data_dict[field_from_table])

    #                 subject.branch = branch
    #                 # print(f"subjectCode: {subject.subjectCode}")
    #                 # print(f"branch: {subject.branch}")
    #                 # print(f"effectiveFrom: {subject.effectiveFrom}")
    #                 # print(f"name: {subject.name}")
    #                 # print(f"category: {subject.category}")
    #                 # print(f"sem: {subject.sem}")
    #                 # print(f"credit: {subject.credit}\n\n")
    #                 subject.save()

    #         except Exception as e:
    #             if course in error_list.keys():
    #                 error_list[course].append(branch)
    #             else:
    #                 error_list.update({course: [branch]})
    #             print(f"Error While Fetching rows, in Branch: {branch.name}!!!\n\n{e}")

    return rem_branch_list


# GET BRANCHES WITH WHERE THERE IS STILL DATA TO COLLECT
def remaining_branches():
    branch_ids = list(Branches.objects.values_list("id"))
    branch_in_subjects = set(list(Subjects.objects.values_list("branch")))
    remaining_branches = []
    # print(f"All Branches: {branch_ids}")
    # print(f"Length: {len(branch_ids)}")
    # print(f"\n\nSubject Branches: {branch_in_subjects}")
    # print(f"\nLength: {len(branch_in_subjects)}")
    
    for id in branch_ids:
        if id not in branch_in_subjects:
            remaining_branches.append(id)

    print(f"\nRem: {remaining_branches}")
    print(f"\nRem: {len(remaining_branches)}")
    return remaining_branches
        # for subject in subjects:
        #     if 
    
    pass


# FIND DUPLICATE SUBJECTS IN DATABASE
def find_duplicate_subjects():
    duplicates = (
        Subjects.objects
        .values(
            'subjectCode',
            'branch',
            'effectiveFrom',
            'name',
            'category',
            'sem',
            'credit'
        )
        .annotate(dup_count=Count('id'))
        .filter(dup_count__gt=1)
    )

    if not duplicates:
        print("✅ No duplicate subjects found.")
        return False

    print("🚫 Duplicate subjects found:\n")

    for entry in duplicates:
        matches = Subjects.objects.filter(
            subjectCode=entry['subjectCode'],
            branch=entry['branch'],
            effectiveFrom=entry['effectiveFrom'],
            name=entry['name'],
            category=entry['category'],
            sem=entry['sem'],
            credit=entry['credit'],
        ).select_related('branch__course')  # To include related Course efficiently

        for subject in matches:
            print("----")
            print(f"ID: {subject.id}", end=" || ")
            print(f"Subject Code: {subject.subjectCode}", end=" || ")
            print(f"Name: {subject.name}", end=" || ")
            print(f"Branch: {subject.branch.name} ({subject.branch.branchCode})", end=" || ")
            print(f"Course: {subject.branch.course.name} ({subject.branch.course.shortform})", end=" || ")
            print(f"Effective From: {subject.effectiveFrom}", end=" || ")
            print(f"Category: {subject.category}", end=" || ")
            print(f"Semester: {subject.sem}", end=" || ")
            print(f"Credit: {subject.credit}", end=" || ")
        print("\n------\n")
    return True


# REMOVE DUPLICATE SUBJECTS IN DATABASE
def remove_duplicate_subjects():
    duplicates = (
        Subjects.objects
        .values(
            'subjectCode',
            'branch',
            'effectiveFrom',
            'name',
            'category',
            'sem',
            'credit'
        )
        .annotate(dup_count=Count('id'))
        .filter(dup_count__gt=1)
    )

    total_deleted = 0

    for entry in duplicates:
        matches = list(Subjects.objects.filter(
            subjectCode=entry['subjectCode'],
            branch=entry['branch'],
            effectiveFrom=entry['effectiveFrom'],
            name=entry['name'],
            category=entry['category'],
            sem=entry['sem'],
            credit=entry['credit'],
        ).order_by('id'))  # ensure consistent order

        # Keep the first and delete the rest
        to_delete = matches[1:]
        deleted_count, _ = Subjects.objects.filter(id__in=[s.id for s in to_delete]).delete()
        total_deleted += deleted_count

    print(f"✅ Removed {total_deleted} duplicate subject(s).")


# GET ALL DATA FROM WEBSITE AND SAVE EXCEPT SUBJETCS
def save_data():
    driver = webdriver.Chrome()
    driver.get("https://gtu.ac.in/Syllabus/Syllabus.aspx")

    time.sleep(2)

    # SAVE COURSE
    courseSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddcourse")
    coursesAll = courseSelectElement.find_element(By.TAG_NAME, "option")
    shortform_lst = []

    # TO DELETE PREVIOUSLY RECORDED Data UNCOMMENT THE BELOW LINES
    # remove_data()
    
    for course in coursesAll:
        shortform = course.get_attribute("value")        
        # TO PREVENT AMBIGUITY
        if shortform in shortform_lst:
            continue
        shortform_lst.append(shortform)
            
        dbCourse = Course( name =course.text, shortform= shortform)
        dbCourse.save()


    courses = Course.objects.all()
    for course in courses:
        # SAVE SEMESTER
        semSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddsem")
        semestersAll = semSelectElement.find_elements(By.TAG_NAME, "option")
        for sem in semestersAll:
            
            value = sem.get_attribute("value")
            if value == "Sem":
                continue
            print(f" |{int(value)}|", end=" ")
            dbSemester = Semester(semester = int(value), course = course)
            dbSemester.save()

        # SAVE YEAR
        yearSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddl_effFrom")
        yearsAll = yearSelectElement.find_elements(By.TAG_NAME, "option")
        for year in yearsAll:
            # print(f"-- Year : {year}")
            if year.text == "Academic Year":
                continue
            print(f" {year.text}", end=" ")
            dbYear = Year(year = year.text, course = course)
            dbYear.save()

        # SAVE BRANCH
        branchSelectElement = driver.find_element(By.ID, "ContentPlaceHolder1_ddlbrcode")
        branchesAll = branchSelectElement.find_elements(By.TAG_NAME, "option")
        for branch in branchesAll:
            if branch.text == "Select Branch":
                continue

            dbBranch = Branches(
                branchCode = branch.get_attribute("value"),
                name = " ".join(branch.text.split(" - ")[1:]),
                course = course,
            )
            dbBranch.save()
        
        # SAVE SUBJECTS
        branches = remaining_branches()
        save_subjects(driver, branches)
        if find_duplicate_subjects():
            remove_duplicate_subjects()
        

    driver.close()
    return True


def get_full_courses():
    url = "https://gtu.ac.in/Syllabus/Default.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
    }
    page = requests.get(url, headers=headers)
    links = {}
    
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table")
    # print(table)
    for index, tag in enumerate(table):
        if isinstance(tag, str):
            continue
        print(f"N-{type(tag)}")
        print("________________________________--")

        if index >= 2:
            break
        

if __name__ == "__main__":
    get_full_courses()
