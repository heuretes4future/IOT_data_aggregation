#!/usr/bin/env python3
import sys
from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

lat_arg = float(sys.argv[1])
lon_arg = float(sys.argv[2])
REF_POINT = (lat_arg, lon_arg)

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Timestamp") or line.startswith("Carbon"):
        continue
    try:
        parts = line.split()
        if len(parts) != 2:
            continue
        timestamp, co2 = parts
        co2 = float(co2)
        # Since you don't have lat/lon per reading, assume all readings are from REF_POINT
        distance = haversine(REF_POINT, REF_POINT)
        print(f"{distance:.2f}\t{co2}")
    except Exception as e:
        continue


