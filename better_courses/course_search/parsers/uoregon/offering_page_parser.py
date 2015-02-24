__author__ = 'tanner'

from ..common_ops import label_table_row_data
from datetime import datetime
import string
import re


def remove_nbsp(text):
    """
    removes the non breaking space characters from a string
    :param text:
    :return:
    """
    pattern = re.compile(u'\xa0')
    return pattern.sub('', text)


def to_int(in_string):
    """
    converts the in_string to an integer if it can. otherwise
    just returns the string
    :param in_string: the string to try and cast to int
    :return: the casted string or just the string
    """
    try:
        return int(in_string)
    except ValueError:
        return in_string

def is_float(in_str):
    """
    Checks if a str can be a float. Useful in the get_fee function
    :param in_str:
    :return:
    """
    try:
        float(in_str)
        return True
    except ValueError:
        return False
def is_tba(in_str):
    """

    :param in_str:
    :return:
    """
    in_str = in_str.lower()
    return 'tba' in in_str



def parse_time(time_str):
    """
    Replaces the time entry with a start and end time entry
    Splits start and end time, strip leading zero in military time and convert to int
    :param time_str: string of start and end times e.g. 1800-1850
    :return: None
    """
    if is_tba(time_str):
        return dict(start='tba', end='tba')
    start, end = [int(t.lstrip('0')) for t in time_str.split('-')]
    return dict(start=start, end=end)


def parse_days(day_str):
    """
    Sometimes offerings have one off meetings denoted by the form: m 10/1.
    Short classes are of the form: m 10/1-10/6
    If the day_str is neither of these forms the start_date and end_date will be None.

    :param day_str: a string of the days of a meeting. the text in the cell next to the time.
    :return: list of dicts of the form {weekday, }
    """

    if is_tba(day_str):
        return [dict(start_date=None,end_date=None, weekday='tba')]

    day_lst = day_str.split(' ')
    weekdays = day_lst[0]
    date_dict = dict(start_date=None, end_date=None)

    if len(day_lst) > 1:
        date_dict = parse_start_end(day_lst[1])


    return [dict(date_dict, weekday=c) for c in weekdays]


def parse_start_end(calendar_day_str):
    """
    Sometimes the course offering is a is a short class that doesn't go the full term.
    This is put in a string of the form: 10/1-10/15
    :param calendar_day_str: a string of the days of a meeting. the text in the cell next to the time.
    :return: a dict of the form {start_date,end_date}
    """
    assert calendar_day_str, 'Must be called on a non empty string '
    assert re.search(r'\d{1,2}\/\d{1,2}', calendar_day_str), 'Must be called on string containing dates'


    day_lst = calendar_day_str.split('-')
    if '-' in calendar_day_str:
        start, end = day_lst
    else:
        start, end = day_lst*2  #start and end is same day

    return dict(start_date=start, end_date=end)


def parse_location(location_str):
    """
    Takes a string of location and splits it up into Room/Number. Sometimes there's no room so will just put None into
    the room key in the return dict. We don't convert room number to .int because sometimes it's a combo of letters and
    numbers e.g. MCK 240C

    :param location_str:
    :return:
    """
    if is_tba(location_str):
        return dict(building='tba', room='tba')

    location_lst = location_str.split(' ')

    if len(location_lst) == 1:
        return dict(building=location_str, room=None)

    elif len(location_lst) == 2:
        pattern = re.compile('\d')
        is_room = lambda i: i if bool(pattern.search(location_lst[i])) else False  # Room Number order isn't consistent
        room_index = is_room(1) or 0
        return dict(building=location_lst[room_index - 1], room=location_lst[room_index])


def parse_meetings(days_str, time_str, location_str):
    """
    Since classes can have different meetings on different days we parse the time into day, time pairs.

    parse_meetings('mf',1600-1650, 'MCK 201')
    >[{'date_period : {weekday: m start:1600,end:1650 start_date:None,end_date:None}, location:{building:MCK, room:201}}
    >,{'date_period : {weekday: f start:1600,end:1650 start_date:None,end_date:None}, location:{building:MCK, room:201}]

    :param day_str: string of days e.g. mwf
    :param time_str: string fo start and end times
    :param location_str: string with the building and room number
    :return:a dict of days mapped to start and end times
    """


    times = parse_time(time_str)
    days = parse_days(days_str)


    for day in days:
        day.update(times)
    return [dict(date_period=day, location=parse_location(location_str)) for day in days]


