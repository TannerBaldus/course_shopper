__author__ = 'tanner'

"""
Names being easy to difficult.
"""
def parse_name(full_name):
    """
    Takes a name and puts it into a dict of fname, middle, lname. If there are more than 3 words in the name, we take
    every word (delimited by spaces) between the middle and the last as the middle name.

    parse_name('Frank Underwood')
    >> {fname:Frank, middle:None, lname=Underwood}

    parse_name('Francis Joseph Underwood')
    >> {fname:Francis middle:Joseph lname: Underwood}

    parse_name('Hector Lombard Mendoza Perez')
    >> {fname:Hector, middle: Lombard Mendoza, lname: Perez}

    :param full_name: a string of a name
    :return: a dict of mapping fname, middle, lname to values
    """
    full_name = full_name.split(' ')

    if len(full_name) > 3:
        fname, lname = full_name[0], full_name[-1]
        middle = ' '.join(full_name[1:-1])

    elif len(full_name) == 3:
        fname, middle, lname = full_name

    else:
        fname, lname = full_name
        middle = ''

    return dict(fname=fname, middle=middle, lname=lname)


def match_middle_name(middle_name_1, middle_name_2):

    equal = False

    if middle_name_2 is None:
        equal = middle_name_2 == middle_name_1

    if len(middle_name_2) != middle_name_1:
        equal = False

        if len(middle_name_2) == 1:
            equal = middle_name_1.startswith(middle_name_2)

        elif middle_name_1 == 1:
            equal = middle_name_2.startswith(middle_name_1)

    else:
        equal = middle_name_2 == middle_name_1

    if equal:
        return middle_name_1 if middle_name_1 >= len(middle_name_2) else middle_name_2

    return False


def match_name(name1, name2):
    name1_dict = parse_name(name1)
    name2_dict = parse_name(name2)
    return name1_dict['fname'] == name2_dict['fname'] and name1_dict['lname'] == name2_dict['lname'] and\
           match_middle_name(name1_dict['middle'], name2_dict['middle'])

def reorder_comma_delimited_name(name):

    """
    Re orders a name of the form Last, First Middle to the form First Middle Last
    :param name:a comma delimited name ordered last, middle first
    :return: a space delimited name ordered first middle last
    """
    print(name)
    comma_index = name.find(',')
    return '{} {}'.format(name[comma_index+2:], name[0:comma_index])



