# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 13:20:35 2019

@author: pat_i
"""

import unittest
import app
import requests

class TestApp(unittest.TestCase):
    def setUp(self):
        return
    
    def tearDown(self):
        return
    
    def test_get_jukeboxes(self):
        #Test initial representation at API endpoint
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/"
        r = requests.get(test_url)
        stat_code = r.status_code
        num_results = len(r.json())
        expected_code = 200
        expected_num_results = 5
        self.assertEqual(stat_code, expected_code, "Got incorrect status code")     
        self.assertEqual(num_results, expected_num_results, "Got unexpected number of results")
        
        #Test settingId param that returns no results
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=4efdf86e-68a1-4256-a154-5069510d78fc"
        r = requests.get(test_url)
        stat_code = r.status_code
        expected_code = 404
        self.assertEqual(stat_code, expected_code, "Got incorrect status code")
        
        #Test settingId param with invalid id
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=somestring"
        r = requests.get(test_url)
        stat_code = r.status_code
        expected_code = 400
        self.assertEqual(stat_code, expected_code, "Got incorrect status code")
        
        #Test settingId param with results and default pagination
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=515ef38b-0529-418f-a93a-7f2347fc5805"
        r = requests.get(test_url)
        stat_code = r.status_code
        num_results = len(r.json())
        expected_code = 200
        expected_num_results = 5
        self.assertEqual(stat_code, expected_code, "Got incorrect status code")     
        self.assertEqual(num_results, expected_num_results, "Got unexpected number of results")
        
        #Test model that does not support setting
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=515ef38b-0529-418f-a93a-7f2347fc5805&model=fusion"
        r = requests.get(test_url)
        stat_code = r.status_code
        expected_code = 404
        self.assertEqual(stat_code, expected_code, "Got incorrect status code") 
        
        #Test invalid model param
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=515ef38b-0529-418f-a93a-7f2347fc5805&model=somestring"
        r = requests.get(test_url)
        stat_code = r.status_code
        expected_code = 404
        self.assertEqual(stat_code, expected_code, "Got incorrect status code")
        
         #Test model that does support setting
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=515ef38b-0529-418f-a93a-7f2347fc5805&model=angelina"
        r = requests.get(test_url)
        stat_code = r.status_code
        num_results = len(r.json())
        expected_code = 200
        expected_num_results = 2
        self.assertEqual(stat_code, expected_code, "Got incorrect status code") 
        self.assertEqual(num_results, expected_num_results, "Got unexpected number of results")
        
         #Test limit param
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=86506865-f971-496e-9b90-75994f251459&limit=6&model=angelina"
        r = requests.get(test_url)
        stat_code = r.status_code
        num_results = len(r.json())
        expected_code = 200
        expected_num_results = 6
        self.assertEqual(stat_code, expected_code, "Got incorrect status code") 
        self.assertEqual(num_results, expected_num_results, "Got unexpected number of results")
        
        #test offset param
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=86506865-f971-496e-9b90-75994f251459&limit=6&model=angelina&offset=1"
        r = requests.get(test_url)
        stat_code = r.status_code
        num_results = len(r.json())
        expected_code = 200
        expected_num_results = 4
        self.assertEqual(stat_code, expected_code, "Got incorrect status code") 
        self.assertEqual(num_results, expected_num_results, "Got unexpected number of results")
        
        #test invalid offset param
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=86506865-f971-496e-9b90-75994f251459&limit=6&model=angelina&offset=somestring"
        r = requests.get(test_url)
        stat_code = r.status_code
        expected_code = 400
        self.assertEqual(stat_code, expected_code, "Got incorrect status code") 
        
        #test invalid limit param
        test_url = "http://localhost:5000/testapi/v1/supported_jukeboxes/?settingId=86506865-f971-496e-9b90-75994f251459&limit=somestring"
        r = requests.get(test_url)
        stat_code = r.status_code
        expected_code = 400
        self.assertEqual(stat_code, expected_code, "Got incorrect status code") 
        
    def test_find_requirements(self):
        requirements = app.find_requirements("b43f247a-8478-4f24-8e28-792fcfe539f5")
        expected_requirements = set(["camera", "amplifier"])
        self.assertEqual(requirements, expected_requirements, "Got unexpected set of requirements")
        
   
    def test_get_page_of_list(self):
        test_list = [1,2,3,4,5]
        #Test first page 
        page_values = app.get_page_of_list(test_list, 2, 0)
        expected_page_values = [1,2]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        #Test second page 
        page_values = app.get_page_of_list(test_list, 2, 1)
        expected_page_values = [3,4]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
         #Test last page 
        page_values = app.get_page_of_list(test_list, 2, 2)
        expected_page_values = [5]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
         #Test out of range value returns last page
        page_values = app.get_page_of_list(test_list, 2, 100)
        expected_page_values = [5]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        #Test limit param
        page_values = app.get_page_of_list(test_list, 4, 0)
        expected_page_values = [1,2,3,4]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        #Test limit param greater than length
        page_values = app.get_page_of_list(test_list, 100, 0)
        expected_page_values = [1,2,3,4, 5]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        #Test negative limit
        page_values = app.get_page_of_list(test_list, -1, 0)
        expected_page_values = None
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        #Test negative offset
        page_values = app.get_page_of_list(test_list, 2, -1)
        expected_page_values = None
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        
        #Test list with string values
        test_list = ["str1", "str2", "str3"]
        page_values = app.get_page_of_list(test_list, 2, 0)
        expected_page_values =["str1", "str2"]
        self.assertEqual(page_values, expected_page_values, "Got unexpected page")
        
    def test_check_pagination_values(self):
        limit = 5
        offset = 3
        ret_limit, ret_offset = app.check_pagination_values(limit, offset)
        self.assertEqual(limit, ret_limit, "limit value changed")
        self.assertEqual(offset, ret_offset, "offset value changed")
        
        limit = "5"
        offset = "3"
        ret_limit, ret_offset = app.check_pagination_values(limit, offset)
        self.assertEqual(int(limit), ret_limit, "limit value changed")
        self.assertEqual(int(offset), ret_offset, "offset value changed")

if __name__ == '__main__':
    unittest.main()