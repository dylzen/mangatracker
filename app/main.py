import ac_data
import mal_data
import popculture


USER_CHOICE = """
Choose an option:
- 'a' : AC - get basic metadata and next volumes dates
- 'm' : MAL - get ratings, popularity and rank
- 'b' : Fetches from both services, then quits
- 'p' : Search for manga (user input) and get volumes' links, then quits
- 'q' : QUIT

Choice: """

def menu():
    user_input = input(USER_CHOICE)
    while user_input != 'q':
        if user_input == 'a':
            ac_data.get_titles()
            ac_data.get_info()
            ac_data.get_release_dates()
            ac_data.write_info
        elif user_input == 'm':
            mal_data.get_titles()
            mal_data.get_metadata()
            # mal_data.write_metadata()
            # mal_data.stop_driver()
        elif user_input == 'b':
            ac_data.get_titles()
            ac_data.get_info()
            ac_data.get_release_dates()
            ac_data.write_info
            mal_data.start_driver()
            mal_data.get_titles()
            mal_data.get_metadata()
            mal_data.write_metadata()
            mal_data.stop_driver()
            quit()
        elif user_input == 'p':
            popculture.search_manga()
            quit()
        user_input = input(USER_CHOICE)

menu()