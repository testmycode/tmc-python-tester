from unittest import TestProgram
from .runner import TMCTestRunner

main = TestProgram

main(testRunner=TMCTestRunner, module=None, failfast=False)
