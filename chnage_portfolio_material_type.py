#!/usr/bin/env python
# coding: utf-8

#Change elelctronic portfolio material type script
#Author Rachel Merrick
#This script was created for the purpose of changing ePortfolio material types based on exsisting Alma analytics reports.
#All reports are saved in this location: ACU>Reports>C&A>Clean up tasks>Reports used by Scripts/API
#The script sends an analytics report path and the desired material type to a function.
#The function then gets the report in XML, parses the XML adding relevant information to lists and a data set.
#A PUT request is sent to the Alma API to edit the material types for each item which appear in the Analytics report.
#Error messages and the material type changes are added to the dataframe as a new column called 'Notes'. 
#The updated dataframe is than saved as a new csv.The use of the function allows for multiple reports and records 
#to be processed in quick succession with minimal intervention.
#Originally written and executed with Anaconda/Jupyter:
#Some libraries may need to be installed before running the script in other environments.

#Import datetime module and set start time to time how long the script takes.
from datetime import datetime
start_time = datetime.now()
#Import required libraries/modules.
import requests as req #Used to to access Alma API.
from requests.structures import CaseInsensitiveDict #used to create and send JSON portfolio object.
import xml.etree.ElementTree as ET #Used to parse XML file.
import pandas as pd #Used to create data frame
import re #Allows use of regular expresions which have been used to extract error messages.

#### FUNCTIONS ####

#Function that gets attributes which interates over XML root and adds all instances of an attribute to a list.
#The list is then returned.
def get_attribute(attribute, root):
    #Create empty list
    All_values = []
    #interate over the XML root by attribute
    for attribute in root.iter(attribute):
        #append values to list.
        All_values.append(attribute.text)
    #return list of attributes.
    return All_values

#Function that writes response from analtics API to an xml file (so it can be read as XML rather than a string).
#Then the tree and root of the XML is found, the root is returned.
def process_xml(name, analytics_response):
    #writting analytics report (API repsonse) to xml file.
    response_xmlfile = open(name + '_analytics.xml', 'w') #Open file in write mode.
    response_xmlfile.write(analytics_response) #write to file.
    response_xmlfile.close() #Close file.
    
    #Declaring XML tree and root from analytics report.
    tree = ET.parse(name + '_analytics.xml')
    root = tree.getroot()
    return root

def create_dataframe(collection_list, service_list, portfolio_list):
    df_data = {'Collection ID' : collection_list , 'Service ID' : service_list, 'Portfolio ID' : portfolio_list }
    df = pd.DataFrame(df_data, columns=['Collection ID' , 'Service ID','Portfolio ID', 'Notes'] )
    return df

