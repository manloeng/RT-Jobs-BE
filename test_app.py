import os
os.environ["TEST"] = "please god just work"
TOPRINT = os.environ.get('TEST')

from app import app
import unittest
import json
testObject = open("testData.json", "r")
testDic = json.load(testObject)


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_all_jobs(self):
        result = self.app.get('/api/jobs/')
        expected = testDic["jobs"]
        actual = json.loads(result.get_data())
        assert expected == actual
    
    def test_single_job(self):
        result = self.app.get('/api/job/JwZDXcesJsniTKyLsGwh')
        expected = testDic["single-job"]
        actual = json.loads(result.get_data())
        assert expected == actual

    def test_single_job(self):
        result = self.app.get('/api/applications/?user_id=user101')
        expected = testDic["userapp"]
        actual = json.loads(result.get_data())
        assert expected == actual

    def test_single_job(self):
        result = self.app.get('/api/applications/?job_id=ONvUyou4hqYA4LzJ8OtB')
        expected = testDic["jobsapp"]
        actual = json.loads(result.get_data())
        assert expected == actual

    
    
        
    

   


