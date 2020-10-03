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
Start the server + file consumer:
```
python test.py
```

Check the metrics:
```
(master)> curl -s localhost:8000 | grep -v "^#"
```
Yielding:
```
...
GLL_lat{talker="GP"} 6004.931
GLL_lon{talker="GP"} 2332.139
VTG_true_track{talker="II"} 209.3
VTG_mag_track{talker="II"} 209.3
VTG_spd_over_grnd_kts{talker="II"} 5.71
ZDA_local_zone{talker="GP"} 0.0
MWD_wind_speed_knots{talker="II"} 8.1
MWD_wind_speed_meters{talker="II"} 4.17
MWV_wind_angle{talker="II"} 343.0
MWV_wind_speed{talker="II"} 13.8
DBT_depth_feet{talker="II"} 22.93
DBT_depth_meters{talker="II"} 6.99
DBT_depth_fathoms{talker="II"} 3.77
VHW_water_speed_knots{talker="II"} 6.08
VHW_water_speed_km{talker="II"} 11.26
VPW_speed_kn{talker="II"} 5.32
VWT_wind_angle_vessel{talker="II"} 30.0
VWT_wind_speed_knots{talker="II"} 8.22
VWT_wind_speed_meters{talker="II"} 4.23
```
