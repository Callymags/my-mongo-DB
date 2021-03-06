import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "myFirstDB"
COLLECTION = "celebrities"


def mongo_connect(url):
    try: 
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could noot connect to MongoDB: %s") % e


def show_menu():
    print("")
    print('1. Add a record')
    print('2. Find a record')
    print('3. Edit a record')
    print('4. Delete a record')
    print('5. Exit')

    option = input('Enter option: ')
    return option


def get_record():
    print('')
    first = input('Enter first name > ')
    last = input('Enter last name > ')

    try: 
        doc = coll.find_one({'first': first.lower(),'last': last.lower()})

    except: 
        print('Error accessing the database')

    # If no results can be found in doc variable
    if not doc: 
        print('')
        print('Error. No results found')
    
    return doc



def add_record():
    print('')
    first = input('Enter first name > ')  
    last = input('Enter last name > ')
    dob = input('Enter date of birth > ')
    gender = input('Enter gender > ')
    hair_color = input('Enter hair color > ')
    occupation = input('Enter occupation > ')
    nationality = input('Enter nationality > ')


    new_doc = {
        'first': first.lower(),  
        'last': last.lower(),
        'dob': dob,
        'gender': gender,
        'hair_color': hair_color,
        'occupation': occupation,
        'nationality': nationality
    }

    try:
        coll.insert(new_doc)
        print('')
        print('Document inserted')
    except:
        print('Error accessing the database')


def find_record():
    # Get results of get_record function
    doc = get_record()
    # If we have results 
    if doc: 
        print('')
        # k=key, v=value
        for k , v in doc.items():
            # Ensure we don't display secret _id generated by Mongo 
            if k != '_id':
                # Capitalize key, value in display
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    # Store results of get_record() in doc 
    doc = get_record()
    if doc:
        # Values will be added to empty update_doc dictionary
        update_doc = {}
        print('')
        for k, v in doc.items():
            # Filter out ID field since this will not be edited  
            if k != '_id':
                # Every iteration will provide the key for our update_doc var and set it 
                # equal to user input
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")

                # If user input is blank, leave the value the same as before 
                if update_doc[k] == '':
                    update_doc[k] = v
                
        # Check to see if doc gets updated successfully 
        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the database")


def delete_record():
    doc = get_record()
    # If a result is found, do the following 
    if doc: 
        print('')
        # Iterate through and print each value to make sure we delete correct record
        for k,v in doc.items():
            if k != '_id':
                print(k.capitalize() + ': ' + v.capitalize())
        
        print('')
        confirmation = input('Is this the document you want to delete?\nY or N > ')
        print('')

        if confirmation.lower() == 'y':
            try:
                coll.remove(doc)
                print('Document deleted')
            except:
                print('Error accessing db')
        else:
            print('Document not deleted')


def main_loop():
    while True: 
        option = show_menu()
        if option == '1':
            add_record()
        elif option == '2':
            find_record()
        elif option == '3':
            edit_record()
        elif option == '4':
            delete_record()
        elif option == '5':
            conn.close()
            break
        else:
            print('Invalid option')
        print('')


conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()