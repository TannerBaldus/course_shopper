__author__ = 'tanner'
from bs4 import BeautifulSoup
import requests

def label_table_row_data(labels, table_row, text=True):
    """
    Creates a dict of labels mapped to text in table data tags contained in a table row tag.
    The order of the labels corresponds to the order of the table data tags. If text is False the mapping will
    map the tag to the label instead of the tag's text.
    Example:
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


    if len(labels) < len(row_data):
        row_data = row_data[0: len(labels)]
    if len(labels) > len(row_data):
        row_data = row_data + ['']*(len(labels)-len(row_data))


    label_mapping = dict(zip(labels, row_data))
    return label_mapping


def get_labels_from_header(rows, to_lower):
    """
    Given a list of rows gets the returns a list of the text found in th tags in the first row. Will convert
    the header text to lower case if the argument to_lower is true.
    Also returns a new list of rows without the row with the header data
    :param rows: list of beautiful soup tr tags
    :param to_lower: a boolean indicating if the header text should be lower case
    :return: a list of text contained in the th tags, list of rows without header row.
    """
    make_lower = lambda in_str: in_str.lower() if to_lower else in_str
    headers = rows[0].find_all('th')
    if not headers:
        raise ParserError('no header data found in first row.')
    labels = [make_lower(header.text.strip()) for header in headers]
    return labels, rows[1:]


def labeled_rows_from_list(lst, labels, text=True):
    """
    Acts like label_table_row_data except takes in a list of tr tags instead of a BeautifulSoup table tag, as this
    is sometimes better than looking trying to just use a whole table depending on the site structure.
    :param lst: a list of BeautifulSoup tr tags
    :param labels: list of labels in the order corresponding to td tag order
    :param text: boolean on wheter to use the tag itself or the tag text as values.
    :return: a dict of label, tag text or tag mappings
    """
    return (label_table_row_data(labels, row, text) for row in lst)

def labeled_rows_from_table(table, labels=[], text=True, to_lower=True):
    """
    Takes a BeautfiulSoup table tag and returns a list of dictonaries mapping the text from td tags to labels from each
    row. These labels can be provided as an argument, if no labels are given the function will try and get labels from
    th tags in the first row. When providing labels as an argument the order should correspond to the order of
    columns from left to right. Change to_lower to be false if when getting labels from the header when we want
    to maintain the capatilzation of the header text.

    :param table: a BeautifulSoup table tag
    :param labels: optional a list of labels to map td text to
    :param to_lower: a boolean indicating if the header text should be lower case default true
    :return: a list of dicts mapping the text from td tags to labels
    """
    if type(table) == list:
        raise ValueError('must be called on a BeautifulSoup obj. For lists of row objs use labeled_rows_from_list.')

    rows = table.find_all('tr')
    if len(rows) == 0:
        raise ParserError("There are no rows in this table: {}".format(rows))

    if not labels:
        labels, rows = get_labels_from_header(rows, to_lower)

    labeled_rows = (label_table_row_data(labels, row, text) for row in rows)
    return labeled_rows


def convert_and(in_str):
    """
    Converts the & to and in strings to keep things consistent.
    :param in_str:
    :return:
    """
    return in_str.replace('&', 'and')

def url_to_soup(url):
    """
    Turns a requests response into BeautifulSoup object
    :param url: url to a webpage
    :return: a beautiful soup object of the webpage
    """
    return BeautifulSoup(requests.get(url).text)


def flatten_dict_values(input_dict):

    """
    Flattens a nested dictonares into a list of it's values. Useful for making checking all of the values for some
    attribute, such as not being an empty string.
    :param arg:
    :return:
    """
    flat_list = []
    for value in input_dict.values():
        if type(value) == dict:
            flat_list.extend(flatten_dict_values(value))
        else:
            flat_list.append(value)
    return flat_list





