import unittest
import subprocess
import json
import os


class TestEverything(unittest.TestCase):

    def __init__(self, args):
        super(TestEverything, self).__init__(args)
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def test_project_with_no_points(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc'], cwd=self.dir + '/resources/no_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/no_points/test/.tmc_test_results.json') as file:
            data = json.load(file)
        test = data[0]
        self.assertEqual(test['status'], 'passed')
        self.assertEqual(test['name'], 'test_points.TestEverything.test_new')
        self.assertEqual(test['points'], [])
        self.assertEqual(test['message'], '')
        self.assertEqual(test['backtrace'], [])

    def test_project_with_test_points(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc'], cwd=self.dir + '/resources/test_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/test_points/test/.tmc_test_results.json') as file:
            data = json.load(file)
        test = data[0]
        self.assertEqual(test['status'], 'passed')
        self.assertEqual(test['name'], 'test_points.TestPoints.test_somepoints')
        self.assertEqual(test['points'], ['1.1'])
        self.assertEqual(test['message'], '')
        self.assertEqual(test['backtrace'], [])

    def test_project_with_class_points(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc'], cwd=self.dir + '/resources/class_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/class_points/test/.tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(data[0]['points'], ['1.5'])
        self.assertEqual(data[1]['points'], ['1.5'])

    def test_failing_tests_fail(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc'], cwd=self.dir + '/resources/failing/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/failing/test/.tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(data[0]['status'], 'failed')

    def test_erroring_tests_error(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc'], cwd=self.dir + '/resources/erroring/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/erroring/test/.tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(data[0]['status'], 'errored')

    def test_multiple_files(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc'], cwd=self.dir + '/resources/multiple_files/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/multiple_files/test/.tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(len(data), 2)

if __name__ == '__main__':
    unittest.main()
