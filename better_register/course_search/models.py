from django.db import models
import managers
import db_common_ops

class Instructor(models.Model):
    fname = models.CharField(max_length=256)
    middle = models.CharField(max_length=256)
    lname = models.CharField(max_length=256)
    objects = managers.InstructorManager()

    def __unicode__(self):
        return "{} {}".format(self.fname, self.lname)


class Location(models.Model):
    building = models.CharField(max_length=256)
    room = models.CharField(max_length=150, null=True)

    class meta:
        unique_together = (('building', 'room'),)

    def __unicode__(self):
        return '{} {}'.format(self.building,self.room)


class DatePeriod(models.Model):
    day = models.CharField(max_length=1)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date= models.DateField(null=True)

    class meta:
        unique_together = (('day', 'start_time','end_time', 'start_date', 'end_date'),)

    def __unicode__(self):
        message =  "{} {}-{}".format(self.day, self.start_time, self.end_time)
        if self.calendar_day:
            message += " on {}".format(self.calendar_day)
        return message



class Meeting(models.Model):
    location = models.ForeignKey(Location)
    date_period = models.ForeignKey(DatePeriod)

    class meta:
        unique_together = (('location','date_period'),)

    def __unicode__(self):
        return 'Course Meeting at {} on {}'.format(self.location, self.date_period)


class Subject(models.Model):
    code = models.CharField(max_length=8, unique=True, primary_key=True)
    subject = models.CharField(max_length=256)

    def __unicode__(self):
        return "{}:{}".format(self.code, self.subject)


class Course(models.Model):
    title = models.TextField()
    number = models.IntegerField()
    subject = models.ForeignKey(Subject)
    credits = models.IntegerField()
    geneds = models.ManyToManyField('GenEd', related_name='courses')
    desc = models.TextField(null=True)
    prereq_text = models.TextField(null=True)
    fee = models.FloatField(default=0.0)

    class meta:
        unique_together = ('title', 'number', 'subject')

    def __unicode__(self):
        return "{} {} {}".format(self.subject.code, self.number, self.title)



    def update_gends(self, gen_ed_list):

        old_gen_eds = {i.code: i for i in self.geneds.all() if i.code not in gen_ed_list}

        if not gen_ed_list and self.geneds.all():
            self.geneds.clear()
            return 1

        else:
            new_gen_eds = 0
            updated_gen_eds = []

            for gen_ed_dict in gen_ed_list:

                if gen_ed_dict.get('code') not in old_gen_eds:
                    gen_ed = GenEd.objects.get_or_create(**gen_ed_dict)
                    updated_gen_eds.append(gen_ed)
                    new_gen_eds += 1

            if new_gen_eds > 0:
                self.geneds.remove(*old_gen_eds.values())
                self.geneds.add(*updated_gen_eds)

            return new_gen_eds

    def update_course(self, **kwargs):
        no_update = ['evals', 'subject_id', 'subject', 'title', 'number']
        m2m_relations =['geneds']
        foreign_keys = ['subject']

        is_simple_field = lambda field: field not in(m2m_relations+no_update+foreign_keys)
        simple_fields = [field for field in self._meta.get_all_field_names() if is_simple_field(field)]

        simple_fields_changed = db_common_ops.update_simple_fields(self, simple_fields, **kwargs)
        new_geneds, old_geneds =  db_common_ops.get_new_old(self.geneds,GenEd,'code', kwargs['geneds'])
















class BaseOfferingInfo(models.Model):

    crn = models.IntegerField(unique=True, primary_key=True)
    meetings = models.ForeignKey(Meeting)

    class Meta:
        abstract = True


class Term(models.Model):
    season = models.CharField(max_length=7)
    year = models.IntegerField()

    class meta:
        unique_together = ('season', 'year')


class Offering(BaseOfferingInfo):
    instructors = models.ManyToManyField(Instructor, related_name='offerings')
    course = models.ForeignKey(Course)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    objects = managers.OfferingManager()


    def __unicode__(self):
        return "Offering {} taught by {} {} meeting: {}".format(self.course, self.instructor, self.meeting)


class AssociatedSection(BaseOfferingInfo):
    instructor = models.ManyToManyField(Instructor, related_name='associated_sections')
    offering = models.ForeignKey(Offering)

    def __unicode__(self):
        return ' Associated Section of {} taught by {} on {}'.format(self.offering, self.instructor, self.meeting)


class Evaluation(models.Model):

    instructor = models.ForeignKey(Instructor, related_name='evals')
    course = models.ForeignKey(Course, related_name='evals')
    term = models.ForeignKey(Term, related_name='evals')
    responses = models.IntegerField()

    course_quality = models.FloatField()
    teaching_quality = models.FloatField()
    organization = models.FloatField()
    class_time_use = models.FloatField()
    communication = models.FloatField()
    grading_clarity = models.FloatField()
    amount_learned = models.FloatField()

    objects = managers.EvaluationManager()

    def __unicode__(self):
        return "{} {} taught by {} {} score: {}".format(self.course.subject.code, self.course.number,
                                                        self.instructor.fname, self.instructor.lname, self.score)


class WebResource(models.Model):
    link_text = models.TextField()
    link_url = models.TextField()

class Note(models.Model):
    code = models.TextField()
    desc = models.TextField()

class GenEd(models.Model):
    code = models.CharField(max_length=6)
    gen_ed = models.CharField(max_length=256)
