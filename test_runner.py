#!/usr/bin/env python3
"""
Test runner script to execute all QStudio tests
"""

import subprocess
import sys
import os

# Add parent directory to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_test(test_file):
    """Run a single test file"""
    try:
        print(f"Running {test_file}...")
        result = subprocess.run([
            sys.executable, test_file
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(f"✓ {test_file} PASSED")
            return True
        else:
            print(f"✗ {test_file} FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"✗ Failed to run {test_file}: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running QStudio Test Suite")
    print("=" * 40)
    
    # Test files to run
    test_files = [
        "tests/test_data_management.py",
        "tests/test_data_download.py", 
        "tests/test_menu_interface.py",
        "tests/validate_implementation.py"
    ]
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if os.path.exists(test_file):
            if run_test(test_file):
                passed += 1
            else:
                failed += 1
        else:
            print(f"⚠ {test_file} not found")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests PASSED!")
        return 0
    else:
        print("❌ Some tests FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())