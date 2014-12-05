from django.db import models

class GenEd(models.Model):
    code = models.CharField(max_length=5)
    desc = models.TextField()


class Instructor(models.Model):
    first_name = models.CharField(max_length=256)
    middle = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(null=True)


class Location(models.Model):
    building = models.CharField(max_length=256)
    room = models.CharField(max_length=150, null=True)


class Notes(models.Model):
    pass


class Subject(models.Model):
    code = models.CharField(max_length=8, unique=True, primary_key=True)
    subject = models.CharField(max_length=256)


class Course(models.Model):
    title = models.TextField()
    number = models.IntegerField()
    subject = models.ForeignKey(Subject)


class Date(models.Model):
    day = models.CharField(max_length=1)
    start = models.IntegerField()
    end = models.IntegerField()

class Meeting(models):
    date = models.ForeignKey(Date)
    location = models.ForeignKey(Location)


class BaseOfferingInfo(models.Model):
    instructors = models.ManyToManyField(Instructor)
    meetings = models.ManyToManyField(Date)
    crn = models.IntegerField(unique=True, null=True)


    class Meta:
        abstract = True




class Offering(BaseOfferingInfo):
    course = models.ForeignKey(Course)
    credits = models.IntegerField(null=True)


class AssociatedSection(BaseOfferingInfo):
    offering = models.ForeignKey(Offering)


class Eval(models.Model):
    instructor = models.ForeignKey(Instructor)
    course = models.ForeignKey(Course)

