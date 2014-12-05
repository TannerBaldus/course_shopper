__author__ = 'tanner'
import unittest
from bs4 import BeautifulSoup
from better_register.registration.parsers import uoregon_course as uo


class UO_Parse_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course_page = open('test_data/uoregon_class.html')
        cls.course_soup = BeautifulSoup(cls.course_page)
        cls.vitals_page = open('test_data/vitals.html')
        cls.title_text = u'CIS 210 Computer Science I >4'
        cls.credit_text = u'4.00 cr.'
        cls.vitals_soup = BeautifulSoup(cls.vitals_page).find('tr')
        cls.multiple_prof = BeautifulSoup(open('test_data/multiple_instructors.html'))
        cls.note_fees = BeautifulSoup(open('test_data/fee_notes.html'))

    def test_parse_instructor(self):
        correct_result = {
            'name': "Michal T. Young",
            'email': "michal@uoregon.edu"
        }
        result = uo.get_instructors(self.course_soup)
        self.assertEqual(correct_result, result[0])

    def test_multiple_instructor(self):
        correct_result = [{"email": "shannonh@uoregon.edu",
                          "name": "Shannon A. Hayes"},
                          {'name': "Judith R. Baskin",
                           'email': "jbaskin@uoregon.edu"},
                          {'name': 'Bonnie J. Mann', 'email': 'bmann@uoregon.edu'}]
        result = uo.get_instructors(self.multiple_prof)
        self.assertEqual(sorted(correct_result), sorted(result))

    def test_parse_vitals(self):
        correct_result = {
            'class_type': 'Lecture',
            'crn': 21497,
            'avail': 124,
            'max': 125,
            'start': 1100,
            'end': 1150,
            'day': 'mwf',
            'location': '240C MCK',
            'instructor': 'Young M',
            'notes': ''
        }
        result = uo.parse_vitals(self.vitals_soup)
        self.assertEqual(correct_result,result)

    def test_parse_time(self):
        parse_dict = {'time': '1000-1150'}
        correct_result = {
            'start': 1000,
            'end': 1150
        }
        uo.parse_time(parse_dict)
        self.assertEqual(correct_result, parse_dict)


    def test_parse_course_code(self):
        test_text = 'Prereq: programming experience and MATH 112.'
        result = uo.parse_course_code(test_text)
        correct_result = [('MATH', 112)]
        self.assertEqual(correct_result, result)



    def test_remove_nbsp(self):
        test_str = u'Hello\xa0 World'
        correct_result = u'Hello World'
        result = uo.remove_nbsp(test_str)
        self.assertEqual(correct_result, result)

    def test_get_term(self):
        result = uo.get_term(self.course_soup)
        correct_result = (u'Fall', 2014)
        self.assertEqual(correct_result, result)

    def test_get_title_credit_text(self):
        result = uo.get_title_credit_text(self.course_soup)
        self.assertEqual([self.title_text, self.credit_text], result)

    def test_get_credits(self):
        result = uo.get_credits(self.credit_text)
        self.assertEqual(4.00, result)

    def test_parse_title(self):
        result = uo.parse_title(self.title_text)
        correct_result = (u'CIS', 210, ['>4'], u'Computer Science I')
        self.assertEqual(correct_result, result)

    def test_get_course_fee(self):
        result = uo.get_course_fee(self.note_fees)
        self.assertEqual(84.00, result)

    def test_no_course_fee(self):
        result = uo.get_course_fee(self.course_soup)
        self.assertEqual(0.0, result)

    def test_get_prereq(self):
        correct_result = [(u'MATH', 112)]
        result = uo.get_prereqs(self.course_soup)
        self.assertEqual(correct_result, result)

    def test_no_prereq(self):
        result = uo.get_prereqs(self.multiple_prof)
        self.assertEqual([], result)



