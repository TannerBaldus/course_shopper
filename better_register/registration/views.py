from django.shortcuts import render
import requests
from bs4 import  BeautifulSoup
import parsers.uoregon_results as uor
# Create your views here.

def class_search(term, subject):
    search_url = 'http://classes.uoregon.edu/pls/prod/hwskdhnt.P_ListCrse?term_in={term}&' \
                 'sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy' \
                 '&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_cred=dummy&sel_tuition=dummy&sel_' \
                 'open=dumm&sel_weekend=dummy&sel_title=&sel_to_cred=&sel_from_cred=&sel_subj={subject}&sel_crse=&sel_crn=&' \
                 'sel_camp=%25&sel_levl=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a' \
                 '&submit_btn=Show+Classes'
    detail_url = ''
    parse_result_fn = lambda x: uor.parse_course_result()
    results_soup = BeautifulSoup(requests.get(search_url).text)
    for i in parse_results(results_soup):
          print i


class_search('201401','CIS')