def parse_vitals(table_row):
    """
    :param table_row
    A <TR> beautiful soup tag structured as
    <TR>
        <TD> class_type  i.e(Lecture)
        <TD> CRN
        <TD> Avail
        <TD> Max
        <TD> Time
        <TD> Day
        <TD> Location
        <TD> Instructor
        <TD> Note
    :return: A dictionary with the above titles as keys and the
    text from the <TD> as the values
    """
    labels = ['class_type', 'crn', 'avail', 'max', 'time', 'day', 'location', 'instructor', 'notes']
    label_mapping = label_table_row_data(labels, table_row)
    label_mapping.update(meetings=parse_meetings(label_mapping['day'], label_mapping['time'],
                                                            label_mapping['location']))

    map(label_mapping.pop, ['day', 'time', 'location', 'instructor', 'notes'])
    return label_mapping


def get_vitals(soup):
    """
    Finds the tag that contains the vitals for the class and returns the vitals parsed into a dict.
    :param soup: beautiful soup obj
    :return: dictonary generated by parse_vitals
    """
    vitals_tag = soup.find('td', class_='dddead', text='Location').parent.find_next_siblings('tr')[0]
    vitals_dict = parse_vitals(vitals_tag)
    return vitals_dict


def get_multiple_meetings(soup):
    """
    Sometimes a offering has meetings with diffrent times depending on the day. This is denoted by a table row of the
    form:
    <tr>
        <td rowspan="1" nowrap="" class="dddefault" width="75">0900-1650</td>
        <td rowspan="1" class="dddefault" width="90">u 1/11</td>
        <td rowspan="1" nowrap="" class="dddefault" width="75">241 KNI</td>
    </tr>
    :param soup: a beautifulsoup object
    :return: a list of meeting dictonaries.
    """

    is_meeting_tag = lambda tag: True if tag and tag.td and re.match(r'(\d{4}-\d{4})', tag.td.text) else False
    multiple_meeting_tags = soup.find_all(is_meeting_tag)
    get_args = lambda tr: [td.text for td in tr.find_all('td')]
    return [parse_meetings(*get_args(tr)) for tr in multiple_meeting_tags]


def get_term(soup):
    """
    Returns the term and year of the class
    :param soup: a beautiful soup obj
    returns the term and the year
    """
    term_tag = soup.find('h2')
    season, year = term_tag.text.split(' ')
    return dict(season=season, year=int(year))


def parse_course_code(text):
    """
    Finds the class codes of the form: CIS 210 in a sentence
    :param text: string to find class
    :return: list of tuples of class code and number

    parse_class_code('CIS 313 with Andrezj builds character.')
    > [('CIS',313)]
    parse_class_code('CIS 451 and HIST 101')
    > [('HIST',101), ('CIS',451)]
    """
    text = text.strip(string.punctuation).split(' ')
    make_course = lambda subj, number: dict(code=subj, number=int(number))
    current_subject = ''
    courses = []
    for i in text:
        if i.isupper():
            current_subject = i
        elif i.isdigit():
            courses.append(make_course(current_subject, i))
        else:
            continue

    return courses


def get_prereqs(soup):
    """
    Gets the prereq text of the course. Formatting is pretty inconsistent. So for now we will just save display the
    prereq text into the database and display it. Planning on a more advanced pre-req parser after initial iteration.
    Trying not to let perfect be the enemy of done.

    :rtype :
    :param soup: beautifulsoup obj of the course page
    :return: string of the text to display
    """
    prereq_text = None
    tag = soup.find('td', text=re.compile('Prereq:'))
    if tag:
        prereq_text = tag.text.split('Prereq:')[1].lstrip()
    return prereq_text


