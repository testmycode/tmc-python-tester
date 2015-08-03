import unittest
from subprocess import Popen
import json
import os


class TestEverything(unittest.TestCase):

    def __init__(self, args):
        super(TestEverything, self).__init__(args)
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.command = ['python3', '-m', 'tmc']
        self.cwd = lambda folder: self.dir + '/resources/' + folder + '/test'
        self.results_path = lambda folder: self.cwd(folder) + '/.tmc_test_results.json'
        self.devnull = open(os.devnull, 'w')

    def test_project_with_no_points(self):
        sb = Popen(self.command, cwd=self.cwd('no_points'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.results_path('no_points')) as file:
            data = json.load(file)
        test = data[0]
        self.assertEqual(test['status'], 'passed')
        self.assertEqual(test['name'], 'test_points.TestEverything.test_new')
        self.assertEqual(test['points'], [])
        self.assertEqual(test['message'], '')
        self.assertEqual(test['backtrace'], [])

    def test_project_with_test_points(self):
        sb = Popen(self.command, cwd=self.cwd('test_points'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.results_path('test_points')) as file:
            data = json.load(file)
        test = data[0]
        self.assertEqual(test['status'], 'passed')
        self.assertEqual(test['passed'], True)
        self.assertEqual(test['name'], 'test_points.TestPoints.test_somepoints')
        self.assertEqual(test['points'], ['1.1'])
        self.assertEqual(test['message'], '')
        self.assertEqual(test['backtrace'], [])

    def test_project_with_class_points(self):
        sb = Popen(self.command, cwd=self.cwd('class_points'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.results_path('class_points')) as file:
            data = json.load(file)
        self.assertEqual(data[0]['points'], ['1.5'])
        self.assertEqual(data[1]['points'], ['1.5'])

    def test_failing_tests_fail(self):
        sb = Popen(self.command, cwd=self.cwd('failing'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.results_path('failing')) as file:
            data = json.load(file)
        self.assertEqual(data[0]['status'], 'failed')
        self.assertEqual(data[0]['passed'], False)

    def test_erroring_tests_error(self):
        sb = Popen(self.command, cwd=self.cwd('erroring'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.results_path('erroring')) as file:
            data = json.load(file)
        self.assertEqual(data[0]['status'], 'errored')
        self.assertEqual(data[0]['passed'], False)

    def test_multiple_files(self):
        sb = Popen(self.command, cwd=self.cwd('multiple_files'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.results_path('multiple_files')) as file:
            data = json.load(file)
        self.assertEqual(len(data), 2)

if __name__ == '__main__':
    unittest.main()
