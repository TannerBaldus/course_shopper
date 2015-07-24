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



def match_middle_name(middle1,middle2):
    """
    To be used to match Instructor new indstructor data with Instructor names
    already in the databse.

    """

    if middle1 == middle2:
        return middle1, True

    equal = False

    if not middle2:
        equal = middle2 == middle1

    if len(middle2) != len(middle1):
        equal = False

        if len(middle2) == 1:
            equal = middle1.startswith(middle2)

        elif len(middle1) == 1:
            equal =middle2.startswith(middle1)

    else:
        equal = middle2 == middle1

    if equal:
        return middle1 if middle1 >= len(middle2) else middle2, True

    return '', False

def to_full(fname, middle, lname):
    if not middle:
        return "{} {}".format(fname, lname)
    return "{} {} {}".format(fname, middle, lname)


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



