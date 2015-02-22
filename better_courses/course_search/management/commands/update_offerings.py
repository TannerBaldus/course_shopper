__author__ = 'tanner'
from optparse import make_option
from course_search.models import Offering, AssociatedSection
from django.core.management.base import BaseCommand, CommandError
from better_courses.settings import UPDATE_OFFERINGS_FN
from _command_common_ops import get_func_from_string

class Command(BaseCommand):
    args = 'season year'
    help = 'Updates '

    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError('There must be 2 arguments. Season and year.')

        season, year = args
        try:
            year = int(year)
        except ValueError:
            raise CommandError('2nd arg year must be an integer')

        update_offerings_fn = get_func_from_string(UPDATE_OFFERINGS_FN)

        for offering_dict in update_offerings_fn(season, year):
            result_type = offering_dict.get('result_type')
            if result_type == 'offering':
                Offering.objects.get_or_create_course(offering_dict.get('data'))

            elif result_type == 'associated_section':
                AssociatedSection.objects.get_or_create(offering_dict.get('data'))





