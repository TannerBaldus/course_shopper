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
        iframe = self.find_element_by_tag_name('iFrame')
        self.switch_to_frame(iframe)

        instructor_select = self.find_element_by_css_selector('[name="instructorSelect"]')
        options = instructor_select.find_elements_by_tag_name('option')

        for option in options:
            yield option.get_attribute('value')


    def get_instructor_option(self, value):
        selector = "[value='{}']".format(value)
        return self.find_element_by_css_selector(selector)



    def get_evals_results(self):
        """

        :return:
        """

        for value in self.instructor_option_values():

            if int(value) > 0:
                instructor_option = self.get_instructor_option(value)
                evals = self.find_element_by_tag_name('tbody')
                yield instructor_option.text, evals.get_attribute('innerHTML')


    def evals(self):
        self.go_to_course_evals()
        return self.get_evals_results()







