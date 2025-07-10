#!/usr/bin/env python3
"""
Add to numbers
num1 = 10
num2 = 2
output : The sum is 12
"""
import sys
import json
import argparse

def main():
    """Main function that handles script execution and output formatting."""
    parser = argparse.ArgumentParser(description='Add two numbers')
    parser.add_argument('--num1', '-N1', required=True, help='first number')
    parser.add_argument('--num2', '-N2', required=True, help='second number')
    args = parser.parse_args()
    try:
        result = int(args.num1) + int(args.num1)
        output = {
            "success": True,
            "sum": result
        }
        print(json.dumps(output))
        sys.exit(0)
    except Exception as e:
        # Print error message to stderr
        print(f"Error: {str(e)}", file=sys.stderr)
        
        # Output JSON error for automation
        error_json = {
            "error": str(e),
            "success": False
        }
        print(json.dumps(error_json))
        
        # Exit with code 1 on exceptions
        sys.exit(1)


if __name__ == "__main__":
    main()
