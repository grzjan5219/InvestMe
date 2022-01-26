import sys
import subprocess

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'plotly', 'flask', 'pandas', 'yfinance', 'CurrencyConverter', 'pandas-datareader', 'currency-symbols'])
