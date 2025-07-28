#!/usr/bin/env python3
"""
Microtek Inverter Status Scraper
Flask API to fetch and return inverter status data as JSON
"""

import re
import requests
from flask import Flask, jsonify
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Default inverter IP address
DEFAULT_INVERTER_IP = "192.168.100.52"
INVERTER_IP = DEFAULT_INVERTER_IP

def extract_js_variables(html_content):
    """
    Extract JavaScript variables from the HTML content.
    Returns a dictionary with variable names as keys and their values.
    """
    variables = {}
    
    # Define the variables we want to extract
    var_patterns = [
        'webdata_sn', 'webdata_msvn', 'webdata_ssvn', 'webdata_pv_type',
        'webdata_rate_p', 'webdata_now_p', 'webdata_today_e', 'webdata_total_e',
        'webdata_alarm', 'webdata_utime', 'cover_mid', 'cover_ver', 'cover_wmode',
        'cover_ap_ssid', 'cover_ap_ip', 'cover_ap_mac', 'cover_sta_ssid',
        'cover_sta_rssi', 'cover_sta_ip', 'cover_sta_mac', 'status_a', 'status_b', 'status_c'
    ]
    
    for var_name in var_patterns:
        # Pattern to match: var variable_name = "value";
        pattern = rf'var\s+{var_name}\s*=\s*"([^"]*)"'
        match = re.search(pattern, html_content)
        if match:
            value = match.group(1).strip()
            variables[var_name] = value
        else:
            logger.warning(f"Variable {var_name} not found in HTML content")
            variables[var_name] = None
    
    return variables

def fetch_inverter_status():
    """
    Fetch the status page from the inverter and extract all variables.
    Returns a dictionary with the extracted data.
    """
    try:
        # Build URL dynamically using current INVERTER_IP
        status_url = f"http://{INVERTER_IP}/status.html"
        
        # Fetch the status page
        response = requests.get(status_url, timeout=10)
        response.raise_for_status()
        
        # Extract variables from the HTML content
        variables = extract_js_variables(response.text)
        
        # Convert numeric values to appropriate types
        numeric_fields = ['webdata_now_p', 'webdata_today_e', 'webdata_total_e', 
                         'webdata_utime', 'status_a', 'status_b', 'status_c']
        
        for field in numeric_fields:
            if variables.get(field) and variables[field].isdigit():
                variables[field] = int(variables[field])
            elif variables.get(field):
                try:
                    variables[field] = float(variables[field])
                except ValueError:
                    # Keep as string if conversion fails
                    pass
        
        return variables
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from inverter: {e}")
        raise Exception(f"Failed to connect to inverter at {INVERTER_IP}: {e}")
    except Exception as e:
        logger.error(f"Error processing inverter data: {e}")
        raise

@app.route('/', methods=['GET'])
def get_inverter_status():
    """
    Root endpoint that returns complete inverter status as JSON.
    """
    try:
        status_data = fetch_inverter_status()
        
        # Return all data directly
        response_data = {
            'success': True,
            'inverter_ip': INVERTER_IP,
            'data': status_data
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        error_response = {
            'success': False,
            'error': str(e),
            'inverter_ip': INVERTER_IP
        }
        return jsonify(error_response), 500

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Microtek Inverter Status API')
    parser.add_argument('--ip', '--inverter-ip', 
                       default=DEFAULT_INVERTER_IP,
                       help=f'Inverter IP address (default: {DEFAULT_INVERTER_IP})')
    parser.add_argument('--port', 
                       type=int, 
                       default=5000,
                       help='Flask server port (default: 5000)')
    parser.add_argument('--host',
                       default='0.0.0.0',
                       help='Flask server host (default: 0.0.0.0)')
    
    args = parser.parse_args()
    
    # Set global variables
    INVERTER_IP = args.ip
    STATUS_URL = f"http://{INVERTER_IP}/status.html"
    
    # Start Flask server
    logger.info(f"Starting Flask server on {args.host}:{args.port}")
    logger.info(f"Inverter IP: {INVERTER_IP}")
    app.run(host=args.host, port=args.port, debug=True)