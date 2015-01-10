from django.db import models
import  managers

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
    calendar_day = models.DateField(null=True)

    class meta:
        unique_together = (('day', 'start_time','end_time', 'calendar_day'),)

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

    class meta:
        unique_together = ('title', 'number', 'subject')

    def __unicode__(self):
        return "{} {} {}".format(self.subject.code, self.number, self.title)


class BaseOfferingInfo(models.Model):

    days = models.CharField(max_length=7)
    crn = models.IntegerField(unique=True, primary_key=True)
    meeting = models.ForeignKey(Meeting)
    evals = models.ManyToManyField('Evaluation')

    class Meta:
        abstract = True


class Term(models.Model):
    season = models.CharField(max_length=7)
    year = models.IntegerField()

    class meta:
        unique_together = ('season', 'year')


class Offering(BaseOfferingInfo):
    instructor = models.ForeignKey(Instructor, related_name='offerings')
    course = models.ForeignKey(Course)
    credits = models.IntegerField(null=True)
    start = models.DateField(null=True)
    end = models.DateField(True)
    objects = managers.OfferingManager()


    def __unicode__(self):
        return "Offering {} taught by {} {} meeting: {}".format(self.course, self.instructor, self.meeting)


class AssociatedSection(BaseOfferingInfo):
    instructor = models.ForeignKey(Instructor, related_name='associated_sections')
    offering = models.ForeignKey(Offering)

    def __unicode__(self):
        return ' Associated Section of {} taught by {} on {}'.format(self.offering, self.instructor, self.meeting)


class Evaluation(models.Model):
    instructor = models.ForeignKey(Instructor, related_name='evals')
    course = models.ForeignKey(Course, related_name='evals')
    score = models.IntegerField()
    objects = managers.EvaluationManager()

    def __unicode__(self):
        return "{} {} taught by {} {} score: {}".format(self.course.subject.code, self.course.number,
                                                        self.instructor.fname, self.instructor.lname, self.score)


class WebResource(models.Model):
    link_text = models.TextField()
    link_url = models.TextField()

class Note(models.Model):
    code =  models.TextField()
    desc = models.TextField()