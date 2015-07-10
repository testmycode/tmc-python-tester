from unittest import TextTestRunner, TestLoader
from .result import TMCResult
from .points import getPoints
import json
import pdb


class TMCTestRunner(TextTestRunner):
    """A test runner for TMC exercises.
    """

    resultclass = TMCResult

    def __init__(self, *args, **kwargs):
        super(TMCTestRunner, self).__init__(*args, **kwargs)

    def run(self, test):
        print('Running tests with some TMC magic...')
        result = super(TMCTestRunner, self).run(test)
        return result

    # TODO: A lot of duplication from result
    def available_points(self):
        testLoader = TestLoader()
        tests = testLoader.discover('.', 'test*.py', None)
        result = {}
        for testa in tests._tests:
            for testb in testa._tests:
                for test in testb._tests:
                    module = test.__module__
                    classname = test.__class__.__name__
                    testName = test.__dict__['_testMethodName']
                    name = module + '.' + classname + '.' + testName
                    points = self._parsePoints(name)
                    result[name] = points
        print(json.dumps(result))

    # TODO: Add support for nested classes.
    def _parsePoints(self, name):
        testPoints = getPoints()['test']
        points = testPoints[name]
        li = name.split('.')
        li.pop()
        key = '.'.join(li)
        suitePoints = getPoints()['suite'][key]
        points += suitePoints
        return points
