from selenium import webdriver
from selenium.webdriver.common.keys import Keys
__author__ = 'tanner'

class LoggedInSession(webdriver.Firefox):


    def __init__(self, login_url, username, pwd):
        super(LoggedInSession, self).__init__()
        self.login_url = login_url
        self._login(username, pwd)


    def find_username_element(self):
        """

        :return:
        """
        pass


    def find_pwd_element(self):
        """

        :return:
        """
        pass
    def find_login_button(self):
        """

        :return:
        """
        pass

    def new_tab(self, url=''):
        """

        :param url:
        :return:
        """
        body = self.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 't')
        if url:
            self.get(url)

    def close_opened_window(self):
        """
        For when we want to immedatly close a new window. Swithces to the new window then
        :return:
        """
        assert self.window_handles > 1, "There's only one window open"
        original_window = self.current_window_handle
        latest_window = self.window_handles[-1]
        self.switch_to_window(latest_window)
        self.close()
        self.switch_to_window(original_window)


    def _login(self, username, pwd):
        """

        :param username:
        :param pwd:
        :return:
        """
        page = self.get(self.login_url)
        usr_input = self.find_username_element()
        usr_input.send_keys(username)
        pwd_input = self.find_pwd_element()
        pwd_input.send_keys(pwd)
        self.find_login_button().click()



if __name__ == '__main__':
    d = DuckwebSession('https://duckweb.uoregon.edu/pls/prod/twbkwbis.P_WWWLogin', '951196832', 't28561')











