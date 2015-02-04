__author__ = 'tanner'
from ..common_ops import get_labeled_rows, convert_and
from better_register.course_search.logged_in_sessions import DuckwebSession


def parse_eval_row(labeled_row):
    course = dict(subject=convert_and(labeled_row['subject']), number=labeled_row['number'], title=labeled_row['title'])
    season, year = labeled_row['term'].split(' ')
    term = dict(season=season, year=int(year))

    questions = {k: v for (k, v) in labeled_row.iteritems() if k not in ['subject', 'number', 'title', 'term']}
    return dict(questions, course=course, term=term)


def parse_eval_table(eval_table):
    questions = ["course_quality", "teaching_quality", "organization", "class_time_use ", "communication",
                 "grading_clarity", "amount_learned"]

    labels = ['subject', 'number', 'title', 'term'] + questions + ['responses']
    rows = get_labeled_rows(labels, eval_table)
    for row in rows:
        yield parse_eval_row(row)


def get_evals():
    duckweb_session = DuckwebSession()







