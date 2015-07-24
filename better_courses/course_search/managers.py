from course_search.common_ops import db_common_ops
import  re

__author__ = 'tanner'
from django.db import models
from django.db.models import Avg, Sum
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from course_search.common_ops import name_ops
import operator


def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):

    """
    Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    """
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def keyword_search(query_string, search_fields):
    query = None
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
        return query

class OfferingManager(models.Manager):



    def get_queryset(self):
        return super(OfferingManager, self).get_queryset().select_related()

    def search_by_instructor(self, fname, lname):
        return self.filter(instructor__fname=fname, instructor__lname=lname)




    def offering_by_query(self, q):
        from models import Subject
        query_lst = normalize_query(q)
        subject_codes = Subject.objects.values_list('code', flat=True)
        course_regex = re.compile('\w{2,4} \d{3}\w{0,1}')
        subject_regex = re.compile('\w{3,4}')
        if query_lst[0].upper() in subject_codes:
            if len(query_lst) == 1:
             return self.filter(course__subject__code=q.upper())
            elif re.match(course_regex):
                code, number = query_lst
                return self.filter(course__subject__code=code.upper(), course__number=number)

        search_fields = ['course__desc', 'course__title']
        return self.filter(keyword_search(q,search_fields))







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


    def get_or_create_offering(self, crn, course, meetings, instructors, term, **kwargs):
        print course

        try:
            offering = self.get(crn=crn)
            return offering, False

        except ObjectDoesNotExist:
            return self.create_offering(crn, course, meetings, instructors, term, **kwargs), True


    def create_offering(self, crn, course, meetings, instructors, term, **kwargs):
        """

        :param crn:
        :param course:
        :param meetings:
        :return:
        """
        from models import Meeting, Course, Instructor, Term

        term = Term.objects.get_or_create(**term)[0]
        course = Course.objects.get_or_create_course(**course)[0]
        offering = self.create(crn=crn, term=term, course=course, **kwargs)
        added_m2m_fields = 0
        added_m2m_fields += db_common_ops.add_kwargs_to_m2m(offering.instructors, Instructor.objects.update_or_create,
                                                            instructors)
        added_m2m_fields += db_common_ops.add_kwargs_to_m2m(offering.meetings, Meeting.objects.get_or_create_meeting,
                                                            meetings)
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

    def average_rating(self):
        total_responses  =  self.aggregate(Sum("responses"))["responses__sum"]
        return sum([i.weighted_average(total_responses) for i in self.all()])

    def get_or_create_evaluation(self, instructor, term, course, responses, course_quality, teaching_quality,
                                 organization, class_time_use, communication, grading_clarity, amount_learned):

        from models import Instructor, Term, Course

        instructor, instructor_created = Instructor.objects.update_or_create(**instructor)
        course, course_created = Course.objects.get_or_create_course(**course)
        term, term_created = Term.objects.get_or_create(**term)

        if not (instructor_created or course_created or term_created):
            try:
                return self.get(term=term, course=course, instructor=instructor), False

            except ObjectDoesNotExist:
                pass

        return self.create(instructor=instructor, course=course, term=term, responses=responses, course_quality=course_quality,
                           organization=organization, class_time_use=class_time_use, communication=communication,
                           grading_clarity=grading_clarity, amount_learned=amount_learned,
                           teaching_quality=teaching_quality), True

class InstructorManager(models.Manager):


    def create(self,fname,middle,lname,email=None):
        new_model = self.model(fname=fname,middle=middle,lname=lname, email=email)
        new_model.full_name = name_ops.to_full(fname, middle, lname)
        new_model.save()
        return new_model


    def get_queryset(self):
        return super(InstructorManager, self).get_queryset().select_related()

    def search_by_evaluation(self, rating, eval_rating_fn):
        offering_pairs = filter(lambda i: i['avg_score'] >= rating, eval_rating_fn)
        instructors = [i['instructor'] for i in offering_pairs]
        return self.filter(id__in=instructors)


    def update_or_create(self, fname, middle, lname, email=None):
        results = self.filter(fname=fname, lname=lname)
        results_count = results.count()
        if results_count == 0:
            return self.create(fname=fname, middle=middle, lname=lname), True

        for result in results:
            print result.middle == middle
            new_middle, isMatch = name_ops.match_middle_name(middle, result.middle)
            print isMatch
            if isMatch:
                result.update_middle(new_middle)
                return result, False

        return self.create(fname=fname, middle=middle, lname=lname), True



