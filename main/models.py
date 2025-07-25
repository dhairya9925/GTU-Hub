from django.db import models

# Create your models here.
# class Course(models.Model):
#     shortform = models.CharField(max_length=2, unique=True, null=False)
#     name = models.CharField(max_length=100, null=False)
    
#     def __str__(self):
#         return self.shortform
class Course(models.Model):
    shortform = models.CharField(max_length=2, unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    total_branches = models.IntegerField(default=0)
    total_subjects = models.IntegerField(default=0)
    total_institutes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.shortform


class Branches(models.Model):
    branchCode = models.CharField(max_length=4, null=False)
    name = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course ,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.branchCode


class Semester(models.Model):

    semester =models.IntegerField(null=False)
    course = models.ForeignKey(Course ,on_delete=models.CASCADE, null=False, default=None)

    class Meta:
        verbose_name = "Semester"
        verbose_name_plural = "Semesters"

    def __str__(self):
        return self.name


class Year(models.Model):

    year = models.CharField(max_length=7, null=False, default=None)
    course = models.ForeignKey(Course ,on_delete=models.CASCADE, null=False, default=None)

    class Meta:
        verbose_name = "Year"
        verbose_name_plural = "Years"

    def __str__(self):
        return self.name


class Subjects(models.Model):
    subjectCode = models.CharField(max_length=100, null=False)
    branch = models.ForeignKey(Branches, verbose_name="branch", on_delete=models.CASCADE, null=False, default=None)
    effectiveFrom = models.CharField(max_length=20, default=None)
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=150, null=False)
    sem = models.IntegerField(null=False)
    credit = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name} ({self.subjectCode})"

    class Meta:
        ordering = ['subjectCode']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Tables(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField(max_length=200)
    data = models.JSONField(default=list)
    def __str__(self):
        return self.name
# class Result(models.Model):
#     categories = [
#         ("remedial", "Remedial")
#         ("regular", "Regular")
#     ]
#     name = models.CharField(max_length=50)
#     date = models.DateField(auto_now=False, auto_now_add=False)
#     category = models.CharField(max_length=8, choices=categories, default=None)
#     link = models.CharField( max_length=50)
#     last_date = models.DateField(auto_now=False, auto_now_add=False)
