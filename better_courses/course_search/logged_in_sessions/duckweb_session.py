__author__ = 'tanner'
from logged_in_session import LoggedInSession
from  ..common_ops.name_ops import parse_name, reorder_comma_delimited_name
from bs4 import  BeautifulSoup

class DuckwebSession(LoggedInSession):

    def __init__(self, username, pwd):
        duckweb_url = 'https://duckweb.uoregon.edu/pls/prod/twbkwbis.P_WWWLogin'
        super(DuckwebSession, self).__init__(duckweb_url, username, pwd)



    def find_username_element(self):
        """

        :return:
        """
        return self.find_element_by_id('UserID')

    def find_pwd_element(self):
        """

        :return:
        """
        return self.find_element_by_xpath('//*[@id="PIN"]/input')

    def find_login_button(self):
        """

        :return:
        """
        return self.find_element_by_css_selector("[value='Login']")

    def go_to_course_evals(self):
        """
        Navigates to the course evaluations page. Opens up a new window and closes it
        because this allows us to open go directly to the url of the evaluation search, thus saving without
        :return:
        """
        print("going to course evals")
        main_menu_link = self.find_element_by_css_selector('[title="Course Evaluations"]')
        main_menu_link.click()
        primer_page_link = self.find_element_by_link_text('Course Evaluations')
        primer_page_link.click()
        self.close_opened_window()
        self.new_tab('https://www.applyweb.com/eval/new/coursesearch')
        iframe = self.find_element_by_tag_name('iFrame')
        self.switch_to_frame(iframe)

    def instructor_option_values(self, start_lname, end_lname):
        """
        Each of the elements in the instructor selection box has a integer value. We put those values in a list
        to be able to easily click those elements later.
        :return:
        """
        instructor_select = self.find_element_by_css_selector('[name="instructorSelect"]')
        option_soup = self.tag_to_soup(instructor_select)
        options = option_soup.find_all('option')
        get_lname = lambda text: parse_name(reorder_comma_delimited_name(text))['lname']
        valid_option= lambda option: int(option['value']) > 0 and start_lname <= get_lname(option.text) >= end_lname
        return [option['value'] for option in options if valid_option(option)]

    def get_instructor_option(self, value):
        selector = "[value='{}']".format(value)
        return self.find_element_by_css_selector(selector)


    def select_instructor(self, instructor_option):
        """

        :param instructor_value:
        :return:
        """
        instructor_option.click()


    def evals(self, start_lname='', end_lname=None):
        self.go_to_course_evals()
        v = self.instructor_option_values(start_lname, end_lname)
        print(v)
        for value in v :
            print 'ins value {}'.format(value)
            instructor_option = self.get_instructor_option(value)
            instructor_name = instructor_option.text
            instructor_option.click()
            yield instructor_name, self.page_to_soup()







