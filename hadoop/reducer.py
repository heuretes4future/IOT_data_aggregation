#!/usr/bin/env python3
import sys

count = 0
total = 0.0
min_val = float("inf")
max_val = float("-inf")

for line in sys.stdin:
    _, val = line.strip().split("\t")
    val = float(val)
    count += 1
    total += val
    min_val = min(min_val, val)
    max_val = max(max_val, val)

if count > 0:
    avg = total / count
    print(f"Min: {min_val}")
    print(f"Max: {max_val}")
    print(f"Avg: {avg}")
else:
    print("No values within distance.")

