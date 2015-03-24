__author__ = 'tanner'
from logged_in_session import LoggedInSession
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
        main_menu_link = self.find_element_by_css_selector('[title="Course Evaluations"]')
        main_menu_link.click()
        primer_page_link = self.find_element_by_link_text('Course Evaluations')
        primer_page_link.click()
        self.close_opened_window()
        self.new_tab('https://www.applyweb.com/eval/new/coursesearch')

    def instructor_option_values(self):
        """
        Each of the elements in the instructor selection box has a integer value. We put those values in a list
        to be able to easily click those elements later.
        :return:
        """
        iframe = self.find_element_by_tag_name('iFrame')
        self.switch_to_frame(iframe)
        instructor_select = self.find_element_by_css_selector('[name="instructorSelect"]')
        option_soup = self.tag_to_soup(instructor_select)
        options = option_soup.find_all('option')
        return [option['value'] for option in options if option['value'] > 0]

    def get_instructor_option(self, value):
        selector = "[value='{}']".format(value)
        return self.find_element_by_css_selector(selector)


    def select_instructor(self, instructor_option):
        """

        :param instructor_value:
        :return:
        """
        instructor_option.click()

    def get_evals_table(self, instructor_value):
        """


        :return:
        """
        tbody_tags = self.find_elements_by_tag_name('tbody')
        if len(tbody_tags) != 3:
            return None
        tbody = self.tag_to_soup(tbody_tags[2])
        return tbody.find_all('tr', class_='even') + tbody.find_all('tr', class_='odd')

    def evals(self):
        self.go_to_course_evals()
        for value in self.instructor_option_values():

            instructor_option = self.get_instructor_option(value)
            instructor_name = instructor_option.text
            instructor_option.click()
            table = self.get_evals_table(value)

            if table:
                yield instructor_name, table







