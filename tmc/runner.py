from unittest import TextTestRunner
from .result import TMCResult


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
