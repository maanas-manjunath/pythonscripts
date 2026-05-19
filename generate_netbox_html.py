#!/usr/bin/env python3
"""
Generates HTML table from NetBox device data
Extracts: name, id, site, manufacturer, model, device_role, primary_ip
"""

import json
import sys
from datetime import datetime

def generate_html_table(netbox_response):
    """Generate HTML table from NetBox API response"""
    
    devices = netbox_response.get('results', [])
    total_count = netbox_response.get('count', len(devices))
    
    # Build HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
        }}
        .header .meta {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .stats {{
            background: white;
            padding: 15px 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: inline-block;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stats strong {{
            font-size: 32px;
            color: #667eea;
            display: block;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
            font-size: 14px;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        .device-id {{
            font-family: 'Courier New', monospace;
            color: #666;
            font-size: 12px;
        }}
        .primary-ip {{
            font-family: 'Courier New', monospace;
            color: #2c3e50;
            background: #ecf0f1;
            padding: 3px 8px;
            border-radius: 4px;
        }}
        .status-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .status-active {{ background: #d4edda; color: #155724; }}
        .status-planned {{ background: #fff3cd; color: #856404; }}
        .status-offline {{ background: #f8d7da; color: #721c24; }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 NetBox Device Inventory Report</h1>
        <div class="meta">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</div>
    </div>
    
    <div class="stats">
        <span style="color: #666; font-size: 14px;">Total Devices</span>
        <strong>{total_count}</strong>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Device Name</th>
                <th>Device ID</th>
                <th>Site</th>
                <th>Manufacturer</th>
                <th>Model</th>
                <th>Type/Role</th>
                <th>Primary IP</th>
            </tr>
        </thead>
        <tbody>
"""
    
    # Add table rows
    for idx, device in enumerate(devices, 1):
        # Extract fields with fallbacks
        name = device.get('name', 'N/A')
        device_id = device.get('id', 'N/A')
        
        # Site is nested object
        site = device.get('site', {})
        site_name = site.get('name', 'N/A') if isinstance(site, dict) else 'N/A'
        
        # Device type contains manufacturer and model
        device_type = device.get('device_type', {})
        if isinstance(device_type, dict):
            manufacturer_obj = device_type.get('manufacturer', {})
            manufacturer = manufacturer_obj.get('name', 'N/A') if isinstance(manufacturer_obj, dict) else str(manufacturer_obj) if manufacturer_obj else 'N/A'
            model = device_type.get('model', 'N/A')
        else:
            manufacturer = 'N/A'
            model = 'N/A'
        
        # Device role
        role = device.get('device_role', {})
        role_name = role.get('name', 'N/A') if isinstance(role, dict) else 'N/A'
        
        # Primary IP (could be IPv4 or IPv6)
        primary_ip4 = device.get('primary_ip4', {})
        primary_ip6 = device.get('primary_ip6', {})
        
        if isinstance(primary_ip4, dict) and primary_ip4.get('address'):
            primary_ip = primary_ip4['address']
        elif isinstance(primary_ip6, dict) and primary_ip6.get('address'):
            primary_ip = primary_ip6['address']
        else:
            primary_ip = '-'
        
        html += f"""
            <tr>
                <td>{idx}</td>
                <td><strong>{name}</strong></td>
                <td><span class="device-id">{device_id}</span></td>
                <td>{site_name}</td>
                <td>{manufacturer}</td>
                <td>{model}</td>
                <td>{role_name}</td>
                <td><span class="primary-ip">{primary_ip}</span></td>
            </tr>
"""
    
    html += """
        </tbody>
    </table>
    
    <div class="footer">
        <p>NetBox Device Inventory | Powered by Itential Automation Platform</p>
    </div>
</body>
</html>
"""
    
    return html


if __name__ == "__main__":
    # Read from stdin or file
    if len(sys.argv) > 1:
        """Main function that handles script execution and output formatting."""
        parser = argparse.ArgumentParser(description='Add two numbers')
        parser.add_argument('--device', '-d', required=True, help='device list')
        args = parser.parse_args()
        data = args.device
    else:
        data = json.load(sys.stdin)
    
    html = generate_html_table(data)
    print(html)
