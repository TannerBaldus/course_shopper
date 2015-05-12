__author__ = 'tanner'
from ...common_ops.parser_ops import labeled_rows_from_list, convert_and, flatten_dict_values
from  ...common_ops.name_ops import parse_name, reorder_comma_delimited_name

def parse_eval_row(labeled_row_dict):
    subject = dict(subject=convert_and(labeled_row_dict['subject']), code='')
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


def is_complete_eval(eval_dict):
    """
    Checks to make sure no data is missing from the eval scraped. It does this by checking the flattened eval dictonary
    that there are no more than 1 blank string. One blank string is allowable because there is no subject code.
    :param eval_dict:
    :return:
    """
    return flatten_dict_values(eval_dict).count('') == 1

def get_evals_table(eval_soup):
        tbody_tags = eval_soup.find_all('tbody')
        if len(tbody_tags) != 3:
            return None
        tbody = tbody_tags[2]
        return tbody.find_all('tr', class_='even') + tbody.find_all('tr', class_='odd')


def parse_eval(instructor_name, eval_soup):
    eval_rows = get_evals_table(eval_soup)
    instructor_name = parse_name(reorder_comma_delimited_name(instructor_name))
    if eval_rows:
        for evaluation in parse_eval_table(eval_rows):
            if is_complete_eval(evaluation):
                yield dict(evaluation, instructor=instructor_name)

















