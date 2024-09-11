# InvestMe
# GL training group project. 
Python based web app, which presents the actual and historical prices of selected cryptocurrencies in the particular currency. 
Data should be fetched from chosen open API and presented in form of charts and tables. 
Fetched data and prices trends should be analysed, so app suggests when to buy or sell particular cryptocurrencies. 

Technologies considered to be used: Flask, yfinance, Pandas, plotly

Following decisions were made during the brainstorm phase of the project:

The API:
The API to be used is called 'YahooFinance'. This API was carefully chosen among the other cryptocurrency APIs, due to its features. Through research of the APIs that would help reach the goal of creating the python based project app, this one was decided to be the best choice. The API was tested, and it ran flawlessly. (Main factors that led to the decision: Ease of use, meets the requirements).

Technology used (framework):
Flask or Django? The framework of choice, after considering the requirements, needs and possibilities of the team is Flask. Django proved to be much harder to use, and understand hence Flask was chosen in it's place. Flask meets all the expectations just as much as Django does, so chosing Flask over Django due to its easier form isn't affecting the project in any way.

Library used to generate graphs:
There are a few libraries in Python, that could be used to create a graph like required by our application. Although many meet the requirements, not many are interactive and can show you data upon "hovering" over the part of interest. Exactly for this reason it was decided that the best choice would be 'plotly'. The library has great graph-drawing capabilities and is interactive which was our deciding factor while chosing.

########## Setup ###########

This project uses many various libraries supplied by the python community. Libraries used are:

Flask - The main library used by the project to run the application. Without it the app simply wouldn't work.
yfinance - The YahooFinance API that is responsible for getting the required data to the application.
pandas - A Data management API used for reading and managing data.
pandas_datareader - A pandas relative library, used for improving the managing part of pandas.
requests - A built-in Python module, used for getting the data from the API.
datetime - A bult-in Python module, that is rather self-explanatory - used for getting data about time and date.
currency-symbols - A library used as the name advises - for getting currency symbols.


TO jest dowóð na to że zmieniłem ten plik
