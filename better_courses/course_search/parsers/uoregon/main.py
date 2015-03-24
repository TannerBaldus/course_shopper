__author__ = 'tanner'
from search_page_parser import parse_results
from course_search.models import Subject
from subject_codes import parse_subject_dropdown
from evals_parser import parse_eval
from ..common_ops import url_to_soup
from course_search.logged_in_sessions.duckweb_session import DuckwebSession




course_search_url = ('http://classes.uoregon.edu/pls/prod/hwskdhnt.P_ListCrse?term_in={}&sel_subj=dummy&sel_day=dummy&'
                  'sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&'
                  'sel_ptrm=dummy&sel_attr=dummy&sel_cred=dummy&sel_tuition=dummy&sel_open=dummy&sel_weekend=dummy'
                  '&sel_title=&sel_to_cred=&sel_from_cred=&sel_subj={}&sel_crse=&sel_crn=&sel_camp=%25&sel_levl=%25'
                  '&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a&submit_btn=Show+Classes')

offering_page_base = 'http://classes.uoregon.edu/pls/prod/hwskdhnt.p_viewdetl?term={}'
offering_page_suffix = '&crn={}'


subject_code_page = 'http://classes.uoregon.edu/pls/prod/hwskdhnt.p_search?term=201402'


def convert_to_term_number(season, year):
    """
    In the uoregon search url the search term is the year and the term number.
    Here are some examples:

    Fall 2014         201401
    Winter 2015       201402
    Spring 2015       201403
    Summer 2015       201404
    Fall   2015       201501

    :param season:
    :param year:
    :return:
    """
    season = season.lower()
    seasons = ['not_valid', 'fall', 'winter', 'spring', 'summer']
    season_index = seasons.index(season)
    assert 1 < season_index < 4, 'season must be fall, winter, spring or summer'

    if season != 'fall':         ## All terms except fall use the previous year in its code
        year -= 1

    season_code = '0{}'.format(season_index)
    return str(year)+season_code



def get_subjects():
    """

    :return:
    """

    soup = url_to_soup(subject_code_page)
    return parse_subject_dropdown(soup)



def get_offerings(season, year, subject_codes):
    """

    :param season:
    :param year:
    :return:
    """
    term = convert_to_term_number(season, year)
    term_search_url = lambda term, code: course_search_url.format(term, code)
    offering_page_url = offering_page_base.format(term)+offering_page_suffix

    for code in subject_codes:
        print code
        search_url = term_search_url(term,code)
        for result in parse_results(term_search_url(term, code), offering_page_url):
            print result
            yield result


def update_evals(username, password):
    d = DuckwebSession(username, password)

    for instructor_name, eval_rows in d.evals():
        for result in parse_eval(instructor_name, eval_rows):
            yield result







