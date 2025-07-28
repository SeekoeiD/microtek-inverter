# Microtek Inverter Status API

A Python Flask application that scrapes status data from a Microtek inverter and provides it via REST API endpoints.

## Features

- Scrapes all status variables from the inverter's web interface
- Provides RESTful API endpoints to access the data
- Returns data in JSON format
- Handles numeric type conversion automatically
- Includes error handling and logging

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

You can specify the inverter IP address as a command line parameter:

```bash
python microtek.py --ip 192.168.100.52
```

Or edit the `DEFAULT_INVERTER_IP` variable in `microtek.py` to set a default:
```python
DEFAULT_INVERTER_IP = "192.168.100.52"  # Change this to your inverter's IP
```

## Usage

1. Start the Flask server with default settings:
```bash
python microtek.py
```

2. Or specify custom IP address and port:
```bash
python microtek.py --ip 192.168.1.100 --port 8080 --host 127.0.0.1
```

3. The API will be available at `http://localhost:5000` (or your custom host/port)

### Command Line Options

```bash
python microtek.py --help
```

Available options:
- `--ip, --inverter-ip`: Inverter IP address (default: 192.168.100.52)
- `--port`: Flask server port (default: 5000)
- `--host`: Flask server host (default: 0.0.0.0)

## API Endpoints

### GET `/`
Returns complete inverter status data including all variables:
- Serial number, version info
- Current power output
- Daily and total energy
- Network configuration
- Status indicators

Example response:
```json
{
  "success": true,
  "inverter_ip": "192.168.100.52",
  "data": {
    "webdata_sn": "SH1ES140M3J019",
    "webdata_now_p": 70,
    "webdata_today_e": 0.4,
    "webdata_total_e": 5.0,
    "webdata_msvn": "V360",
    "webdata_pv_type": "SH1ES140",
    "cover_sta_ssid": "UNIFI_IoT_2G",
    "cover_sta_rssi": "82%",
    "cover_sta_ip": "192.168.100.52",
    "status_a": 1,
    "status_b": 0,
    "status_c": 0
  }
}
```

## Testing

Run the test script to verify all endpoints:
```bash
python test_api.py
```

## Command Line Equivalent

The original curl command:
```bash
curl -s http://192.168.100.52/status.html | grep 'var webdata_now_p' | sed 's/.*"\(.*\)".*/\1/'
```

Is now available as:
```bash
curl http://localhost:5000/
```

And you can extract specific values using jq:
```bash
# Get current power
curl -s http://localhost:5000/ | jq '.data.webdata_now_p'

# Get today's energy
curl -s http://localhost:5000/ | jq '.data.webdata_today_e'
```

## Variables Extracted

The script extracts all these JavaScript variables from the inverter:

- `webdata_sn` - Serial number
- `webdata_msvn` - Main software version
- `webdata_ssvn` - Sub software version  
- `webdata_pv_type` - PV type
- `webdata_rate_p` - Rated power
- `webdata_now_p` - Current power output
- `webdata_today_e` - Today's energy
- `webdata_total_e` - Total energy
- `webdata_alarm` - Alarm status
- `webdata_utime` - Update time
- `cover_mid` - Module ID
- `cover_ver` - Cover version
- `cover_wmode` - WiFi mode
- `cover_ap_ssid` - AP SSID
- `cover_ap_ip` - AP IP
- `cover_ap_mac` - AP MAC
- `cover_sta_ssid` - Station SSID
- `cover_sta_rssi` - Signal strength
- `cover_sta_ip` - Station IP
- `cover_sta_mac` - Station MAC
- `status_a`, `status_b`, `status_c` - Status indicators
