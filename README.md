# ExLibris-Alma-change-portfolio-material-type

Brief Description: This script retrieves premade reports from Alma analytics and changes each portfolios contained in the reports material type.

Long description/background:
This script was made to quickly change material types based on analytics filters. Four reports sit static in analytics they are for the following:
	• Portfolio's with the portfolio material type videos, which is changed to streaming videos
	• Portfolio's with the bib material type as book and portfolio material type as unknown, unknown is changed to book
	• Portfolio's with the bib material type as journal and portfolio material type as unknown, unknown is changed to journal
	• Portfolio's with the bib material type as music and portfolio material type as unknown, unknown is changed to streaming audio
Two test reports are also included.
A main project runs setting the analytics paths and desired material type, those and a report name is sent to a function to change the material type.
In the change material type function , the reports are retrieved by their from analytics in XML format. Each column from the report that needs to be added to a list it sent to another function with the XML root to parse the XML tree for that element and send it back as a list. If no elements were added to the list no further processing takes place and the analytics XML is saved to a file. If the lists contain elements a data frame is made from the lists. A JSON data object is created including the desired material type values passed from the main function. The columns of the dataframe are then added to arrays/lists. Each list/array is iterated over by a loop to create the link to send a put request to the Alma API. Error messages are added to the dataframe as a new column called 'Notes'. The updated dataframe is than saved as a new csv file.
	
Language: Python
APIs: 
	• Analytics - Production Read-only
	• Electronic - Read/write
Originally written and executed with Anaconda/Jupyter

Analytics reports location: ACU>Reports>C&A>Clean up tasks>Reports used by Scripts/API

Modules/Libraries used:
	• Requests (for API communication)
	• Requests.structures import CaseInsensitiveDict (used to create and send JSON data objects)
	• Pandas (using and creating data frames)
	• xml.etree.ElementTree (used to parse XML file)
	• Re (regular expressions)
	• Datetime (current day/time, used to time)

Includes:
	• Timing the script from start to finish
	• Sending a Get API request to Alma analytics to retrieve reports in XML.
	• Parsing XML into lists for required elements into lists
	• Using and if/else statement to check for a resumption token and running a loop to retrieve and append data when there is one.
	• Creating a data frame from lists
	• Converting data frame columns into arrays, stored as variables
	• Iterating over the arrays above using a for loop, values contained in the arrays used to build individual links for each fine to be sent to the API
	• Put API requests with JSON object and write response to variable
	• Selection statement, look for error notifier with regular expressions:
		○ If there is error: Look for error message in response using regular expressions and contain the message, add it to variable
		○ If there is no error add success message to variable
	• Add either success or error message (contained in variable) to the notes column of the data frame
	• Write new data frame with updated notes column with error and success messages to csv
	• Display records processed, for each report.

Resources Used:
API console https://developers.exlibrisgroup.com/console/
Rest Portfolio: https://developers.exlibrisgroup.com/alma/apis/docs/xsd/rest_portfolio.xsd/?tags=PUT (What can be added in JSON object for ePortfolios)
Put method with JSON data object https://stackoverflow.com/questions/52510584/http-put-request-in-python-using-json-data
Pandas cheat sheet: http://datacamp-community-prod.s3.amazonaws.com/f04456d7-8e61-482f-9cc9-da6f7f25fc9b
Regular Expressions Python Capture groups: https://stackoverflow.com/questions/48719537/capture-groups-with-regular-expression-python
Find substring in string http://net-informations.com/python/basics/contains.htm#:~:text=Using%20Python's%20%22in%22%20operator,%2C%20otherwise%2C%20it%20returns%20false%20.
Update Dataframes https://www.askpython.com/python-modules/pandas/update-the-value-of-a-row-dataframe?fbclid=IwAR3o7WAnpPYk6q7PmyMcpmpW8F9F4EVzV3GR-KoUAdmGPOUaIkELYoZOAhA
Create data frames: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/
Parse XML in python: https://docs.python.org/3/library/xml.etree.elementtree.html![image](https://github.com/ramerrick/ExLibris-Alma-change-portfolio-material-type/assets/119052194/14c76bb1-0d6d-472c-9e76-7bde58199def)
