# Grading Results for student1

## Summary

**Score:** 100.0 / 100 (100.0%)

## Function Implementation

**Implemented:** add, subtract, multiply, divide, factorial

**Missing:** None

## Doctest Results

**Functions with doctests:** add, multiply, factorial, divide, subtract

**Passed tests:** 5 / 5

## Detailed Test Results

### functions.add

**Status:** Passed

**Examples tested:** 2

**Failures:** 0

**Output:**

```
Trying:
    add(2, 3)
Expecting:
    5
ok
Trying:
    add(-1, 1)
Expecting:
    0
ok
```

### functions.divide

**Status:** Passed

**Examples tested:** 3

**Failures:** 0

**Output:**

```
Trying:
    divide(10, 2)
Expecting:
    5.0
ok
Trying:
    divide(7, 2)
Expecting:
    3.5
ok
Trying:
    divide(5, 0)
Expecting:
    Traceback (most recent call last):
        ...
    ZeroDivisionError: Cannot divide by zero
ok
```

### functions.factorial

**Status:** Passed

**Examples tested:** 3

**Failures:** 0

**Output:**

```
Trying:
    factorial(0)
Expecting:
    1
ok
Trying:
    factorial(5)
Expecting:
    120
ok
Trying:
    factorial(-1)
Expecting:
    Traceback (most recent call last):
        ...
    ValueError: Factorial is not defined for negative numbers
ok
```

### functions.multiply

**Status:** Passed

**Examples tested:** 2

**Failures:** 0

**Output:**

```
Trying:
    multiply(3, 4)
Expecting:
    12
ok
Trying:
    multiply(-2, 3)
Expecting:
    -6
ok
```

### functions.subtract

**Status:** Passed

**Examples tested:** 2

**Failures:** 0

**Output:**

```
Trying:
    subtract(5, 2)
Expecting:
    3
ok
Trying:
    subtract(2, 5)
Expecting:
    -3
ok
```

## Score Breakdown

* Implementation: 70.0 / 70
* Doctests: 20.0 / 20
* Error Handling: 10.0 / 10
* **Total:** 100.0 / 100
