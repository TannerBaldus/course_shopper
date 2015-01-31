from django.db import models
import managers

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
    end_date= models.DateField

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
    gen_eds = models.ManyToManyField(GenEd, related_name='courses')
    desc = models.TextField()
    fee = models.FloatField(default=0.0)

    class meta:
        unique_together = ('title', 'number', 'subject')

    def __unicode__(self):
        return "{} {} {}".format(self.subject.code, self.number, self.title)


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
