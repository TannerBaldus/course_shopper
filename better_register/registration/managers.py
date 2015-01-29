__author__ = 'tanner'
from django.db import models
from django.db import connection
from django.db.models import Avg
from django.db.models import Q
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


    def get_or_create(self, title, code, number, desc='', defaults=None, **kwargs):
        """
        Tries to get a course instance based on the subject_code, number and title only.
        If a course instance is found and a non blank description is given; the course
        instance's description will be updated.
        If no instance is found a new course instance is created.

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
            if desc and course.desc != desc:
                course.update(desc=desc)
            return course

        except self.DoesNotExist:
            from models import Subject
            subject = Subject.get(code=code)
            self.create(title=title, subject=subject, number=number, desc=desc)










