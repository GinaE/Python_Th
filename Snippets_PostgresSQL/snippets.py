# snippets.py basically puts and gets entries into a data base. 
# from the promt line use the commands: 
#    python3 snippets.py put Key "Snippet to be kept under Key" ---> to put an entry into the data base
#    python3 snippets.py get select ---> Get the snippet that is kept under the key "OldKey"
# To check how the data base, or the table is looking like, enter psql using the name of the data base:
#    psql -d snippets
# inside psql, you can run SQL queries on the data base:
#    table snippets;
#    select * from snippets;
#    select message from snippets; 



import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")  # should have been created before, we did it with PostgreSQL
logging.debug("Database connection established.")

''' # "Put" Skeleton
def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
'''

''' # "get" skeleton
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet "Error message: Snippet not found"
    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""
'''    
    
# "Put" Fleshed, with the commands from psql

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    
    ''' Testing cursor as a context manager bellow
    cursor = connection.cursor()
    try:
        command = "insert into snippets values (%s, %s)"
        cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
        connection.rollback()
        command = "update snippets set message=%s where keyword=%s"
        cursor.execute(command, (snippet, name))    
    connection.commit()
    '''
    # with connection, connection.cursor() as cursor:
    try:
        with connection, connection.cursor() as cursor:
            command = "insert into snippets values (%s, %s)"
            cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:     # this error is triggered if the snippet is already there.
        with connection, connection.cursor() as cursor:
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))  
         
    
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet "Error message: Snippet not found"
    Returns the snippet.
    """
    logging.info("Getting snippet named {!r}".format(name))
    
    ''' # commit and roll back can be automated by using cursor as  context manager (next uncommented 3 lines)    
    # cursor = connection.cursor()
    # command = "select message from snippets where keyword=%s"
    # cursor.execute(command, (name,)) 
    # snippet = cursor.fetchone() 
    # connection.commit()   
    '''   
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        snippet = cursor.fetchone()
    
    logging.debug("Snippet retrieved successfully.")
    if not snippet:
        return "Error message: Snippet {!r} not found ".format(name)  # return will break the loop
    return snippet[0]
    
    

def catalog():
    '''
    # catalog() function, you'll need to query the keywords from the snippets table    
    '''
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword")
        catalog_list = cursor.fetchall()  #??? tuple, makes a tuple of every entry
    logging.debug("The catalog was retrieved successfully.")
    if not catalog_list:
        return "Error message: There are not available entries"  # return will break the loop
        
    return([x[0] for x in catalog_list]) 
    
def search(string_name):
    '''
    listing snippets which contain a given string anywhere in their messages.
    '''
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where message like '% %s %'",(string_name,))
        catalog_list = cursor.fetchall()  #??? tuple, makes a tuple of every entry


def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # put subparser
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    # get subparser
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieves a snippet")
    get_parser.add_argument("name", help="The name of the snippet")

    # catalog subparser
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="shows a list of available keys")


    arguments = parser.parse_args()
    
     # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        catalog_list = catalog(**arguments)
        print("The available keys are: {!r}".format(catalog_list))    
    
    

if __name__ == "__main__":
    main()