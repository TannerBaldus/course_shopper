__author__ = 'tanner'
from models import Subject
from models import Course
from models import Instructor
from models import Location
from models import Offering
from models import AssociatedSection
from models import Evaluation
from random import  randint



def create_course(subject_code, num, title):
    subject = Subject.objects.get(code=subject_code)
    Course.objects.create(number=num, title=title, subject=subject)

def get_instructor(name):
    fname, middle, lname = name.split(' ')
    return Instructor.objects.get(fname=fname, lname=lname)

def create_instructor(name):
    fname, lname = name.split(' ')
    return Instructor.objects.create(fname=fname, lname=lname)

def get_course(code, number):
    subject = Subject.objects.get(code=code)
    return Course.objects.get(subject=subject, number=number)


def create_offering(subject_code, number, credits, room, bldg,  days, instructor_name):
    in_crn = randint(1000, 9999)
    instructor = get_instructor(instructor_name)
    course = get_course(subject_code, number)
    location = Location.objects.get(building=bldg, room=room)
    Offering.objects.create(instructor=instructor, course=course, crn=in_crn, days=days, credits=credits,
                            location=location)

def create_associated_section(room, bldg, in_crn, days, instructor_name):
    instructor = get_instructor(instructor_name)
    offering = Offering.objects.get(crn=in_crn)
    location = Location.objects.get(building=bldg, room=room)
    AssociatedSection.objects.create(offering=offering, instructor=instructor, crn=in_crn, days=days, location=location)


def create_eval(instructor_name, subject_code, number, min_rating=''):
    min_rating = min_rating or 1
    instructor = get_instructor(instructor_name)
    print subject_code, number
    course = get_course(subject_code, number)

    for i in range(randint(5, 10)):
        rating = randint(min_rating, 5)
        Evaluation.objects.create(instructor=instructor, course=course, score=rating)








