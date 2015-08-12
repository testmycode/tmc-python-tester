import unittest
from subprocess import Popen
import json
import os


class TestAvailablePoints(unittest.TestCase):

    def __init__(self, args):
        super(TestAvailablePoints, self).__init__(args)
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.command = ['python3', '-m', 'tmc', 'available_points']
        self.cwd = lambda folder: self.dir + '/resources/' + folder
        self.points_path = lambda folder: self.cwd(folder) + '/.available_points.json'
        self.devnull = open(os.devnull, 'w')

    def test_project_points(self):
        sb = Popen(self.command, cwd=self.cwd('test_points'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.points_path('test_points')) as file:
            data = json.load(file)
        self.assertEqual(data['test.test_points.TestPoints.test_somepoints'], ['1.1'])

    def test_class_points(self):
        sb = Popen(self.command, cwd=self.cwd('class_points'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.points_path('class_points')) as file:
            data = json.load(file)
        self.assertEqual(data['test.test_class_points.TestClassPoints.test_class_points'], ['1.5'])
        self.assertEqual(data['test.test_class_points.TestClassPoints.test_more_class_points'], ['1.5'])

    def test_project_with_no_points(self):
        sb = Popen(self.command, cwd=self.cwd('no_points'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.points_path('no_points')) as file:
            data = json.load(file)
        self.assertEqual(data['test.test_points.TestEverything.test_new'], [])

    def test_multiple_files(self):
        sb = Popen(self.command, cwd=self.cwd('multiple_files'), stdout=self.devnull, stderr=self.devnull)
        sb.wait()
        with open(self.points_path('multiple_files')) as file:
            data = json.load(file)
        self.assertEqual(len(data['test.test_one.TestOne.test_new']), 2)
        self.assertEqual(len(data['test.test_two.TestTwo.test_new']), 2)

if __name__ == '__main__':
    unittest.main()
