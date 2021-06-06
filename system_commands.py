from os import system
from datetime import date, datetime, timedelta, time
from time import sleep


def bash_command(user_in):
    _ = system(user_in)


def clear_screen():
    bash_command('clear')


def days_between(start_date, end_date):
    d1 = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    d2 = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    delta = (d2 - d1).days
    return delta


def time_remaining_until_midnight(dt=None):
    if dt is None:
        dt = datetime.now()
    tomorrow = dt + timedelta(days=1)
    answer = str(datetime.combine(tomorrow, time.min) - dt)
    display = answer[:-7]
    return display


def countdown(time_in_seconds):
    while time_in_seconds:
        mins, secs = divmod(time_in_seconds, 60)
        timer = 'Time remaining until Sunday: {:02d}min {:02d}sec'.format(mins, secs)
        print(timer, end="\r")
        sleep(1)

        time_in_seconds -= 1
        clear_screen()


# date_to_check string format: 'dd/mm/yyyy hh:mm:ss'
def check_if_future_date(date_to_check):
    now = datetime.now()
    date_format = "%d/%m/%Y %H:%M:%S"

    # create datetime objects from the strings
    the_past = datetime.strptime(date_to_check, date_format)

    # If date is in the past
    if the_past < now:
        return True
    return False


if __name__ == '__main__':
    pass
