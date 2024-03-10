# server.py

import xmlrpc.server
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

"""
addNewNote is used to add a new note to the notes.xml file
"""
def addNewNote(topicName, topicText):
    try:
        # Retrieving the current date and time
        timenow = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        tree = ET.parse('notes.xml')
        root = tree.getroot()

        # Checking if the topic already exists
        topicExists = False
        for element in root.findall('topic'):
            if element.attrib.get('name') == topicName:
                topicExists = True
                note = ET.SubElement(element, 'note')
                text = ET.SubElement(note, 'text')
                text.text = topicText
                timestamp = ET.SubElement(note, 'timestamp')
                timestamp.text = timenow
                break
        
        # Checking if the topic doesn't exist, creating a new one if needed
        if not topicExists:
            topic = ET.Element('topic')
            topic.set('name', topicName)
            root.append(topic)
            if openSearchWikipedia(topicName):
                wikipediaNote = ET.SubElement(topic, 'note')
                wikipediaText = ET.SubElement(wikipediaNote, 'text')
                wikipediaText.text = openSearchWikipedia(topicName)
                wikipediaTimestamp = ET.SubElement(wikipediaNote, 'timestamp')
                wikipediaTimestamp.text = timenow
            note = ET.SubElement(topic, 'note')
            text = ET.SubElement(note, 'text')
            text.text = topicText
            timestamp = ET.SubElement(note, 'timestamp')
            timestamp.text = timenow

        # Writing the updated notes.xml file
        tree.write('notes.xml')

        # Returning a success message
        return "Added new note successfully"
    
    # Catching any exceptions and return an error message
    except Exception as e:
        return f"Error while adding new note: {str(e)}"
    
"""
GetNotes is used to get all the notes under a topic
"""
def getNotes(topicName):
    try:
        tree = ET.parse('notes.xml')
        root = tree.getroot()
        
        # Checking for the wanted topic and appending all the notes to the 'notes' list
        notes = []
        for element in root.findall('topic'):
            if element.attrib.get('name') == topicName:
                for note_elem in element.findall('note'):
                    text = note_elem.find('text').text.strip()
                    timestamp = note_elem.find('timestamp').text.strip()
                    notes.append({'text': text, 'timestamp': timestamp})
                return notes # Returning notes lsit
            
        # Returning an error message if the topic is not found
        return "Topic not found or no notes under the topic."
    
    # Catching any exceptions and return an error message
    except Exception as e:
        return f"Error while retrieving notes: {str(e)}"

"""
openSeachWikipedia is used to open search in Wikipedia
"""
def openSearchWikipedia(topicName):
    try:
        # Initializing the URL for Wikipedia API open search
        url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={topicName}&limit=1&namespace=0&format=json"
        
        # Sending the request and getting the response
        response = requests.get(url)

        # Parsing the response and returning the URL of the first result
        data = response.json()

        # Priting the URL of the first result in the server output for debugging
        print(f"Wikipedia Article URL for {topicName}: {data[3][0]}")

        # Returning the URL of the first result
        if data[3][0] != "":
            return data[3][0]
        
        # Returning False if no result is found
        else:
            return False
        
    # Catching any exceptions and return an error message
    except Exception as e:
        return f"Error while open searching in Wikipedia API: {str(e)}"

# Starting the server at localhost:8000
with xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000)) as server:
    # Registering the functions
    server.register_function(addNewNote, 'addNewNote')
    server.register_function(getNotes, 'getNotes') 
    server.register_function(openSearchWikipedia, 'openSearchWikipedia')

    # Starting the server
    print("Server is listening on port 8000...")
    server.serve_forever()