#Change material type function.
def change_material_type(name, path, material_type,material_description):
    
    #Print the name of report currently being processed.
    print("Processing: " + name)
    
    #Building anlytics API url and requesting it using get function.
    analytics_key = '' #Use your instiutions key
    analytics_url = ('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/analytics/reports?path='
                     +path+'&limit=1000&col_names=true&apikey=' + analytics_key)
    analytics_response = req.get(analytics_url)
    
    root = process_xml(name, analytics_response.text)
    
    #Call get_attribute method to parse over XML file and create lists for collection IDs, license IDs and Portfolio ID.
    collection_list = get_attribute('{urn:schemas-microsoft-com:xml-analysis:rowset}Column2', root)
    service_list = get_attribute('{urn:schemas-microsoft-com:xml-analysis:rowset}Column5', root)
    portfolio_list = get_attribute('{urn:schemas-microsoft-com:xml-analysis:rowset}Column4', root)
    
    #If the report holds no results stop any further processing and print message indicating this.
    if len(collection_list) == 0:
        print('Analytics report has no results, processing skiped. for more infomration see ' +name + '_analytics.xml.')
    
    #If report yields results continue.
    else:
        #Create data frame to record changes and errors.
        df = create_dataframe(collection_list, service_list, portfolio_list)

        #Loop with resumption token stuff will need to sit here
        finished_message = '<IsFinished>(.+)</IsFinished>'
        finished_check = re.search(finished_message, analytics_response.text)
        is_finished = finished_check.group(1)
        
        if is_finished == 'false':
            Resumption_token_message = '<ResumptionToken>(.+)</ResumptionToken>'
            Resumption_token_check = re.search(Resumption_token_message, analytics_response.text)
            Resumption_token = Resumption_token_check.group(1)
        
            while is_finished == 'false':
                analytics_url = ('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/analytics/reports?path='
                     +path+'&limit=1000&col_names=true&apikey=' + analytics_key + '&token=' + Resumption_token)
                analytics_response = req.get(analytics_url)
                root = process_xml(name, analytics_response.text)
                collection_list_2 = get_attribute('{urn:schemas-microsoft-com:xml-analysis:rowset}Column2', root)
                service_list_2 = get_attribute('{urn:schemas-microsoft-com:xml-analysis:rowset}Column5', root)
                portfolio_list_2 = get_attribute('{urn:schemas-microsoft-com:xml-analysis:rowset}Column4', root)
                df2 = create_dataframe(collection_list_2, service_list_2, portfolio_list_2)
                df = df.append(df2, ignore_index=True)
                collection_list.extend(collection_list_2)
                service_list.extend(service_list_2)
                portfolio_list.extend(portfolio_list_2)
                finished_check = re.search(finished_message, analytics_response.text)
                is_finished = finished_check.group(1)
        
        #Setting variables that will be used to build eResource API urls
        #eresource_key = '' #Use your instiutions key
        get_headers = {'Accept': 'application/json'}
        put_headers = CaseInsensitiveDict() #Used to send JSON portfolio object.
        put_headers["Content-Type"] = "application/json" #Used to send JSON portfolio object.
    
        #Variables used to detect and report errors.
        url_error = '<errorsExist>true</errorsExist>' #Test to indicate when an error is pressent in API request url.
        error_message = '<errorMessage>(.+)</errorMessage>' #Extracting the error message from API response.
        data_object_error = '"errorsExist":true' #Test to indicate when an error is pressent in JSON data object.

        #Loop iterating over the number of records in the Collection ID column. all columns should have 
        #the same number of rows.
        for i in range(len(collection_list)):
            #Setting the variable for the Collection ID, Service ID and Portfolio ID to be used in buidling the url.
            #All variables are converted to string so that the URL can be concatenated.
            collection = str(collection_list[i])
            service = str(service_list[i])
            portfolio = str(portfolio_list[i])
            #Building URL wil variables and electronic resource API key.
            url = ('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections/' + collection
                   + '/e-services/' + service + '/portfolios/' + portfolio + '?apikey='+ eresource_key)
            
            get_response = req.get(url, headers=get_headers)
            get_data  = str(get_response.text)
            json_data =re.sub('"material_type":{"value":".+?","desc":".+?"}',
                              '"material_type":{"value":"' + material_type + '","desc":"' + material_description + '"}',
                              get_data)
            json_data =re.sub('"material_type":{"value":"","desc":null}(,"activation_date".+)', 
                        '"material_type":{"value":"'+ material_type +'","desc":"'+ material_description+'"}\\1"}',
                        json_data)
            json_data =re.sub('"material_type":{"value":""}(,"activation_date".+)', 
                        '"material_type":{"value":"'+ material_type +'","desc":"'+ material_description+'"}\\1"}',
                        json_data)
            
            #Send request using Put URL and data object to Alma. Reponse will be contained in the variable.
            eresource_response = req.put(url, headers=put_headers, data=json_data.encode('utf-8'))
    
            #Selection statement if there is an error add error message to notes column of data frame, else No errors detected.
            #Testing for API url error, if error pressent add error to notes column.
            if url_error in eresource_response.text:
                note = re.search(error_message, eresource_response.text)
                df.at[i, 'Notes'] = note.group(1)
    
            #Testing for data object error, if error pressent add error to notes column.
            elif data_object_error in eresource_response.text:
                note = eresource_response.text
                df.at[i, 'Notes'] = note
    
            #Else no errors, add "No errors detected" to notes column.    
            else:
                note = 'No errors detected'
                df.at[i, 'Notes'] = note
    
        #save data frame to csv file.
        df.to_csv(name+'_response.csv')
    
        #Print information on number of records and the file name they have been saved to.
        print(str(i + 1) + " records processed and added to " 
              +name+'_response.csv file, please check there for details.')
    
    #print line break for clarity.
    print()
    
#### MAIN ####

#Paths to analytics reports
#Saved in ACU>Reports>C&A>Clean up tasks>Reports used by Scripts/API
test_path = '' #Use path to relevant analytics report.
test_path2 = '' #Use path to relevant analytics report.
video_path ='' #Use path to relevant analytics report.
book_path = '' #Use path to relevant analytics report.
journal_path = '' #Use path to relevant analytics report.
music_path ='' #Use path to relevant analytics report.

#Material types
streaming_video = 'STREAMINGV'
book = 'BOOK'
journal = 'JOURNAL'
streaming_audio = 'STREAMINGA'

#Material type descriptions
streaming_video_desc = 'Streaming Video'
book_desc = 'Book'
journal_desc = 'Journal'
streaming_audio_desc = 'Streaming Audio'

#Calls to change material type function
#change_material_type('Report1', test_path, streaming_video) #Using for testing.
#change_material_type('Report2',test_path2, book) #Using for testing.
change_material_type('video_report', video_path, streaming_video, streaming_video_desc) #Change video to streaming video.
change_material_type('unknown_book_report', book_path, book, book_desc) #Change unknown (bib material type book) to book.
change_material_type('unknown_journal_report', journal_path, journal, journal_desc) #Change unknown (bib journal type book) to journal.
change_material_type('unknown_audio_report', music_path, streaming_audio, streaming_audio_desc) #Change unknown (bib journal type music) to streaming audio.

#Program completeion messages.
print('all reports and records have now been processed.')
end_time = datetime.now()
print('Time taken: {}'.format(end_time - start_time))
