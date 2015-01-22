__author__ = 'tanner'
from logged_in_session import LoggedInSession
class DuckwebSession(LoggedInSession):
    def __init__(self, login_url, username, pwd):
        super(DuckwebSession, self).__init__(login_url, username, pwd)


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
        main_menu_link = self.find_element_by_css_selector('[title="Course Evaluations"]')
        main_menu_link.click()
        primer_page_link = self.find_element_by_class_name('Course Evaluations')
        primer_page_link.click()
        self.close_opened_window()
        self.new_tab('https://www.applyweb.com/eval/new/coursesearch')


