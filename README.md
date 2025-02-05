# LeetCode Testing Framework

A simple and flexible testing framework for LeetCode solutions in Python.

## Structure

```
leetcode/
├── test.py              # Main testing framework
├── README.md           # This file
└── problem_name/       # Directory for each LeetCode problem
    ├── solution.py     # Your solution class
    ├── test_cases.txt  # Test cases
    └── ans.txt         # Expected answers
```

## How to Use

1. Create a new directory for your LeetCode problem:
   ```bash
   mkdir problem_name
   ```

2. Create a `solution.py` file in the problem directory with your solution class:
   ```python
   from typing import List
   
   class Solution:
       def methodName(self, param1: Type1, param2: Type2) -> ReturnType:
           # Your solution here
           pass
   ```

3. Create a `test_cases.txt` file with your test cases:
   ```
   # First line: method name
   # Following lines: test inputs separated by semicolons
   methodName
   input1;input2
   input3;input4
   ```

4. Create an `ans.txt` file with expected outputs:
   ```
   # One answer per line, matching test cases order
   [expected_output1]
   [expected_output2]
   ```

5. Run the tests:
   ```bash
   python3 test.py problem_name
   ```

## Example: Two Sum

Here's how to set up tests for the Two Sum problem:

1. `two_sum/solution.py`:
   ```python
   from typing import List
   
   class Solution:
       def twoSum(self, nums: List[int], target: int) -> List[int]:
           d = {}
           for i, num in enumerate(nums):
               if target - num in d:
                   return [d[target - num], i]
               d[num] = i
   ```

2. `two_sum/test_cases.txt`:
   ```
   twoSum
   [2,7,11,15];9
   [3,2,4];6
   [3,3];6
   ```

3. `two_sum/ans.txt`:
   ```
   [0,1]
   [1,2]
   [0,1]
   ```

4. Run the tests:
   ```bash
   python3 test.py two_sum
   ```

## Features

- Dynamic method importing
- Support for various input types (lists, integers, strings, etc.)
- Clear test case output and summary
- Support for multiple test cases per problem
- Order-independent list comparison for problems like Two Sum
- Helpful error messages for debugging

## Requirements

- Python 3.6+
- No external dependencies required

## Tips

1. Make sure your test cases cover:
   - Normal cases
   - Edge cases
   - Empty/null inputs
   - Large inputs
   - Invalid inputs (if applicable)

2. For list outputs where order doesn't matter (like Two Sum), the framework will automatically sort the lists before comparison.

3. Comments in test_cases.txt and ans.txt files are supported (lines starting with #).
