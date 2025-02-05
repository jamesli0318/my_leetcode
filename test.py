import sys
import importlib.util
import os
import json
import inspect

def import_solution(problem_name):
    # Construct the path to the solution file
    solution_path = os.path.join(os.path.dirname(__file__), problem_name, 'solution.py')
    
    if not os.path.exists(solution_path):
        print(f"Error: Solution file not found at {solution_path}")
        sys.exit(1)
    
    # Import the module dynamically
    spec = importlib.util.spec_from_file_location(problem_name, solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get the Solution class
    solution_class = getattr(module, 'Solution', None)
    if solution_class is None:
        print(f"Error: No Solution class found in {solution_path}")
        sys.exit(1)
    
    return solution_class()

def parse_value(value_str, param_type):
    """Parse string value based on parameter type annotation"""
    try:
        # Handle List type hints (e.g., List[int])
        if str(param_type).startswith('typing.List'):
            return eval(value_str)  # Use eval for lists since they're in Python syntax
        # Handle basic types
        elif param_type == int:
            return int(value_str)
        elif param_type == float:
            return float(value_str)
        elif param_type == str:
            return value_str.strip('"')
        elif param_type == bool:
            return value_str.lower() == 'true'
        elif param_type == list:
            return eval(value_str)  # Use eval for Python list syntax
        elif param_type == dict:
            return eval(value_str)  # Use eval for Python dict syntax
        else:
            return eval(value_str)
    except Exception as e:
        print(f"Error parsing value {value_str} as {param_type}: {e}")
        return None

def run_test_case(solution, method_name, inputs):
    """Run a single test case with given inputs"""
    try:
        method = getattr(solution, method_name)
        sig = inspect.signature(method)
        params = list(sig.parameters.items())[1:]  # Skip self
        
        if len(inputs) != len(params):
            print(f"Error: Method {method_name} expects {len(params)} arguments but got {len(inputs)}")
            print(f"Method signature: {method_name}({', '.join(f'{name}: {param.annotation}' for name, param in params)})")
            return None
        
        # Parse inputs according to parameter types
        parsed_inputs = []
        for (param_name, param), input_value in zip(params, inputs):
            param_type = param.annotation
            if str(param_type).startswith('typing.List'):
                # For List type hints, we need to ensure we're passing a list
                try:
                    parsed_value = eval(input_value)
                    if not isinstance(parsed_value, list):
                        raise ValueError(f"Expected list but got {type(parsed_value)}")
                except Exception as e:
                    print(f"Error parsing list input {input_value}: {e}")
                    return None
            else:
                # For other types (like int), use the regular parse_value
                try:
                    parsed_value = int(input_value)
                except:
                    parsed_value = parse_value(input_value, param_type)
                
            if parsed_value is None:
                print(f"Error: Failed to parse input {input_value} for parameter {param_name}")
                return None
            parsed_inputs.append(parsed_value)
        
        # Run the method and get result
        result = method(*parsed_inputs)
        return result
    except Exception as e:
        print(f"Error running test case: {e}")
        return None

def compare_results(actual, expected):
    """Compare actual result with expected result, handling different types and orders"""
    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        # For lists that represent sets (like two_sum where order doesn't matter)
        if all(isinstance(x, (int, float)) for x in actual + expected):
            return sorted(actual) == sorted(expected)
        # For lists where order matters
        return actual == expected
    return actual == expected

def main():
    if len(sys.argv) != 2:
        print("Usage: python test.py <problem_name>")
        sys.exit(1)
    
    problem_name = sys.argv[1]
    solution = import_solution(problem_name)
    
    # Read test cases and answer files
    base_dir = os.path.dirname(__file__)
    test_case_file = os.path.join(base_dir, problem_name, 'test_cases.txt')
    ans_file = os.path.join(base_dir, problem_name, 'ans.txt')
    
    if not os.path.exists(test_case_file):
        print(f"Error: No test cases found at {test_case_file}")
        sys.exit(1)
    if not os.path.exists(ans_file):
        print(f"Error: No answer file found at {ans_file}")
        sys.exit(1)

    # Read expected answers
    expected_results = []
    with open(ans_file, 'r') as f:
        for line in f:
            if line.strip() and not line.strip().startswith('#'):
                expected_results.append(eval(line.strip()))

    print(f"Running test cases for {problem_name}:")
    passed_tests = 0
    total_tests = 0
    
    with open(test_case_file, 'r') as f:
        # Read all lines first
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        if not lines:
            print("Error: No test cases found")
            sys.exit(1)
            
        # First line should be the method name
        method_name = lines[0]
        if not hasattr(solution, method_name):
            print(f"Error: Solution class does not have method {method_name}")
            sys.exit(1)
        
        # Run test cases
        case_number = 0
        for line in lines[1:]:  # Skip the method name line
            try:
                nums_str, target_str = line.split(';')
                nums = eval(nums_str)
                target = int(target_str)
                
                # Run test case
                result = getattr(solution, method_name)(nums, target)
                
                print(f"\nTest Case {case_number + 1}:")
                print(f"Input: nums = {nums}, target = {target}")
                print(f"Your Output: {result}")
                print(f"Expected: {expected_results[case_number]}")
                
                # Compare results
                is_correct = sorted(result) == sorted(expected_results[case_number]) if result else result == expected_results[case_number]
                print(f"Status: {'✓ PASSED' if is_correct else '✗ FAILED'}")
                
                if is_correct:
                    passed_tests += 1
                total_tests += 1
                
            except Exception as e:
                print(f"\nError in test case {case_number + 1}: {e}")
            
            case_number += 1
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Passed: {passed_tests}/{total_tests} tests")
    if passed_tests == total_tests:
        print("Congratulations! All tests passed!")
    else:
        print(f"Keep going! {total_tests - passed_tests} tests still need work.")

if __name__ == '__main__':
    main()
