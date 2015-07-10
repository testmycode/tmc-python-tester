from unittest.runner import TextTestResult
from .points import getPoints
import atexit
import json
import traceback

results = []


class TMCResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super(TMCResult, self).__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        super(TMCResult, self).startTest(test)

    def addSuccess(self, test):
        super(TMCResult, self).addSuccess(test)
        self.addResult(test, 'passed')

    def addFailure(self, test, err):
        super(TMCResult, self).addFailure(test, err)
        self.addResult(test, 'failed', err)

    def addError(self, test, err):
        super(TMCResult, self).addError(test, err)
        self.addResult(test, 'errored', err)

    def addResult(self, test, status, err=None):
        module = test.__module__
        classname = test.__class__.__name__
        testName = test.__dict__['_testMethodName']
        name = module + '.' + classname + '.' + testName
        points = self._parsePoints(name)
        message = ""
        backtrace = []
        if err is not None:
            message = err[1].__str__()
            backtrace = traceback.format_tb(err[2])

        details = {
            'name': name,
            'status': status,
            'message': message,
            'points': points,
            'backtrace': backtrace
        }
        results.append(details)

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

    # TODO: Do not do this if not using TMCTestRunner
    @atexit.register
    def write_output():
        with open('tmc_test_results.json', 'w') as f:
            json.dump(results, f, ensure_ascii=False)
