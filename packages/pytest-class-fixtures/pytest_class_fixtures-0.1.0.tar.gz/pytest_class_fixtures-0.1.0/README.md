# `pytest-class-fixtures` — Object-oriented fixtures for pytest

## Turn your class into a fixture

Ever have PyTest ´s `@fixture` tell you this?

```
ValueError: class fixtures not supported (maybe in the future)
```

well, the future is now:

```python
from pytest_class_fixtures import class_fixture

@class_fixture(name="calc")
class Calculator:
    def __init__(self):
        self.result = 0

def test_calculator_initial_state(calc):
    assert calc.result == 0
```

Do you want [BDD](https://pytest-bdd.readthedocs.io/) with that?

```gherkin
# calculator.feature
Feature: Calculator
    Scenario: Addition
        Given the calculator is cleared
        When I add 5
        Then the result should be 5

```

```python
import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from pytest_class_fixtures import class_fixture

scenarios("calculator.feature")

@class_fixture(name="calc")
class Calculator:
    def __init__ (self):
        self.clear()

    @given("the calculator is cleared")
    def clear (self):
        self.result = 0

    @when(parsers.parse("I add {number}"))
    def add (self, number):
        self.result += int(number)

@then(parsers.parse("the result should be {result}"))
def check_result(calc, result):
    assert calc.result == int(result)
```
