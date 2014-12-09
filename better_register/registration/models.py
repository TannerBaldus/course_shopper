from django.db import models
import  managers

class Instructor(models.Model):
    fname = models.CharField(max_length=256)
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
    location = models.ForeignKey(Location)
    crn = models.IntegerField(unique=True, primary_key=True)

    class Meta:
        abstract = True


class Offering(BaseOfferingInfo):
    instructor = models.ForeignKey(Instructor, related_name='offerings')
    course = models.ForeignKey(Course)
    credits = models.IntegerField(null=True)
    objects = managers.OfferingManager()

    def __unicode__(self):
        return "{} {} taught by {} {} on {} in {} {}".format(self.course.subject.code, self.course.number, self.instructor.fname,
                                              self.instructor.lname, self.days, self.location.building, self.location.room)


class AssociatedSection(BaseOfferingInfo):
    instructor = models.ForeignKey(Instructor, related_name='associated_sections')
    offering = models.ForeignKey(Offering)


    def __unicode__(self):
        return ' Associated Section taught by {} {} on {}'.format(self.instructor.fname,
                                                                  self.instructor.lname, self.days)


class Evaluation(models.Model):
    instructor = models.ForeignKey(Instructor, related_name='evals')
    course = models.ForeignKey(Course, related_name='evals')
    score = models.IntegerField()
    objects = managers.EvaluationManager()

    def __unicode__(self):
        return "{} {} taught by {} {} score: {}".format(self.course.subject.code, self.course.number,
                                                                 self.instructor.fname, self.instructor.lname, self.score)
