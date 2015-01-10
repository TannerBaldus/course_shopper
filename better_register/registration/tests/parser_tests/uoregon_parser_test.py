__author__ = 'tanner'
import unittest
from bs4 import BeautifulSoup
from better_register.registration.parsers import uoregon_course as uo


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
        offering has multiple instructors.
        """
        cls.peo_class = BeautifulSoup(open('test_data/peo.html'))

        diff_day_location = dict(room='241', building='KNI')
        cls.diff_days_meetings = [
            dict(weekday='f', calendar_day='1/09', start=1330, end=1720, location=diff_day_location),
            dict(weekday='s', calendar_day='1/10', start=900, end=1650, location=diff_day_location),
            dict(weekday='u', calendar_day='1/09', start=900, end=1650, location=diff_day_location)]

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
        correct_result = dict(avail=124, max=125, end_date=None, start_date=None, class_type="Lecture", meetings=
        [dict(weekday='m', start=1100, end=1150, location=location, calendar_day=None),
         dict(weekday='w', start=1100, end=1150, location=location, calendar_day=None),
         dict(weekday='f', start=1100, end=1150, location=location, calendar_day=None)], crn=21497)

        result = uo.parse_vitals(self.vitals_soup)
        self.assertItemsEqual(correct_result, result)

    def test_parse_time(self):
        parse_str = '1000-1150'
        correct_result = {
            'start': 1000,
            'end': 1150
        }
        result = uo.parse_time(parse_str)
        self.assertEqual(correct_result, result)


    def test_parse_course_code(self):
        test_text = 'Prereq: programming experience and MATH 112.'
        result = uo.parse_course_code(test_text)
        correct_result = [dict(code='MATH', number=112)]
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
        result = uo.get_credits(self.credit_text)
        self.assertEqual(4.00, result)

    def test_parse_title(self):
        result = uo.parse_title(self.title_text)
        correct_result = (dict(subject=u'CIS', number=210, title=u'Computer Science I'), ['>4'] )
        self.assertEqual(correct_result, result)

    def test_get_course_fee(self):
        result = uo.get_course_fee(self.note_fees)
        self.assertEqual(84.00, result)

    def test_no_course_fee(self):
        result = uo.get_course_fee(self.course_soup)
        self.assertEqual(0.0, result)

    def test_get_prereq(self):
        correct_result = [dict(code=u'MATH', number=112)]
        result = uo.get_prereqs(self.course_soup)
        self.assertEqual(correct_result, result)

    def test_get_prereq_and(self):
        correct_result = [dict(code='PEO', number=285), dict(code='PEO', number=351)]
        result = uo.get_prereqs(self.peo_class)
        self.assertEqual(correct_result, result)

    def test_no_prereq(self):
        result = uo.get_prereqs(self.diff_days)
        self.assertEqual([], result)

    def test_parse_location(self):
        location_str = '240C MCK'
        correct_result = dict(room='240C', building="MCK")
        self.assertEqual(correct_result, uo.parse_location(location_str))

    def test_parse_location_reverse(self):
        location_str = 'MCK 240C'
        correct_result = dict(room='240C', building="MCK")
        self.assertEqual(correct_result, uo.parse_location(location_str))

    def test_parse_start_end(self):
        self.assertEqual(dict(start_date='10/1', end_date='10/15'), uo.parse_start_end(self.two_date))

    def test_parse_start_end_no_dates(self):
        self.assertEqual(dict(start_date=None, end_date=None), uo.parse_start_end(self.no_date))

    def test_parse_start_end_one_date(self):
        self.assertEqual(dict(start_date=None, end_date=None), uo.parse_start_end(self.one_date))

    def test_parse_days(self):
        correct_result = [dict(weekday='m', calendar_day=None), dict(weekday='w', calendar_day=None)]
        self.assertItemsEqual(correct_result, uo.parse_days(self.no_date))

    def test_parse_days_date(self):
        self.assertItemsEqual([dict(weekday='t', calendar_day='10/1')], uo.parse_days(self.one_date))

    def test_parse_days_two_date(self):
        self.assertItemsEqual([dict(weekday='f', calendar_day=None)], uo.parse_days(self.two_date))

    def test_get_course_fee(self):
        result = uo.get_course_fee(self.peo_class)
        self.assertEqual(205.00, result)

    def test_get_web_resources(self):
        correct_result = [
            dict(link_text='IMPORTANT!  Enrollment and attendance policies',
                 link_url=u'http://opp.uoregon.edu/attendance_policies.pdf'),
            dict(link_text='Professional Courses Main Page',
                 link_url='http://opp.uoregon.edu/professional/procourses.html')
        ]
        result = uo.get_web_resources(self.peo_class)
        self.assertItemsEqual(correct_result,result)













