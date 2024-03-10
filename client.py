# client.py

import xmlrpc.client

# Initialize the server proxy
server = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Starting the client loop
while True:
    # Printing the options/choices
    print("\n########### Menu ############")
    print("1. Add a note")
    print("2. Get notes by topic")
    print("0. Exit")

    # Getting the user's input/choice
    choice = input("Enter your choice: ")

    # If user chooses 1, add a new note by requesting the user for the topic and text and passing it to the server
    if choice == '1':
        try:
            topic = input("Enter topic: ")
            text = input("Enter text: ")
            result = server.addNewNote(topic, text)
            print("\n########### Result ############")
            print(f"\n{result}")
        except xmlrpc.client.Fault as error:
            print("Error:", error.faultString)
        except Exception as e:
            print("Error occured:", str(e))

    # If user chooses 2, get notes by topic and passing it to the server
    elif choice == '2':
        try:
            topic = input("Enter topic to search for notes: ")
            notes = server.getNotes(topic)
            print(f"\n########### Notes for {topic}  ############")
            i = 1
            if isinstance(notes, list):
                for note in notes:
                    print(f"Note {i}: {note['text']} - Timestamp: {note['timestamp']}")
                    i += 1
            else:
                print(notes)
        except Exception as e:
            print(f"Error occured: {str(e)}")

    # If user chooses 0, exit the client loop
    elif choice == '0':
        break
    else:
        print("Invalid input. Input must be either 1, 2, or 0.")
