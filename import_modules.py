import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'plotly', 'flask', 'pandas', 'yfinance', 'pandas-datareader', 'currency-symbols'])