class CourseManager(models.Manager):
    def create_course(self, title, number, min_credits, max_credits, subject, web_resources=[], gen_eds=[], notes=[],
                      **kwargs):
        """


        """
        from models import Subject, Note, GenEd, WebResource

        subject = Subject.objects.get_or_create_subject(**subject)[0]
        course = self.create(title=title, number=number, min_credits=min_credits, max_credits=max_credits,
                             subject=subject, **kwargs)

        new_m2m_relations = 0
        new_m2m_relations += db_common_ops.add_kwargs_to_m2m(course.notes, Note.objects.get_or_create, notes)
        new_m2m_relations += db_common_ops.add_kwargs_to_m2m(course.gen_eds, GenEd.objects.get_or_create, gen_eds)
        new_m2m_relations += db_common_ops.add_kwargs_to_m2m(course.web_resources, WebResource.objects.get_or_create,
                                                             web_resources)
        if new_m2m_relations:
            course.save()

        return course

    def get_or_create_course(self, title, subject, number, min_credits=0, max_credits=0, defaults=None, **kwargs):
        """
        Tries to get a course instance based on the subject_code, number and title only. If
        If a course instance is found and a non blank description is given;
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
            course = self.get(title=title, subject__code=subject['code'], number=number)
            return course, False

        except ObjectDoesNotExist:
            course = self.create_course(title=title, subject=subject, number=number,
                                        min_credits=min_credits, max_credits=max_credits, **kwargs)
            return course, True

    def update_or_create_course(self, title, subject, number, min_credits=0, max_credits=0, defaults=None, **kwargs):
        course, created = self.get_or_create_course(title, subject, number, min_credits, max_credits,
                                                    defaults=None, **kwargs)
        if not created:
            course.update_course(min_credits=min_credits, max_credits=max_credits, **kwargs)

        return course, created

    def offered_by_term(self, season, year):
        return self.filter(offering__term__season=season, offering__term__year=year)

    def by_subject_code(self, subj_code):
        return self.filter(subject__code=subj_code)

    def by_subj_code_and_number(self, subj_code, number):
        return self.filter(subject__code=subj_code, number=number)

    @property
    def average_rating(self):
        pass




class MeetingManager(models.Manager):

    def get_or_create_meeting(self, location, date_period):
        from models import Location, DatePeriod

        date_period_obj, date_period_created = DatePeriod.objects.get_or_create(**date_period)
        location_obj, location_created = Location.objects.get_or_create(**location)

        if date_period and location_created:
            return self.create(date_period=date_period_obj, location=location_obj), True

        try:
            meeting = self.get(location=location_obj, date_period=date_period_obj)
            return meeting, False

        except ObjectDoesNotExist:
            return self.create(location=location_obj, date_period=date_period_obj), True


class AssociatedSectionManager(models.Manager):

    def create_associated_section(self, crn, offering, instructors=[], meetings=[], **kwargs):
        from models import Instructor, Meeting, Offering

        offering = Offering.objects.get(**offering)
        associated_section = self.create(crn=crn, offering=offering, **kwargs)
        new_m2m_fields = db_common_ops.add_kwargs_to_m2m(associated_section.instructors,
                                                         Instructor.objects.update_or_create, instructors)
        new_m2m_fields += db_common_ops.add_kwargs_to_m2m(associated_section.meetings,
                                                          Meeting.objects.get_or_create_meeting, meetings)
        if new_m2m_fields > 0:
            associated_section.save()
        return associated_section

    def get_or_create_associated_section(self, crn, offering, instructors=[], meetings=[], **kwargs):
        try:
            associated_section = self.get(crn=crn)
            return associated_section, False

        except ObjectDoesNotExist:
            associated_section = self.create_associated_section(crn, offering, instructors=instructors,
                                                                meetings=meetings, **kwargs)
            return associated_section, True


class SubjectManager(models.Manager):

    def find_by_subject_or_code(self, code, subject):

        assert code or subject, "Need to have at least code or subject"

        try:
            if not code:
                subject_model = self.get(subject=subject)
            else:
                subject_model = self.get(code=code)
            return subject_model
        except ObjectDoesNotExist:
             return False

    def get_or_create_subject(self, code, subject):
        subject_model = self.find_by_subject_or_code(code, subject)
        if subject_model:
            return subject_model, False
        return self.create(code=code, subject=subject), True

    def update_or_create_subject(self, code, subject):
        subject_model, created = self.get_or_create_subject(code, subject)
        if not created:
            subject_model.update(code, subject)
















