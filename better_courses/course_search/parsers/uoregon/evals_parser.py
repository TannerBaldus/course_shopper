__author__ = 'tanner'
from ..common_ops import labeled_rows_from_list, convert_and, parse_name, flatten_dict_values
from  ..parser_error import ParserError
from course_search.logged_in_sessions.duckweb_session import DuckwebSession
from bs4 import BeautifulSoup


def parse_eval_row(labeled_row_dict):
    subject = dict(subject=convert_and(labeled_row_dict['subject']),code='')
    course = dict(subject=subject, number=labeled_row_dict['number'], title=labeled_row_dict['title'])
    season, year = labeled_row_dict['term'].split(' ')[0:2]  #Remove extraneous info e.g. Summer 2010 Final to Summer 2010
    term = dict(season=season, year=int(year))

    questions = {k: v for (k, v) in labeled_row_dict.iteritems() if k not in ['subject', 'number', 'title', 'term']}
    return dict(questions, course=course, term=term)


def parse_eval_table(eval_rows):
    questions = ["course_quality", "teaching_quality", "organization", "class_time_use", "communication",
                 "grading_clarity", "amount_learned"]

    labels = ['subject', 'number', 'title', 'term'] + questions + ['responses']
    rows = labeled_rows_from_list(eval_rows, labels)
    for row in rows:
        yield parse_eval_row(row)

def reorder_name(instructor_name):
    """

    :param instructor_name:
    :return:
    """
    name_lst = instructor_name.split(', ')
    return ' '.join(name_lst[1:]+[name_lst[0]])

def is_complete_eval(eval_dict):
    """
    Checks to make sure no data is missing from the eval scraped. It does this by checking the flattened eval dictonary
    that there are no more than 1 blank string. One blank string is allowable because there is no subject code.
    :param eval_dict:
    :return:
    """

    return flatten_dict_values(eval_dict).count('') == 1

def parse_eval(instructor_name, eval_rows):
    instructor_dict = parse_name(reorder_name(instructor_name))
    for evaluation in parse_eval_table(eval_rows):
        if is_complete_eval(evaluation):
            yield dict(evaluation, instructor=instructor_dict)
















