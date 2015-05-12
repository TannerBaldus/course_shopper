__author__ = 'tanner'
from ...common_ops.parser_ops import labeled_rows_from_table, convert_and

def parse_subject_table(soup):
    table = soup.find("table")
    return labeled_rows_from_table(table)


def parse_subject_dropdown(soup):
    selection = soup.find(id='subj_id')
    options = selection.find_all('option')[1:]
    for option in options:
        code, subject = option.text.strip().split(' - ')
        yield dict(code=code.replace(' ', ''), subject=convert_and(subject).strip())



