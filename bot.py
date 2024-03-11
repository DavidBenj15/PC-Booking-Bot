import time
import threading
from datetime import datetime, timedelta
from booking_logic import handle_booking
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

ROOM_LINK = "https://bookit.dmc.jhu.edu/reserve/GamingPCs"

class Bot(threading.Thread):
    def __init__(self, pc_number, target_time, conn, lock):
        super().__init__() # Call the constructor of the thread class
        self.pc_number = pc_number
        self.target_time = target_time
        self.conn = conn
        self.lock = lock

    def run(self):
        options = Options()
        options.add_experimental_option("detach", True) # keeps browser open after processes are complete 
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                options=options)
        driver.get(ROOM_LINK)
        driver.maximize_window()
        latest_time = datetime.strptime('23:45', '%H:%M')
        while self.target_time <= latest_time:
            success = self.book_pc(self.target_time)
            if not success:
                self.target_time += timedelta(minutes=15) # incrament target time by 15 minutes, try again       
    
    def book_pc(self, target_time):
        acquired_lock = self.acquire_lock(target_time)
        if acquired_lock:
            booked_successfully = handle_booking(self)
            if booked_successfully:
                return True
            else:
                self.release_lock(target_time) # if unsuccessful booking, release lock
        return False # if lock was not acquired or booking was unsucessful, return False

    def acquire_lock(self, resource):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM locks WHERE resource=?', (resource,))
            if cursor.fetchone() is None:
                cursor.execute('INSERT INTO locks VALUES (?)', (resource,))
                self.conn.commit()
                return True
            else:
                return False
            
    def release_lock(self, resource):
        with self.lock:
            self.conn.execute('DELETE FROM locks WHERE resource=?', (resource,))
            self.conn.commit()

    def format_date_time(self):
        return self.target_time.strftime("%#I:%M%p %A, %B %#d, %Y")