import ac_data
import mal_data


USER_CHOICE = """
Choose which service you want to fetch from:
- 'a' : AC - basic metadata and next volumes dates
- 'm' : MAL - ratings, popularity and rank
- 'b' : Fetches from both services and then quits
- 'q' : QUIT

Scelta: """

def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'a':
            ac_data.get_manga()    
        elif user_input == 'm':
            mal_data.get_manga()
        elif user_input == 'b':
            ac_data.get_manga()
            mal_data.get_manga()
            quit()
        user_input = input(USER_CHOICE)

menu()