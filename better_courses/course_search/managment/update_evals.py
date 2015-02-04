__author__ = 'tanner'
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'username password'
    help = 'Updates '

    def handle(self, *args, **options):
        if 2 > len(args) < 2:
            raise CommandError('There must be 2 arguments. Username and passowrd.')
        try:
            pass