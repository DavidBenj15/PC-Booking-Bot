from  datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

TIMEOUT = 4

def handle_booking(bot, driver):
    return select_start_time(bot, driver)

def select_start_time(bot, driver):
    try:
        formatted_date_time = bot.format_date_time()
        box = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH,
                f'//a[@title="{formatted_date_time} - Gaming PC {bot.pc_number} - Available"]'))
            )
        box.click()
        return select_latest_end_time(bot, driver)
    except TimeoutException:
        return False
    
def select_latest_end_time(bot, driver):
    try:
        end_times_dropdown = WebDriverWait(driver, MAX_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH,
                                        '//select[starts-with(@id, "bookingend_")]'))  # dropdown id changes sometimes
            )
        select = Select(end_times_dropdown)

        # the following is straight from ChatGPT lmao
        # Get all the options from the dropdown
        options = select.options

        latest_time_option = None
        latest_time = datetime.min

        # Iterate through the options to find the one with the latest time value
        for option in options:
            option_text = option.text
            option_time = datetime.strptime(option_text, "%I:%M%p %A, %B %d, %Y") # format time
            if option_time > latest_time:
                latest_time = option_time
                latest_time_option = option

        # Select the option with the latest time value
        if latest_time_option is not None:
            latest_time_option.click()

        return submit_time_block(bot, driver) # submit!
    except TimeoutException:
        return False
    
def submit_time_block(bot, driver):
    print("Clicking submit time block")
    return True
