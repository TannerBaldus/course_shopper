__author__ = 'tanner'
import logging

from better_courses.settings import UPDATE_EVALS_FN
from course_search.models import Evaluation, Subject
from course_search.common_ops.management_ops import get_func_from_string
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    args = 'username password'
    help = 'Updates '

    option_list = BaseCommand.option_list + (
        make_option(
            "--start_lname",
            "-s",
            default='',
            dest="start_lname",
            help="Update evals of all instructor with the last name >= to this name",
            metavar="LAST_NAME"
        ),


    )

    option_list = option_list + (
        make_option(
            "--end_lname",
            "-e",
            default=None,
            dest="end_lname",
            help="Update evals of all instructor with the last name <= to this name",
            metavar="LAST_NAME"
        ),
    )

    def handle(self, *args, **options):
        if 2 > len(args) < 2:
            raise CommandError('There must be 2 arguments. Username and passowrd.')
        update_evals_fn = get_func_from_string(UPDATE_EVALS_FN)
        username, password = args
        start_lname = options['start_lname']
        end_lname= options['end_lname']


        for eval_kwargs in update_evals_fn(username=username, password=password,
                                           start_lname=start_lname, end_lname=end_lname):

            logger.info('Eval Kwargs:\n{}'.format(eval_kwargs))
            if Subject.objects.find_by_subject_or_code(**eval_kwargs['course']['subject']):
                logger.info('Teaches a subject {} in the DB'.format(eval_kwargs['course']['subject']['code']))
                Evaluation.objects.get_or_create_evaluation(**eval_kwargs)
