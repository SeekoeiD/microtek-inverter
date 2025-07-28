#!/usr/bin/env python3
"""
Test script for the Microtek inverter scraper
"""

import requests
import json

def test_endpoints():
    """Test the API endpoint"""
    base_url = "http://localhost:5000"
    
    try:
        print("--- Testing / endpoint ---")
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error testing /: {e}")

if __name__ == "__main__":
    test_endpoints()
