# NEMA0183 to Prometheus
Tiny proof of concept for converting NEMA0183 messages into Prometheus metrics.
Based upon [pynmea2](https://github.com/Knio/pynmea2).

# Installation
Install dependencies:
```
pip install -r requirements.txt
```

## Data acquisition (Optional)
The repository ships with a minimal `nmea0183.dat` from `pynmea2`.

However a full daysail dataset, might be more interesting, and can be acquired:
```
wget https://raw.githubusercontent.com/SignalK/signalk-server/master/samples/plaka.log -O nmea0183.dat
```

# Usage
```
python test.py
```
