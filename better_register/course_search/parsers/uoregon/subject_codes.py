__author__ = 'tanner'
from ..common_ops import get_labeled_rows

def parse_subject_table(soup):
    table = soup.find(id="DataTables_Table_0")
    labels = ['code', 'subject']
    return get_labeled_rows(labels, table)

