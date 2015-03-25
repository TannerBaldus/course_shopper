__author__ = 'tanner'
import unittest
import datetime
from bs4 import BeautifulSoup
import course_search.parsers.uoregon.offering_page_parser as uo


class UO_Parse_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ## Course Pages
        cls.course_soup = BeautifulSoup(open('test_data/uoregon_class.html'))
        cls.vitals_soup = BeautifulSoup(open('test_data/vitals.html')).find('tr')
        cls.diff_days = BeautifulSoup(open('test_data/diff_days.html'))

        """
        PEO, or outdoor pursuits classes are awesome classes and edge case prone. They all have course fees,
        preqs structured like: PEO 285 and 315, and important web_related resources and notes. And this particular
        offering has multiple instructors
        """
        cls.peo_class = BeautifulSoup(open('test_data/peo.html'))
        cls.note_tag = BeautifulSoup('<div class="notes"><b>A</b> - Mandatory Attendance</div>')
        cls.note_img_tag = BeautifulSoup(open('test_data/note.html'))

        diff_day_location = dict(room='241', building='KNI')
        cls.diff_days_meetings = [
            dict(date_period=dict(weekday='f', start_date='1/09', end_date='1/09', start_time=1330, end_time=1720, ),
                 location=diff_day_location),
            dict(date_period=dict(day='s', start_date='1/10', end_date='1/10', start_time=900, end_time=1650),
                 location=diff_day_location),
            dict(date_period=dict(day='u', start_date='1/11', end_date='1/11', start_time=900, end_time=16500),
                 location=diff_day_location)]

        cls.title_text = u'CIS 210 Computer Science I >4'
        cls.credit_text = u'4.00 cr.'

        # # Day Str Cases
        cls.no_date = 'mw'
        cls.one_date = 't 10/1'
        cls.two_date = 'f 10/1-10/15'


    def test_parse_instructor(self):
        correct_result = dict(fname='Michal', middle='T', lname='Young', email="michal@uoregon.edu")
        result = uo.get_instructors(self.course_soup)
        self.assertEqual(correct_result, result[0])

    def test_multiple_instructor(self):
        correct_result = [dict(email="mstrong@uoregon.edu", fname='Michael', middle='C', lname='Strong'),
                          dict(email="dcrowe@uoregon.edu", fname='Daniel', middle='R', lname='Crowe')]
        result = uo.get_instructors(self.peo_class)
        self.assertItemsEqual(correct_result, result)

    def test_parse_vitals(self):
        location = dict(room="240C", building="MCK")
        correct_result = dict(open_seats=124, total_seats=125, meetings=
        [dict(weekday='m', start=1100, end=1150, location=location, end_date=None, start_date=None),
         dict(weekday='w', start=1100, end=1150, location=location, end_date=None, start_date=None),
         dict(weekday='f', start=1100, end=1150, location=location, end_date=None, start_date=None)], crn=21497)

        result = uo.parse_vitals(self.vitals_soup)
        self.assertItemsEqual(correct_result, result)

    def test_parse_time(self):
        parse_str = '1000-1150'
        correct_result = {
            'start_time': 1000,
            'end_time': 1150
        }
        result = uo.parse_time(parse_str)
        self.assertEqual(correct_result, result)

    def test_parse_course_code(self):
        test_text = 'Prereq: programming experience and MATH 112.'
        result = uo.parse_course_code(test_text)
        correct_result = [dict(subject__code='MATH', number='112')]
        self.assertEqual(correct_result, result)

    def test_remove_nbsp(self):
        test_str = u'Hello\xa0 World'
        correct_result = u'Hello World'
        result = uo.remove_nbsp(test_str)
        self.assertEqual(correct_result, result)

    def test_get_term(self):
        result = uo.get_term(self.course_soup)
        correct_result = dict(season=u'Fall', year=2014)
        self.assertEqual(correct_result, result)

    def test_get_title_credit_text(self):
        result = uo.get_title_credit_text(self.course_soup)
        self.assertEqual([self.title_text, self.credit_text], result)

    def test_get_credits(self):
        result = uo.parse_credits(self.credit_text)
        correct_result = dict(min_credits=4.0, max_credits=4.0)
        self.assertItemsEqual(correct_result, result)

    def test_parse_title(self):
        result = uo.parse_title_text(self.title_text)
        correct_result = dict(subject=u'CIS', number='210', title=u'Computer Science I', gen_eds=[dict(code='>4')])
        self.assertEqual(correct_result, result)

    def test_no_course_fee(self):
        result = uo.get_course_fee(self.course_soup)
        correct_result = dict(fee=0.0, fee_per_credit=False)
        self.assertEqual(correct_result, result)

    def test_get_prereq(self):
        correct_result = u'programming experience and MATH 112.'
        result = uo.get_prereqs(self.course_soup)
        self.assertEqual(correct_result, result)

    @unittest.skip('Skipping until re-implement parse_prereqs')
    def test_parse_prereq_and(self):
        correct_result = [dict(code='PEO', number='285'), dict(code='PEO', number='351')]
        result = uo.get_prereqs(self.peo_class)
        self.assertEqual(correct_result, result)

    def test_no_prereq(self):
        result = uo.get_prereqs(self.diff_days)
        self.assertEqual(None, result)

    def test_parse_location(self):
        location_str = '240C MCK'
        correct_result = dict(room='240C', building="MCK")
        self.assertEqual(correct_result, uo.parse_location(location_str))

    def test_parse_location_reverse(self):
        location_str = 'MCK 240C'
        correct_result = dict(room='240C', building="MCK")
        self.assertEqual(correct_result, uo.parse_location(location_str))

    def test_parse_start_end(self):
        self.assertEqual(dict(start_date='10/1', end_date='10/15'), uo.parse_start_end('10/1-10/15'))

    def test_parse_start_end_no_dates(self):
        with self.assertRaises(AssertionError):
            uo.parse_start_end(self.no_date)

    def test_parse_start_end_empty_string(self):
        with self.assertRaises(AssertionError):
            uo.parse_start_end("")

    def test_parse_start_end_one_date(self):
        self.assertEqual(dict(start_date='10/1', end_date='10/1'), uo.parse_start_end('10/1'))

    def test_parse_days(self):
        correct_result = [dict(day='m', start_date=None, end_date=None),
                          dict(day='w', start_date=None, end_date=None)]
        self.assertItemsEqual(correct_result, uo.parse_days(self.no_date))

    def test_parse_days_date(self):
        self.assertItemsEqual([dict(day='t', start_date='10/1', end_date='10/1')], uo.parse_days(self.one_date))

    def test_parse_days_two_date(self):
        self.assertItemsEqual([dict(day='f', start_date='10/1', end_date='10/15')], uo.parse_days(self.two_date))

    def test_get_course_fee(self):
        result = uo.get_course_fee(self.peo_class)
        print(result)
        correct_result = dict(fee=205.0, fee_per_credit=False)
        self.assertEqual(correct_result, result)

    def test_parse_meetings(self):
        day_str = 'mw'
        time_str = '1600-1650'
        location_str = 'MCK 201'

        correct_result = [
            {'date_period': {'start_time': 1600, 'end_time': 1650, 'start_date': None, 'end_date': None, 'day': 'm'},
             'location': {'building': 'MCK', 'room': '201'}},

            {'date_period': {'start_time': 1600, 'end_time': 1650, 'start_date': None, 'end_date': None, 'day': 'w'},
             'location': {'building': 'MCK', 'room': '201'}}]

        result = uo.parse_meetings(time_str, day_str, location_str)
        self.assertItemsEqual(correct_result, result)

    def test_get_web_resources(self):
        correct_result = [
            dict(link_text='IMPORTANT!  Enrollment and attendance policies',
                 link_url=u'http://opp.uoregon.edu/attendance_policies.pdf'),
            dict(link_text='Professional Courses Main Page',
                 link_url='http://opp.uoregon.edu/professional/procourses.html')
        ]
        result = uo.get_web_resources(self.peo_class)
        self.assertItemsEqual(correct_result, result)

    def test_parse_notes(self):
        correct_result = dict(code='A', desc='Mandatory Attendance')
        result = uo.parse_note(self.note_tag)
        self.assertEqual(correct_result, result)

    def test_parse_notes_img(self):
        correct_result = dict(
            code='Approval Required',
            desc=("Dept or Instructor approval required; check course details for effective dates.",
                  "When approved, use the Add/Drop menu to add the course by entering the CRN directly")
        )
        result = uo.parse_note(self.note_img_tag)


    def test_get_notes(self):
        correct_result = [
            dict(code='b', desc='Course articles and information available on course website'),
            dict(code='A', desc='Mandatory Attendance'),
            dict(code='j', desc='Must be able to run 2 miles in 20 mins during in-class fitness test'),
            dict(
                code='Approval Required',
                desc="Dept or Instructor approval required; check course details for effective dates." +
                     "  When approved, use the Add/Drop menu to add the course by entering the CRN directly"
            )
        ]

        result = uo.get_notes(self.peo_class)
        self.assertItemsEqual(correct_result, result)

    def test_get_course_description(self):
        correct_result = ('Basic concepts and practices of computer science. Topics include algorithmic problem solving'
                          ', levels of abstraction, object-oriented design and programming, software organization, '
                          'analysis of algorithm and data structures. Sequence.')

        result = uo.get_course_description(self.course_soup)
        self.assertEqual(correct_result, result)

    def test_convert_meeting_to_date(self):
        test_meetings = [
            {
            'date_period': {'start_time': 1600, 'end_time': 1650, 'start_date': '10/1', 'end_date': '10/6', 'day': 'm'},
            'location': {'building': 'MCK', 'room': '201'}},
            {
            'date_period': {'start_time': 1600, 'end_time': 1650, 'start_date': '10/1', 'end_date': '10/6', 'day': 'w'},
            'location': {'building': 'MCK', 'room': '201'}}]
        year = 2015
        start_date = datetime.datetime(year, 10, 1).date()
        end_date = datetime.datetime(year, 10, 6).date()

        correct_ouput = [
            {'date_period': {'start_time': 1600, 'end_time': 1650, 'start_date': start_date, 'end_date': end_date,
                             'day': 'm'},
             'location': {'building': 'MCK', 'room': '201'}},
            {'date_period': {'start_time': 1600, 'end_time': 1650, 'start_date': start_date, 'end_date': end_date,
                             'day': 'w'},
             'location': {'building': 'MCK', 'room': '201'}}]

        self.assertEqual(correct_ouput, uo.convert_meeting_to_datetime(test_meetings, year))


    def test_get_course(self):
        correct_result = {'min_credits': 4.0,
                          'max_credits': 4.0,
                          'desc': u'Basic concepts and practices of computer science. Topics include algorithmic problem solving, '
                                  u'levels of abstraction, object-oriented design and programming, software organization, analysis of '
                                  u'algorithm and data structures. Sequence.',
                          'fee': 0.0,
                          'fee_per_credit': False,
                          'gen_eds': [u'>4'],
                          'notes': [{'code': u'A', 'desc': u'Mandatory Attendance'}],
                          'number': '210',
                          'subject': u'CIS',
                          'title': u'Computer Science I'}
        self.assertItemsEqual(correct_result, uo.get_course(self.course_soup))

    def test_credit_range(self):
        test_text = '1.00-12.00'
        correct_result = dict(min_credits=1.0, max_credits=12.0)
        self.assertItemsEqual(correct_result, uo.parse_credits(test_text))

    def test_parse_course_title(self):
        correct_result = 'Computer Science I'
        self.assertEqual(correct_result, uo.parse_course_title(self.title_text, '210', 27))

    def test_parse_course_title_no_gen_eds(self):
        test_title = 'CIS 210 Computer Science I'
        correct_result = 'Computer Science I'
        self.assertEqual(correct_result, uo.parse_course_title(test_title, '210', -1))

    def test_multiple_meetings(self):
        result = uo.get_multiple_meetings(self.diff_days)
        correct_result = [{'date_period': {'day': u's',
                                           'end_date': u'1/10',
                                           'end_time': 1650,
                                           'start_date': u'1/10',
                                           'start_time': 900},
                           'location': {'building': u'KNI', 'room': u'241'}},
                          {'date_period': {'day': u'u',
                                           'end_date': u'1/11',
                                           'end_time': 1650,
                                           'start_date': u'1/11',
                                           'start_time': 900},
                           'location': {'building': u'KNI', 'room': u'241'}}]

        return self.assertItemsEqual(correct_result, result)