def parse_associated_sections(soup):
    """
    Gets the associated sections of a class.
    Found by searching for element:
    <TR>
        <TD COLSPAN="8" CLASS="dddead" width="536"><br>Associated Sections</TD>
    Then parsing the sibling rows which are the vitals for the associated section.

    :param soup: a beautifulsoup object of the class page
    :return: a list of dictionaries made from get_vitals()
    """
    associated_section_header = soup.find('td', text='Associated Sections').parent
    return [parse_vitals(sib) for sib in associated_section_header.find_next_siblings('tr')]


def parse_note(note_tag):
    """
    Parses the description and note code from a note tag.
    Sometimes the note code is actually an image, we get a string representation by getting the title of the image.
    :param note_tag:
    :return:
    """
    note_text =  note_tag.text
    note_delimiter = note_text.find('-')
    note_code = note_text[0:note_delimiter].strip()
    note_desc = note_text[note_delimiter+1:].strip()

    if not note_code:  # Note code is a image
        note_code = note_tag.img['title']
    return dict(code=note_code, desc=note_desc)

def get_notes(soup):
    """
    Luckily a lot of the notes for a class have the class 'notes'. So we find those divs and parse them here.
    :param soup:
    :return: a list of dicts
    """
    note_divs = soup.find_all('div', class_='notes')
    return map(parse_note, note_divs)



def get_course_description(soup):
    """
    Finds and returns the desctipion of the course.
    :param soup: beatifulsoup obj of course page
    :return: string of the course description
    """
    data_table = soup.find(class_='datadisplaytable')
    desc_row = data_table.find_all('tr')[1]
    return desc_row.td.text or ''


def parse_instructor(instructor_tag):
    """

    :param instructor_str:
    :return:
    """
    if not instructor_tag.a:
        instructor_tag = instructor_tag.text.strip()
        email = None

        if is_tba(instructor_tag):
            return dict(fname='tba',middle=None, lname='', email=None)

        else:   ##Sometimes a class is just taught by STAFF
            return dict(fname='STAFF', middle=None, lname='', email=None)
    else:
        full_name = instructor_tag.a['target'].replace('.', '').split(' ')
        email = instructor_tag.a['href'].replace('mailto:', '')

    if len(full_name) > 3:
        fname, lname = full_name[0], full_name[-1]
        middle = ' '.join(full_name[1:-1])

    elif len(full_name) == 3:
        fname, middle, lname = full_name

    else:
        fname, lname = full_name
        middle = None



    return dict(fname=fname, middle=middle, lname=lname, email=email)


def get_instructors(soup):
    """
    We use this instead of the vitals because the course evals
    need the full name. And the vitals only give us the lastname  first initial

    :param soup:
    :return:
    """
    instructor_elements = [tag.find_next('td') for tag in soup.find_all('td', text='Instructor:')]
    return map(parse_instructor, instructor_elements)


def parse_gen_eds(title_text):
    """
    The gen_ed codes of the form >4 are contained in the title text for some reason. So we extract those here.
    :param title_text: the title string
    :return: all the gen ed categories of the course, empty list if none

    parse_gen_eds('PHIL 110 Postmodernist Bullshitting >IP >2')
    >['>IP','>2']
    parse_gen_eds('BIS 400 Dude I have a great startup idea. I just need you to code it')
    > []
    """
    return [i for i in title_text.split(' ') if '>' in i]


def get_title_credit_text(soup):
    """
    The tags containg the credits and the title string are in the same TR so we get both strings here.
    :rtype : list
    :param soup: beautifulsoup obj
    :return: (title_text, credit_text)
    get_title_credit_text(course_soup)
    >['CIS 210 Computer Science I >4', '4.00 cr.']
    """
    return [remove_nbsp(tag.text) for tag in soup.find(class_="datadisplaytable").find('tr').find_all('td')]


def parse_credits(credit_text):
    """
    Returns the number of credits the course is worth.
    :param credit_text: the tag containing the credits
    :return:
    """
    credit_lst = credit_text.split(' ')[0].split('-')
    min_credits, max_credits = 2*[credit_lst[0]]

    if len(credit_lst) == 2:
        max_credits = credit_lst[1]

    return dict(min_credits=min_credits, max_credits=max_credits)


