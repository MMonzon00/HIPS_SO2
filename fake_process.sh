#!/usr/bin/env python3
import numpy as np

# Generate a list of random byte arrays, each of size 1 MB (1024 * 1024 bytes)
result = [np.random.bytes(1024 * 1024) for x in range(8192)]

# Print the length of the result list
print(f"Length of result: {len(result)}")

#DON'T RUN THIS FILE IF YOU HAVE LESS THAN 16GB OF RAM
