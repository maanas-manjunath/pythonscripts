#!/usr/bin/env python3
"""
Cisco Device Command Simulator
Simulates responses from Cisco devices without actual SSH connection
Usage: python run_command.py -device_ip <ip> -command "<command>"
Example: python run_command.py -device_ip 1.1.1.1 -command "show version"
"""

import sys
import argparse
import random
from datetime import datetime, timedelta


def generate_random_version():
    """
    Generate a random Cisco IOS version
    
    Returns:
        str: Random version string (e.g., "17.3.4a", "16.12.5", "15.9.3")
    """
    major = random.randint(15, 17)
    minor = random.randint(1, 12)
    patch = random.randint(1, 9)
    
    # Randomly add a letter suffix (30% chance)
    suffix = random.choice(['', '', '', 'a', 'b', 'c'])
    
    return f"{major}.{minor}.{patch}{suffix}"


def generate_random_uptime():
    """
    Generate random uptime
    
    Returns:
        tuple: (weeks, days, hours, minutes)
    """
    weeks = random.randint(0, 52)
    days = random.randint(0, 6)
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    
    return weeks, days, hours, minutes


def generate_random_serial():
    """
    Generate random serial number
    
    Returns:
        str: Random serial number (e.g., "9FKLJWM5EB0")
    """
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for _ in range(11))


def generate_random_mac():
    """
    Generate random MAC address
    
    Returns:
        str: Random MAC address in Cisco format (e.g., "0050.56bf.1234")
    """
    mac = [random.randint(0x00, 0xff) for _ in range(6)]
    return "{:04x}.{:04x}.{:04x}".format(
        (mac[0] << 8) + mac[1],
        (mac[2] << 8) + mac[3],
        (mac[4] << 8) + mac[5]
    )


def generate_random_memory():
    """
    Generate random memory sizes
    
    Returns:
        tuple: (processor_memory, io_memory)
    """
    processor = random.choice([1024000, 2048000, 4096000, 8192000])
    io = random.choice([3075, 6147, 12291])
    
    return processor, io


def generate_show_version():
    """
    Generate show version output with random values
    
    Returns:
        str: Complete show version output
    """
    version = generate_random_version()
    weeks, days, hours, minutes = generate_random_uptime()
    serial = generate_random_serial()
    processor_mem, io_mem = generate_random_memory()
    
    # Random compilation date (within last 3 years)
    compile_date = datetime.now() - timedelta(days=random.randint(30, 1095))
    compile_str = compile_date.strftime("%a %d-%b-%y %H:%M")
    
    # Random memory values
    nvram = random.choice([32768, 65536, 131072, 262144])
    physical_mem = random.choice([3984776, 7969552, 15939104])
    virtual_disk = random.choice([6139904, 12279808, 24559616])
    
    # Random config register
    config_reg = random.choice(['0x2102', '0x2142', '0x2100'])
    
    # Format uptime string
    uptime_parts = []
    if weeks > 0:
        uptime_parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
    if days > 0:
        uptime_parts.append(f"{days} day{'s' if days != 1 else ''}")
    uptime_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    uptime_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    uptime_str = ", ".join(uptime_parts)
    
    output = f"""Cisco IOS XE Software, Version {version}
Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version {version}, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2021 by Cisco Systems, Inc.
Compiled {compile_str} by mcpre

Cisco IOS-XE software, Copyright (c) 2005-2021 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.

ROM: IOS-XE ROMMON
BOOTLDR: Virtual XE ROM

Router uptime is {uptime_str}
Uptime for this control processor is {uptime_str}
System returned to ROM by reload
System image file is "bootflash:packages.conf"
Last reload reason: reload

This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.

cisco CSR1000V (VXE) processor (revision VXE) with {processor_mem}K/{io_mem}K bytes of memory.
Processor board ID {serial}
Router operating mode: Autonomous
4 Gigabit Ethernet interfaces
{nvram}K bytes of non-volatile configuration memory.
{physical_mem}K bytes of physical memory.
{virtual_disk}K bytes of virtual hard disk at bootflash:.

Configuration register is {config_reg}"""
    
    return output


# Mock responses dictionary - functions generate dynamic content
MOCK_RESPONSES = {
    "show version": generate_show_version
}


def execute_mock_command(command):
    """
    Execute a mock command and return simulated response
    
    Args:
        command (str): Command to execute
    
    Returns:
        str: Mock command output or error message
    """
    # Check if command exists in mock responses
    if command in MOCK_RESPONSES:
        response_func = MOCK_RESPONSES[command]
        # If it's a function, call it to generate dynamic output
        if callable(response_func):
            return response_func()
        else:
            return response_func
    else:
        # Return Cisco-style error message
        return f"% Invalid input detected at '^' marker."


def main():
    """
    Main function to handle command-line arguments and execute mock commands
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Cisco Device Command Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_command.py -device_ip 1.1.1.1 -command "show version"
  python run_command.py -device_ip 192.168.1.1 -command "show version" -save
  python run_command.py -list
        """
    )
    
    parser.add_argument(
        '-device_ip',
        dest='device_ip',
        help='IP address of the device'
    )
    
    parser.add_argument(
        '-command',
        dest='command',
        default='show version',
        help='Command to execute (default: show version)'
    )
    
    parser.add_argument(
        '-save',
        dest='save',
        action='store_true',
        help='Save output to file'
    )
    
    parser.add_argument(
        '-list',
        dest='list',
        action='store_true',
        help='List all available commands'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If -list flag is used, show available commands and exit
    if args.list:
        print("Available commands:")
        for command in MOCK_RESPONSES.keys():
            print(f"  - {command}")
        sys.exit(0)
    
    # Validate required arguments
    if not args.device_ip:
        parser.error("-device_ip is required (unless using -list)")
    
    # Execute mock command
    output = execute_mock_command(args.command)
    
    # Display output (exactly as device would)
    print(output)
    
    # Save output if requested
    if args.save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{args.device_ip}_{args.command.replace(' ', '_')}_{timestamp}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(output)
            # Print to stderr so it doesn't mix with device output
            print(f"\nOutput saved to {filename}", file=sys.stderr)
        except Exception as e:
            print(f"\nERROR: Failed to save file: {str(e)}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n% Command interrupted", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"\n% Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
