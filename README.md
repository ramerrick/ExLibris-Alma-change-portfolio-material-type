# ExLibris-Alma-change-portfolio-material-type

<b>Brief Description:</b> This script retrieves premade reports from Alma analytics and changes each portfolios contained in the reports material type.

<b>Long description/background:</b></br>
This script was made to quickly change material types based on analytics filters. Four reports sit static in analytics they are for the following:
<ul>
<li>Portfolio's with the portfolio material type videos, which is changed to streaming videos</li>
<li>Portfolio's with the bib material type as book and portfolio material type as unknown, unknown is changed to book</li>
<li>Portfolio's with the bib material type as journal and portfolio material type as unknown, unknown is changed to journal</li>
<li>Portfolio's with the bib material type as music and portfolio material type as unknown, unknown is changed to streaming audio</li>
</ul>
Two test reports are also included.</br>
</br>
A main project runs setting the analytics paths and desired material type, those and a report name is sent to a function to change the material type.
In the change material type function , the reports are retrieved by their from analytics in XML format. Each column from the report that needs to be added to a list it sent to another function with the XML root to parse the XML tree for that element and send it back as a list. If no elements were added to the list no further processing takes place and the analytics XML is saved to a file. If the lists contain elements a data frame is made from the lists. A JSON data object is created including the desired material type values passed from the main function. The columns of the dataframe are then added to arrays/lists. Each list/array is iterated over by a loop to create the link to send a put request to the Alma API. Error messages are added to the dataframe as a new column called 'Notes'. The updated dataframe is than saved as a new csv file.</br>
	
<b>Language:</b> Python</br>
</br>
<b>APIs:</b>
<ul>
<li>Analytics - Production Read-only</li>
<li>Electronic - Read/write</li></br>
</ul>
Originally written and executed with Anaconda/Jupyter</br>
</br>
<b>Modules/Libraries used:</b>
<ul>
<li>Requests (for API communication)</li>
<li>Requests.structures import CaseInsensitiveDict (used to create and send JSON data objects)</li>
<li>Pandas (using and creating data frames)</li>
<li>xml.etree.ElementTree (used to parse XML file)</li>
<li>Re (regular expressions)</li>
<li>Datetime (current day/time, used to time)</li>
</ul>

<b>Includes:</b>
<ul>
<li>Timing the script from start to finish</li>
<li>Sending a Get API request to Alma analytics to retrieve reports in XML.</li>
<li>Parsing XML into lists for required elements into lists</li>
<li>Using and if/else statement to check for a resumption token and running a loop to retrieve and append data when there is one.</li>
<li>Creating a data frame from lists</li>
<li>Converting data frame columns into arrays, stored as variables</li>
<li>Iterating over the arrays above using a for loop, values contained in the arrays used to build individual links for each fine to be sent to the API</li>
<li>Put API requests with JSON object and write response to variable</li>
<li>Selection statement, look for error notifier with regular expressions:</li>
		-If there is error: Look for error message in response using regular expressions and contain the message, add it to variable</br>
		-If there is no error add success message to variable
<li>Add either success or error message (contained in variable) to the notes column of the data frame</li>
<li>Write new data frame with updated notes column with error and success messages to csv</li>
<li>Display records processed, for each report.</li>
 </ul>

<b>Resources Used:</b></br>
API console https://developers.exlibrisgroup.com/console/
Rest Portfolio: https://developers.exlibrisgroup.com/alma/apis/docs/xsd/rest_portfolio.xsd/?tags=PUT (What can be added in JSON object for ePortfolios)</br>
Put method with JSON data object https://stackoverflow.com/questions/52510584/http-put-request-in-python-using-json-data</br>
Pandas cheat sheet: http://datacamp-community-prod.s3.amazonaws.com/f04456d7-8e61-482f-9cc9-da6f7f25fc9b</br>
Regular Expressions Python Capture groups: https://stackoverflow.com/questions/48719537/capture-groups-with-regular-expression-python</br>
Find substring in string http://net-informations.com/python/basics/contains.htm#:~:text=Using%20Python's%20%22in%22%20operator,%2C%20otherwise%2C%20it%20returns%20false%20.</br>
Update Dataframes https://www.askpython.com/python-modules/pandas/update-the-value-of-a-row-dataframe?fbclid=IwAR3o7WAnpPYk6q7PmyMcpmpW8F9F4EVzV3GR-KoUAdmGPOUaIkELYoZOAhA</br>
Create data frames: https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-lists/</br>
Parse XML in python: https://docs.python.org/3/library/xml.etree.elementtree.html![image](https://github.com/ramerrick/ExLibris-Alma-change-portfolio-material-type/assets/119052194/14c76bb1-0d6d-472c-9e76-7bde58199def)</br>
