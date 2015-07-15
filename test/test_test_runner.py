import unittest
import subprocess
import json
import pdb


class TestEverything(unittest.TestCase):

    def test_project_with_no_points(self):
        subprocess.Popen(['python3', '-m', 'tmc'], cwd='resources/no_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open('resources/no_points/test/tmc_test_results.json') as file:
            data = json.load(file)
        test = data[0]
        self.assertEqual(test['status'], 'passed')
        self.assertEqual(test['name'], 'test_points.TestEverything.test_new')
        self.assertEqual(test['points'], [])
        self.assertEqual(test['message'], '')
        self.assertEqual(test['backtrace'], [])

    def test_project_with_test_points(self):
        subprocess.Popen(['python3', '-m', 'tmc'], cwd='resources/test_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open('resources/test_points/test/tmc_test_results.json') as file:
            data = json.load(file)
        test = data[0]
        self.assertEqual(test['status'], 'passed')
        self.assertEqual(test['name'], 'test_points.TestPoints.test_somepoints')
        self.assertEqual(test['points'], ['1.1'])
        self.assertEqual(test['message'], '')
        self.assertEqual(test['backtrace'], [])

    def test_project_with_class_points(self):
        subprocess.Popen(['python3', '-m', 'tmc'], cwd='resources/class_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open('resources/class_points/test/tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(data[0]['points'], ['1.5'])
        self.assertEqual(data[1]['points'], ['1.5'])

    def test_failing_tests_fail(self):
        subprocess.Popen(['python3', '-m', 'tmc'], cwd='resources/failing/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open('resources/failing/test/tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(data[0]['status'], 'failed')

    def test_erroring_tests_error(self):
        subprocess.Popen(['python3', '-m', 'tmc'], cwd='resources/erroring/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        with open('resources/erroring/test/tmc_test_results.json') as file:
            data = json.load(file)
        self.assertEqual(data[0]['status'], 'errored')

if __name__ == '__main__':
    unittest.main()
