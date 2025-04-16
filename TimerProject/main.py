import sys
import threading
import pystray
from PIL import Image
import data_display_gui
import timer_program
import time

def update_icon(icon, path):
    image = Image.open(path)
    icon.icon = image

def start_timer(icon, item):
    update_icon(icon, 'Assets/clock_active.png')
    print('Timer is running')

    def run_timer():
        timer_program.start_program()
        while not timer_program.stop_event.is_set():
            time.sleep(1)

    threading.Thread(target=run_timer, daemon=True).start()

def stop_timer(icon, item):
    update_icon(icon, 'Assets/clock.png')
    timer_program.stop_program()
    print('Timer is stopped')

def show_data():
    data_display_gui.run_app()
    print('Display data')

def exit_app(icon, item):
    timer_program.stop_program()
    icon.stop()
    sys.exit()

def run_main_app():
    image = Image.open('Assets/clock.png')
    menu = pystray.Menu(
        pystray.MenuItem('Start Timer', start_timer),
        pystray.MenuItem('Stop Timer', stop_timer),
        pystray.MenuItem('Show Data', show_data),
        pystray.MenuItem('Exit', exit_app),
    )

    icon = pystray.Icon('Time Tracker', image, menu=menu)
    icon.run_detached()

    threading.Thread(target=start_timer, args=(icon, None), daemon=True).start()

run_main_app()