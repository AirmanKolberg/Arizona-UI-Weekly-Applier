from calendar import day_name
from datetime import datetime
import pandas as pd
from os import path, system


# Use this to verify yes or no questions
def verify_yes_or_no(response):

    if response == 'yes' or response == 'y':
        return True
    elif response == 'no' or response == 'n':
        return False
    else:
        response = input("Try again, simple 'yes', 'y', 'no', or 'n': ")
        verify_yes_or_no(response)


def create_framework(date, website, company, position, action):

    framework = {
        'date': [date],
        'website': [website],
        'company': [company],
        'position': [position],
        'action': [action]
    }
    return framework


def get_job_details_from_user():

    date = day_name[datetime.today().weekday()]

    user_responses = list()
    user_questions = ['Website applied: ', 'Company name: ',
                      'Position applied: ']

    for question in user_questions:
        user_responses.append(input(question))

    website = user_responses[0]
    company = user_responses[1]
    position = user_responses[2]

    action = 'Applied online.'

    framework = create_framework(date, website, company, position, action)

    return framework


def update_csv(pd_framework):

    df = pd.DataFrame(pd_framework, columns=['date', 'website', 'company',
                                             'position', 'action'])
    if path.exists('job_data.csv'):
        df.to_csv('job_data.csv', mode='a', header=False)
    else:
        df.to_csv('job_data.csv')


def add_new_job_application():

    # Retrieve user-input data
    framework = get_job_details_from_user()

    # Put that data into the DataFrame
    update_csv(framework)

    # Give user option to add another
    while True:
        response = input('Add another?\n').lower()

        if response == 'y' or response == 'yes':
            add_new_job_application()
        elif response == 'n' or response == 'no':
            exit()
        else:
            print(f"'{response}' isn't 'yes', 'no', 'y', nor 'n'.  Please try again.")


def check_if_weekly_search_continues(file_name):

    # Ensure file exists, and has <4 entries
    try:
        data = pd.read_csv(file_name)
        if len(data) > 3:
            return False
        return True
    except FileNotFoundError:
        return True


def main_menu():

    # Check if more job applications are required for the week
    continuing = check_if_weekly_search_continues('job_data.csv')

    if not continuing:
        wipe_everything = verify_yes_or_no(f"You've already logged 4+ jobs this week!  Wipe the file for the new week?\n")

        if wipe_everything:
            _ = system("rm 'job_data.csv'")

    # Add a new job application
    framework = get_job_details_from_user()

    # Save to .csv file
    update_csv(framework)


if __name__ == '__main__':
    main_menu()
