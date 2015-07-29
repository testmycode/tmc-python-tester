# tmc-python-tester

[![Build Status](https://travis-ci.org/rage/tmc-python3-utils.svg?branch=master)](https://travis-ci.org/rage/tmc-python3-utils)

A unittest-based test runner that [tmc-langs](https://github.com/rage/tmc-langs) uses to check exercises. Runs tests and ouputs the results in JSON format. Allows one to assign points to individual test cases or classes with `@points` decorators.

## Usage

This test runner accepts standard unittest test cases. One can optionally import and use the `@points` decorators from the library. A basic decorated test case looks like this:

```python
import unittest
from tmc import points


class TestSomething(unittest.TestCase):

    @points('1.1')
    def test_something(self):
        self.assertEqual('a', 'a')

if __name__ == '__main__':
    unittest.main()
```

See the [test resources](test/resources/) folder for more examples.

### Running the tests

To run the tests, execute:

```shell
$ python -m tmc
```

Now `.tmc_test_results.json` will contain the test results:

```json
[
    {
        "backtrace": [],
        "message": "",
        "name": "test_something.TestSomething.test_something",
        "points": [
            "1.1"
        ],
        "status": "passed"
    }
]
```

### Available points

One can check what points are available by running:

```shell
$ python -m tmc available_points
```

Then `.available_points.json` has all the points:

```json
{
    "test_something.TestSomething.test_something": [
        "1.1"
    ]
}
```
