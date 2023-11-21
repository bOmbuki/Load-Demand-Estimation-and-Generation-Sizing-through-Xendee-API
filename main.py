import subprocess
import sys

subprocess.run([sys.executable, 'Sort_excel.py'])

subprocess.run([sys.executable, 'daily_LoadProfile.py'])

subprocess.run([sys.executable, 'yearly_demand.py'])

subprocess.run([sys.executable, 'api_Optimization.py'])