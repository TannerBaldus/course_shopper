__author__ = 'tanner'
from better_courses.settings import GET_SUBJECTS_FN
from course_search.models import Subject
from course_search.management.commands._command_common_ops import get_func_from_string
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fills the db with the subject codes'

    def handle(self, *args, **options):
        get_subject_fn = get_func_from_string(GET_SUBJECTS_FN)
        for subject_kwargs in get_subject_fn():
            print subject_kwargs
            Subject.objects.get_or_create_subject(**subject_kwargs)