__author__ = 'tanner'
from optparse import make_option

from course_search.models import Offering, AssociatedSection, Subject
from django.core.management.base import BaseCommand, CommandError
from better_courses.settings import UPDATE_OFFERINGS_FN
from course_search.common_ops.management_ops import get_func_from_string


class Command(BaseCommand):
    args = 'season year'
    help = 'Updates the offerings in the database fora given season and year using the UPDATE_OFFERINGS_FN ' \
           'specified in the settings '

    option_list = BaseCommand.option_list + (
            make_option(
                "--subjects",
                default=False,
                dest = "subjects",
                help = "a space delimited string of subject codes whose offerings to update",
                metavar = "CODE(S)"
            ),


    )

    option_list = option_list + (
            make_option(
                "--start_at",
                default = False,
                dest = "start",
                help = "a subject code to start at when iterating over subjects alphabetically to update offerings",
                metavar = "CODE"
            ),
        )



    def handle(self, *args, **options):
        if len(args) < 2:
            raise CommandError('There must be 2 arguments. Season and year.')

        season, year = args
        try:
            year = int(year)
        except ValueError:
            raise CommandError('2nd arg year must be an integer')

        user_subjects = options['subjects']
        starting_subject = options['start']

        if starting_subject and user_subjects:
            raise CommandError('--subjects and --start are mutually exclusive')

        subject_codes_in_db = Subject.objects.values_list('code', flat=True).order_by('code')

        if starting_subject:
            subject_codes = self.handle_starting_subject(starting_subject,subject_codes_in_db)

        elif user_subjects:
            subject_codes = self.handle_user_subjects(user_subjects, subject_codes_in_db)

        else:
            subject_codes = subject_codes_in_db

        update_offerings_fn = get_func_from_string(UPDATE_OFFERINGS_FN)
        for offering_dict in update_offerings_fn(season, year, subject_codes):
            result_type = offering_dict.get('result_type')
            if result_type == 'offering':
                Offering.objects.get_or_create_offering(**offering_dict.get('data'))

            elif result_type == 'associated_section':
                AssociatedSection.objects.get_or_create_associated_section(**offering_dict.get('data'))


    def handle_starting_subject(self, starting_subject, subject_codes_in_db):
            subject_codes = list(subject_codes_in_db)
            try:
                starting_index = subject_codes.index(starting_subject)
            except ValueError:
                raise ValueError('{} subject code not in database'.format(starting_subject))
            return subject_codes[starting_index:]

    def handle_user_subjects(self, user_subjects, subject_codes_in_db):
            subject_codes = user_subjects.split(' ')
            for subject_code in subject_codes:
                if subject_code not in subject_codes_in_db:
                    raise ValueError('{} subject code not in database'.format(subject_code))
            return subject_codes




