import configparser
from bot import Bot
import threading
import sqlite3
import multiprocessing

# Initialize SQLite database
conn = sqlite3.connect('booking.db')
conn.execute('''CREATE TABLE IF NOT EXISTS locks (resource TEXT PRIMARY KEY)''')
conn.commit()

lock = threading.Lock()

if __name__ == '__main__':
    # Parse the config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    target_date = calc_target_date()
    # list of processes for mulitprocessing
    processes = []

    # Loop through the sections
    for i, chunk in enumerate(config.sections()):
        email = config[chunk]['email']
        password = config[chunk]['password']
        start_time = config[chunk]['start_time']

        bot = Bot(i, email, password, start_time, target_date, conn, lock)

        process = multiprocessing.Process(target=bot.run)
        processes.append(process)
        process.start()

    # wait for all processes to finish
    for process in processes:
        process.join()