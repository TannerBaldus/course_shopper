__author__ = 'tanner'
from duckweb_session import DuckwebSession


def parse_eval_tag(eval_tag):

    rows = eval_tag.find_all('td')
    labels = ['subject', 'number', 'title', 'term', 'q1', 'q2', 'q3', 'q4', 'q5']
    label_mapping = dict(zip(labels, rows))
    term = label_mapping['term'].split(' ')
    term = dict(season=term[0], year=int(term[1]))
    course = dict(subject=label_mapping['subject'], title=label_mapping['title'], number=label_mapping['number'])
    return dict(course=course, term=term)



