__author__ = 'tanner'
from ..common_ops import get_labeled_rows

def parse_subject_table(soup):
    table = soup.find("table")
    return get_labeled_rows(table)

