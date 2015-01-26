__author__ = 'tanner'
from ..common_ops import get_labeled_rows, convert_and,
from better_register.registration.logged_in_sessions import DuckwebSession


def parse_eval_row(labeled_row):
    course = dict(subject=convert_and(labeled_row['subject']), number=labeled_row['number'], title=labeled_row['title'])
    season, year = labeled_row['term'].split(' ')
    term = dict(season=season, year=int(year))
    questions = {k:v for (k,v) in labeled_row.iteritems() if 'q' in k}



def parse_eval_table(eval_tag):
    questions  = ['q{}'.format(i) for i in range(1, 8)]
    labels = ['subject', 'number', 'title', 'term'] + questions + ['responses']
    rows = get_labeled_rows(labels)
    return parse_eval_row(rows)



def get_evals():
    duckweb_session = DuckwebSession()






