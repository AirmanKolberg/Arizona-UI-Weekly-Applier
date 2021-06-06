from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from system_commands import *
from job_apply import verify_yes_or_no
from secrets import my_ssn, my_pin


def examine_verification_image():

    # Questions to verify with associated commands
    questions_and_commands = {
        "View the verification image?\n": 'open verification_image.png',
        "Delete the verification image?\n": 'rm verification_image.png'
    }

    # Iterate through questions
    for question in questions_and_commands:
        positive_response = verify_yes_or_no(input(question))

        # Execute commands if user responded "yes"
        if positive_response:
            try:
                bash_command(questions_and_commands[question])
            except FileNotFoundError:
                print('No file found...')


def fill_job_search_requirements(web_browser, date_today):

    # Gather the required fields for the job search section
    date_field = web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_ddlWSE_Date')
    website_field = web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_txtWSE_Website')
    company_name_field = web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_txtWSE_EmpName')
    type_of_work_field = web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_txtWSE_WorkSought')
    actions_taken_field = web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_txtWSE_Results')
    add_next_button_field = web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_btnWSE_AddEntry')

    # Grab data from the DataFrame
    data = pd.read_csv('job_data.csv')

    # Create lists from the DataFrame
    dates = list(data['date'])
    sites = list(data['website'])
    jobs = list(data['company'])
    positions = list(data['position'])
    actions = list(data['action'])

    # For debugging during next use
    input("If you've made it this far, you've reached your debug input statement!\nPress 'Return' to continue...")

    # Click a bunch of buttons
    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_btnNext').click()
    sleep(2)
    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_rblConfirmMainQuestions_0').click()
    sleep(1)
    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_btnNext').click()
    sleep(3)
    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_btnNext').click()
    sleep(2)

    # Final new section
    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_rblConfirmWorkSearch_0').click()
    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_btnNext').click()

    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_rblCertifyClaim_0').click()
    sleep(1)

    web_browser.find_element_by_id('ctl00_ContentPlaceHolder1_btnFileClaim').click()
    sleep(2)

    success_message = 'Claim Filed Successfully'
    final_page = web_browser.page_source
    web_browser.save_screenshot(f'verification_image_{date_today}.png')
    clear_screen()

    if success_message in final_page:
        print('All good to go for this week!')
    else:
        print('Something went wrong, please address.')

    web_browser.close()

    examine_verification_image()


def file_claim(ssn, pin):

    # Navigate to the application page and minimise the window
    firefox = webdriver.Firefox()
    firefox.get('https://azuiinternetweeklyclaim.azdes.gov/')
    firefox.minimize_window()
    sleep(2)

    # Insert the SSN and press 'Return'
    firefox.find_element_by_id('txtSSN1').send_keys(ssn[0:3])
    firefox.find_element_by_id('txtSSN2').send_keys(ssn[3:5])
    firefox.find_element_by_id('txtSSN3').send_keys([ssn[5:9], Keys.RETURN])
    sleep(3)

    # Click the button to file weekly claim
    firefox.find_element_by_id('ctl00_ContentPlaceHolder1_lbnFileClaim').click()
    sleep(3)

    # Insert the PIN and press 'Return'
    firefox.find_element_by_id('ctl00_ContentPlaceHolder1_txtPin').send_keys([pin, Keys.RETURN])
    sleep(3)

    # Select the appropriate answer buttons
    answers = ['ctl00_ContentPlaceHolder1_rblFF1_0',
               'ctl00_ContentPlaceHolder1_rblFF2_0',
               'ctl00_ContentPlaceHolder1_rblFF3_0',
               'ctl00_ContentPlaceHolder1_rblFF4_1',
               'ctl00_ContentPlaceHolder1_rblFF5_1',
               'ctl00_ContentPlaceHolder1_rblFF6_1',
               'ctl00_ContentPlaceHolder1_rblFF7Main_1',
               'ctl00_ContentPlaceHolder1_rblFF129Main_1',

               # And the "next" button
               'ctl00_ContentPlaceHolder1_btnNext']

    # Select all of the correct answers
    for answer in answers:
        firefox.find_element_by_id(answer).click()
    sleep(3)

    # Pass it off to the next (newly required) task!
    fill_job_search_requirements(firefox, str(date.today()))


# Checks every hour to see if it's time to file
def check_if_time_to_file(json_data):

    while True:
        time_to_file = check_if_future_date(json_data['next_file'])

        if time_to_file:
            file_claim(my_ssn, my_pin)
        else:

            # Check again in an hour
            sleep(3600)


if __name__ == '__main__':

    check_if_time_to_file()     # Needs JSON file
