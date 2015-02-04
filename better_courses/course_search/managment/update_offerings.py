__author__ = 'tanner'
__author__ = 'tanner'
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'username password'
    help = 'Updates '

    def handle(self, *args, **options):



            raise CommandError('There must be 2 arguments. Username and passowrd.')
        try:
            pass