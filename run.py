import subprocess
import os
import time
import sys

def run_tests(test_case_name):
    # Ensure the results directory exists
    os.makedirs('results', exist_ok=True)
    
    # Generate a unique filename based on the test case name and timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_filename = f"results/{test_case_name}_report_{timestamp}.html"
    
    # Run pytest and generate the report
    result = subprocess.run([
        'pytest',
        f'--html={report_filename}',
        '--self-contained-html',
        f'ota_framework/test_cases/{test_case_name}.py'
    ], check=True)
    
    if result.returncode != 0:
        raise Exception("Tests failed")
    
    print(f"Report saved to {report_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script_name.py <test_case_name>")
        sys.exit(1)
    
    test_case_name = sys.argv[1]
    run_tests(test_case_name)
