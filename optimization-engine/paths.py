import os
import sys

dirs = ['optimizer', 'predictor', 'costModel']
for i in dirs:
    package_path = os.path.abspath(i)
    sys.path.append(package_path)

print(sys.path)