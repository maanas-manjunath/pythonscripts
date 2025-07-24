import sys
import json
import argparse

def main():
    """Main function that handles script execution and output formatting."""
    parser = argparse.ArgumentParser(description='Add two numbers')
    parser.add_argument('--echo', '-ec', required=True, help='first number')
    args = parser.parse_args()
    print(args.echo)

if __name__ == "__main__":
    main()
