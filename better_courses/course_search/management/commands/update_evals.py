__author__ = 'tanner'
from better_courses.settings import UPDATE_EVALS_FN
import logging
from course_search.models import Evaluation, Subject
from _command_common_ops import get_func_from_string
from django.core.management.base import BaseCommand, CommandError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Command(BaseCommand):
    args = 'username password'
    help = 'Updates '


    def handle(self, *args, **options):
        if 2 > len(args) < 2:
            raise CommandError('There must be 2 arguments. Username and passowrd.')
        update_evals_fn = get_func_from_string(UPDATE_EVALS_FN)
        username, password = args
        for eval_kwargs in update_evals_fn(username, password):
            logger.info('Eval Kwargs:\n{}'.format(eval_kwargs))
            if Subject.objects.find_by_subject_or_code(**eval_kwargs['course']['subject']):
                logger.info('Teaches a subject {} in the DB'.format(eval_kwargs['course']['subject']['code']))
                Evaluation.objects.get_or_create_evaluation(**eval_kwargs)
