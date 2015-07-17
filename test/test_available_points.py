import unittest
import subprocess
import json
import os


class TestAvailablePoints(unittest.TestCase):

    def __init__(self, args):
        super(TestAvailablePoints, self).__init__(args)
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def test_project_points(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc', 'available_points'], cwd=self.dir + '/resources/test_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/test_points/test/.available_points.json') as file:
            data = json.load(file)
        self.assertEqual(data['test_points.TestPoints.test_somepoints'], ['1.1'])

    def test_class_points(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc', 'available_points'], cwd=self.dir + '/resources/class_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/class_points/test/.available_points.json') as file:
            data = json.load(file)
        self.assertEqual(data['test_class_points.TestClassPoints.test_class_points'], ['1.5'])
        self.assertEqual(data['test_class_points.TestClassPoints.test_more_class_points'], ['1.5'])

    def test_project_with_no_points(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc', 'available_points'], cwd=self.dir + '/resources/no_points/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/no_points/test/.available_points.json') as file:
            data = json.load(file)
        self.assertEqual(data['test_points.TestEverything.test_new'], [])

    def test_multiple_files(self):
        sb = subprocess.Popen(['python3', '-m', 'tmc', 'available_points'], cwd=self.dir + '/resources/multiple_files/test', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        sb.wait()
        with open(self.dir + '/resources/multiple_files/test/.available_points.json') as file:
            data = json.load(file)
        self.assertEqual(len(data['test_one.TestOne.test_new']), 2)
        self.assertEqual(len(data['test_two.TestTwo.test_new']), 2)

if __name__ == '__main__':
    unittest.main()
