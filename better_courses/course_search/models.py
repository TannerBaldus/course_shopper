from django.db import models
import managers
import db_common_ops


class Instructor(models.Model):
    fname = models.CharField(max_length=256)
    middle = models.CharField(max_length=256, null=True)
    lname = models.CharField(max_length=256)
    email = models.EmailField(null=True)
    objects = managers.InstructorManager()

    def __unicode__(self):
        return "{} {}".format(self.fname, self.lname)


class Location(models.Model):
    building = models.CharField(max_length=256)
    room = models.CharField(max_length=150, null=True)

    class meta:
        unique_together = (('building', 'room'),)

    def __unicode__(self):
        return '{} {}'.format(self.building, self.room)


class DatePeriod(models.Model):
    day = models.CharField(max_length=3)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    class meta:
        unique_together = (('day', 'start_time', 'end_time', 'start_date', 'end_date'),)

    def __unicode__(self):
        message = "{} {}-{}".format(self.day, self.start_time, self.end_time)
        if self.calendar_day:
            message += " on {}".format(self.calendar_day)
        return message


class Meeting(models.Model):
    location = models.ForeignKey(Location)
    date_period = models.ForeignKey(DatePeriod)
    objects = managers.MeetingManager()

    class meta:
        unique_together = (('location', 'date_period'),)

    def __unicode__(self):
        return 'Course Meeting at {} on {}'.format(self.location, self.date_period)


class Subject(models.Model):
    code = models.CharField(max_length=8, unique=True, primary_key=True)
    subject = models.CharField(max_length=256)

    def __unicode__(self):
        return "code: {} subject name:{}".format(self.code, self.subject)


class Course(models.Model):
    title = models.TextField()
    number = models.IntegerField()
    subject = models.ForeignKey(Subject)
    min_credits = models.FloatField()
    max_credits = models.FloatField()

    gen_eds = models.ManyToManyField('GenEd', related_name='courses')
    desc = models.TextField(null=True)
    prereq_text = models.TextField(null=True)

    fee = models.FloatField(default=0.0)
    fee_per_credit = models.BooleanField(default=False)
    notes = models.ManyToManyField('Note', related_name='courses')
    web_resources = models.ManyToManyField('WebResource', related_name='courses')
    objects = managers.CourseManager()

    class meta:
        unique_together = ('title', 'number', 'subject')

    def __unicode__(self):
        return "{} {} {}".format(self.subject.code, self.number, self.title)


    def update_course(self, **kwargs):

        print kwargs

        simple_fields = ['min_credits', 'max_credits','desc','fee', 'fee_per_credit', 'prereq_text']
        simple_fields_changed = db_common_ops.update_simple_fields(self, simple_fields, **kwargs)
        m2m_fields_changed = db_common_ops.update_m2m(self.gen_eds, GenEd, 'code', kwargs.get('gen_eds', []))
        m2m_fields_changed += db_common_ops.update_m2m(self.web_resources, WebResource, ['link_text', 'link_url'],
                                                       kwargs.get('web_resources', []))
        m2m_fields_changed += db_common_ops.update_m2m(self.notes, Note, 'code', kwargs.get('notes', []))
        if m2m_fields_changed + simple_fields_changed:
            self.save()


class Term(models.Model):
    season = models.CharField(max_length=7)
    year = models.IntegerField()

    class meta:
        unique_together = ('season', 'year')



class BaseOfferingInfo(models.Model):
    crn = models.IntegerField(unique=True, primary_key=True)
    meetings = models.ManyToManyField(Meeting)
    open_seats = models.IntegerField()
    total_seats = models.IntegerField()
    class Meta:
        abstract = True


class Offering(BaseOfferingInfo):
    instructors = models.ManyToManyField(Instructor, related_name='offerings')
    course = models.ForeignKey(Course)
    objects = managers.OfferingManager()
    term = models.ForeignKey(Term,related_name='offerings')



    def __unicode__(self):
        return "Offering of {} {}".format(self.course.subject.code, self.course.number)


class AssociatedSection(BaseOfferingInfo):
    instructors = models.ManyToManyField(Instructor, related_name='associated_sections')
    offering = models.ForeignKey(Offering)
    term = models.ForeignKey(Term, related_name='associated_sections')
    objects = managers.AssociatedSectionManager()

    def __unicode__(self):
        return ' Associated Section of {}'.format(self.offering)


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
