__author__ = 'tanner'
import string

def label_table_row_data(labels, table_row, text=True):
    """
    Creates a dict of labels mapped to text in table data tags contained in a table row tag.
    The order of the labels corresponds to the order of the table data tags. If text is False the mapping will
    map the tag to the label instead of the tag's text. Example:
    labels = ['fname','middle','lname']
    <tr>
        <td>Grace</td>
        <td>Brewster</td>
        <td>Hopper</td>
    </tr>
    >> {fname: Grace, middle: Brewster, lname: Hopper}


    :param labels: list of labels in the order corresponding to td tag order
    :param table_row: beautiful soup object of a table row containing table data
    :param text: boolean on wheter to use the tag itself or the tag text as values.
    :return: a dict of label, tag text or tag mappings
    """

    row_data = table_row.find_all('td')

    if text:
        row_data = [td.text for td in row_data]

    assert len(row_data) != 0, "There is no table data in this row:\n {}".format(table_row)
    assert len(labels) == len(row_data), "Number td tags and labels must be equal\n labels\n{}\ntd tags\n{}".format(
        labels, row_data)
    label_mapping = dict(zip(labels, row_data))
    return label_mapping


def get_labeled_rows(labels, table):
    """
    :param labels:
    :param table:
    :return:
    """
    rows = table.find_all('tr')
    assert len(rows) != 0, "There are no rows in this table: {}".format(rows)
    labeled_rows = (label_table_row_data(labels, row) for row in rows)
    return labeled_rows


def convert_and(in_str):
    """
    Converts the & to and in strings to keep things consistent.
    :param in_str:
    :return:
    """
    return in_str.replace('&', 'and')