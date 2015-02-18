__author__ = 'tanner'
from django.db import models
from django.db import connection
from django.db.models import Avg
from django.db.models import Q
import  db_common_ops
import operator

class OfferingManager(models.Manager):

    def get_queryset(self):
        return super(OfferingManager, self).get_queryset().select_related()

    def search_by_instructor(self, fname, lname):
        return self.filter(instructor__fname=fname, instructor__lname=lname)



    def search_by_evaluation(self, rating, eval_rating_fn):
        """
        Ch
        :param eval_rating_fn: function to make evaluation averages list
        :return:
        """
        offering_pairs = filter(lambda i: i['avg_score'] >= rating, eval_rating_fn())
        if not offering_pairs:
            return self.none()
        queries = [Q(course=i['course'], instructor=i['instructor']) for i in offering_pairs]
        query = reduce(operator.or_, queries)
        return self.filter(query)

    def create_offering(self, crn, course, meetings, instructors, term, **kwargs):
        """

        :param crn:
        :param course:
        :param meetings:
        :return:
        """
        from models import Meeting, Course, Instructor, Term
        term = Term.objects.get_or_create(**term)
        course = Course.objects.get_or_create(**course)
        offering = self.create(crn=crn,term=term,course=course,**kwargs)
        added_m2m_fields = 0
        added_m2m_fields+= db_common_ops.add_kwargs_to_m2m(offering.instructors, Instructor.objects, instructors)
        added_m2m_fields+= db_common_ops.add_kwargs_to_m2m(offering.meetings,  Meeting.objects, meetings)
        if added_m2m_fields:
            offering.save()



class EvaluationManager(models.Manager):

    def get_queryset(self):
        return super(EvaluationManager, self).get_queryset().select_related('instructor', 'course')

    def avg_offering_ratings(self):
        return self.values('instructor', 'course').annotate(avg_score=Avg('score'))

    def avg_ins_ratings(self):
        return self.values('instructor').annotate(avg_score=Avg('score'))

    def by_instructor(self, fname, lname):
        return self.filter(instructor_fname=fname, instructor_lname=lname)

    def by_score(self, score):
        return self.filter(score__gte=score)


class InstructorManager(models.Manager):

    def get_queryset(self):
        return super(InstructorManager, self).get_queryset().select_related()

    def search_by_evaluation(self, rating, eval_rating_fn):
        offering_pairs = filter(lambda i: i['avg_score'] >= rating, eval_rating_fn())
        instructors = [i['instructor'] for i in offering_pairs]
        return self.filter(id__in=instructors)


class CourseManager(models.Manager):

    def create_course(self, title, number, credits, subject, gen_eds=[], notes=[], **kwargs):
        """

        :param title:
        :param number:
        :param credits:
        :param defaults:
        :param kwargs:
        :return:
        """
        from models import Subject, Note, GenEd
        subject = Subject.objects.get_or_create(**subject)[0]
        course = self.create(title=title, number=number, credits=credits, subject=subject, **kwargs)
        new_m2m_relations = 0
        new_m2m_relations += db_common_ops.add_kwargs_to_m2m(course.notes, Note.objects, notes)
        new_m2m_relations += db_common_ops.add_kwargs_to_m2m(course.gen_eds, GenEd.objects, gen_eds)
        if new_m2m_relations:
            course.save()


    def get_or_create(self, title, code, number, defaults=None, **kwargs):
        """
        Tries to get a course instance based on the subject_code, number and title only.
        If a course instance is found and a non blank description is given; the course
        instance's description will be updated.
        If no instance is found a new course instance is created.
a
        :param title:
        :param code:
        :param number:
        :param desc:
        :param defaults:
        :param kwargs:
        :return:

        """

        try:
            course = self.get(title=title, subject__code=code, number=number)
            course.update(credits=credits, **kwargs)
            return course, False

        except self.DoesNotExist:
            course = self.create(title=title, number=number, credits=credits, **kwargs)
            return course, True




class MeetingManager(models.Manager):

    def get_or_create_meeting(self, location, date_period):
        from models import Location, DatePeriod
        date_period_obj,date_period_created = DatePeriod.objects.get_or_create(**date_period)
        location_obj, location_created = Location.objects.get_or_create(**location)

        if date_period and location_created:
            return self.create(date_period=date_period_obj,location=location), True

        try:
            meeting = self.get(location=location_obj, date_period=date_period_obj)
            return meeting, False

        except self.DoesNotExist:
            return self.create(location=location_obj, date_period=date_period_obj), True














