'''
Created on 3 Aug 2021

@author: qsong
'''
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import datetime
import json
import os
from pathlib import Path

class GameInfo(object):
    '''
    This module provides League related function
    '''
    game_base_url = "http://zq.win007.com/analysis/{}.htm"
    nowgoal_base_url = "https://www.nowgoal3.com/football/fixture/?date={}"
    daily_game_path_base = "../../data/daily_game/"
    date_str = ""
    daily_game_path = ""
    def __init__(self):
        '''
        Constructor
        '''
        self.date_str, self.daily_game_path = self.daily_game_pre()
        return

    def __del__(self):
        return

    def daily_game_pre(self):
        time_now = datetime.datetime.now()
        date_str = time_now.strftime('%Y-%m-%d')
        daily_game_path = os.path.join(self.daily_game_path_base,date_str)
        Path(daily_game_path).mkdir(parents=True, exist_ok=True)
        return date_str, daily_game_path

    def get_daily_game_table_file(self):
        driver = webdriver.Chrome()
        #driver = webdriver.Firefox()
        nowgoal_request_url = self.nowgoal_base_url.format(self.date_str)
        driver.get(nowgoal_request_url)
        mintable_content = driver.find_element_by_id('mintable').get_attribute('outerHTML')
        mintable_content_path = os.path.join(self.daily_game_path, "mintable_"+self.date_str+".html")
        print(mintable_content_path)
        mintable_content_file = open(mintable_content_path, 'w+')
        mintable_content_file.write(mintable_content.encode('ascii', 'ignore').decode('ascii'))
        mintable_content_file.close()
        driver.close()
        return mintable_content_path

    def get_daily_game_id_list_from_mintable(self,mintable_path):
        today_game_list = []
        soup = BeautifulSoup(open(mintable_path),'html.parser')
        tr_list = soup.find_all('tr')

        for tr_element in tr_list:
            id_value = tr_element.attrs['id']
            if "tr1_" in id_value:
                game_id = id_value.replace("tr1_","")
                today_game_list.append(game_id)
        return today_game_list

    def write_daily_game_info(self, game_list):
        daily_game_id_list_json_path = os.path.join(self.daily_game_path, "game_id_list.json")
        with open(daily_game_id_list_json_path, 'w+') as game_id_json_file:
            game_id_json_file.write(json.dumps(game_list))
        return

    def get_daily_game_id_list(self):
        mintable_html_path = self.get_daily_game_table_file()
        daily_game_id_list = self.get_daily_game_id_list_from_mintable(mintable_html_path)
        print("Today: {} games".format(len(daily_game_id_list)))
        self.write_daily_game_info(daily_game_id_list)

        # os.remove("../../data/game/day_table_info.html")
        return

'''
    def get_game_info_by_id (self, game_id):
        game_info_url = self.game_base_url.format(game_id)
        print game_info_url
        opener = urllib2.build_opener()
        headers = {  'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',}
        opener.addheaders = headers.items()
        url_data = opener.open(game_info_url,timeout=10).read()
        soup = BeautifulSoup(url_data)
        odd_table_body = soup.find_all("script")
        print odd_table_body    
        for script_in_body in odd_table_body:
            if script_in_body.text.find("function show_info") != -1 :
                print script_in_body
                game_file = open("../../data/game/game_info"+str(game_id)+".js", 'w+')
                game_file.write(script_in_body.text.encode('ascii', 'ignore').decode('ascii'))
                game_file.close()
        return
'''


class Test(unittest.TestCase):

    def setUp(self):
        self.test_obj = GameInfo()

    def tearDown(self):
        self.test_obj = None
        return

    def test_get_game_info(self):
        pass
#        self.test_obj.get_game_info_by_id(1365286)
        # self.test_obj.get_goldenbet()
        return

    def test_get_game_id_per_day(self):
        self.test_obj.get_daily_game_id_list()
        # self.test_obj.get_goldenbet()
        return

    def test_daily_game_pre(self):
        self.test_obj.daily_game_pre()
        return

    def test_get_daily_game_table_file(self):
        self.test_obj.get_daily_game_table_file()
        return

    def test_get_daily_game_id_list_from_mintable(self):
        self.test_obj.get_daily_game_id_list_from_mintable("../../data/daily_game/2021-08-19/mintable_2021-08-19.html")
        return