def parse_title(title_text):
    """
    The title, subject, number and gen eds are stored in the title. So we parse an return them here.
    :param title_text: the tag containing the title string
    :return: the course code
    """

    subject, number = parse_course_code(title_text)[0].values()
    end_of_number = title_text.find(str(number)) + 3
    gen_ed_start = title_text.find('>')  # If there's a > in the title its a gen ed
    gen_eds = parse_gen_eds(title_text)

    if gen_ed_start != -1:
        title = title_text[end_of_number:gen_ed_start]  # Title stops where gen ed begins
    else:
        title = title_text[end_of_number:]

    return dict(subject=subject, number=number, title=title.strip(), gen_eds=gen_eds)



def parse_course_fee(fee_text):
    """

    :param fee_text: text that contains the course fee
    :return:
    """
    fee_per_credit = False or 'per credit' in fee_text
    tag_text_lst = fee_text.lower().replace('$','').split(' ')
    fee = [is_float(i) for i in tag_text_lst][0]
    return dict(fee=fee, fee_per_credit=fee_per_credit)


def get_course_fee(soup):
    """
    Gets the course fee of a course returns 0.0 if there is no fee.
    :param soup: beautiful soup obj
    :return: a dict mapping the fee and fee_per_credit bool
    """
    tag = soup.find('td', text=re.compile('\$'))
    fee_per_credit = False
    fee = 0.0
    if tag:
        return parse_course_fee(tag.text)
    return dict(fee=0.0, fee_per_credit=False)


def get_web_resources(soup):
    """
    Some course offerings have important links about course policies. We parse them here into dicts of link_url
    and link_text.
    :param soup:a beautiful soup object
    :return: a list of dicts of the form dict(link_text='Lorem Ipsum', link_url='foobar.com')
    """
    web_resource_img = soup.find('img', title='Additional Web Resources Available')
    if web_resource_img:
        resource_anchors = web_resource_img.find_next('td').find_all('a')
        parse_anchor = lambda a: dict(link_text=a.text, link_url=a['href'])
        return map(parse_anchor, resource_anchors)
    return []


def get_parent_offering(soup):
    """

    :param soup:
    :return:
    """
    is_offering_tag = lambda t: t.text == 'Associated Sections' if t else False
    offering_tag = soup.find(is_offering_tag).parent
    offering_vitals = offering_tag.find_next('tr')
    return offering_vitals.get('crn')



def convert_meeting_to_datetime(meeting_dicts_list,year):
    """

    :param meeting_dicts_list:
    :return:
    """
    add_year = lambda date_str: '{}/{}'.format(date_str, year)

    make_date_obj = lambda date_str: datetime.strptime(add_year(date_str), '%m/%d/%Y').date()
    updated_list = []
    for meeting_dict in meeting_dicts_list:
        updated_dict = meeting_dict
        start_date, end_date = meeting_dict['date_period']['start_date'], meeting_dict['date_period']['end_date']

        if start_date:
            updated_dict['date_period']['start_date'] = make_date_obj(start_date)
            updated_dict['date_period']['end_date'] = make_date_obj(end_date)


        updated_list.append(updated_dict)

    return updated_list


def get_course(soup):
    """


    :param soup:
    :return:
    """
    title_text, credit_text = get_title_credit_text(soup)
    course = parse_title(title_text)
    credits = parse_credits(credit_text)
    course.update(credits, notes=get_notes(soup), fee=get_course_fee(soup), desc=get_course_description(soup))
    return course




def get_primary_offering(soup):
    """
    :param soup:
    :return:
    """

    primary_dict = get_vitals(soup)
    term = get_term(soup)
    meetings = convert_meeting_to_datetime(primary_dict.get('meetings') + get_multiple_meetings(soup), term.get('year'))
    course = get_course(soup)

    primary_dict.update(course=course, term=get_term(soup), instructors=get_instructors(soup),
                        meetings=meetings, web_resources=get_web_resources(soup)

    )
    return primary_dict


def parse_associated_section(soup):
    associated_section = get_vitals(soup)
    associated_section['meetings'] = associated_section['meetings'] + get_multiple_meetings(soup)
    associated_section['instructors'] = get_instructors(soup)
    associated_section['offering'] = get_parent_offering(soup)

    return associated_section


























