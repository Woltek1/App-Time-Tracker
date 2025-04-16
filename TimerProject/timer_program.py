import win32gui
import win32process
import psutil
import time
import json
import os
import threading
from threading import Event
from pynput import mouse, keyboard

is_active = Event()
stop_event = Event()
json_path = 'time_data.json'
is_active.set()

last_activity_time = time.time()
inactive_time_limit = 3

if os.path.exists(json_path):
    with open(json_path, 'r') as f:
        window_data = json.load(f)
else:
    window_data = {}

def save_data():
    with open(json_path, 'w') as f:
        json.dump(window_data, f, indent=4)

def timer_mechanics():
    global window_data
    last_time = time.perf_counter()
    remainder = 0.0
    was_active = is_active.is_set()

    while not stop_event.is_set():
        now_active = is_active.is_set()
        if now_active and not was_active:
            last_time = time.perf_counter()
            remainder = 0.0
        was_active = now_active

        if now_active:
            current_time = time.perf_counter()
            elapsed = current_time - last_time
            last_time = current_time
            elapsed += remainder
            whole_seconds = int(elapsed)
            remainder = elapsed - whole_seconds

            if whole_seconds > 0:
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)

                try:
                    process = psutil.Process(pid).name().replace('.exe', '').capitalize()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

                if process not in window_data:
                    window_data[process] = 0
                window_data[process] += whole_seconds

                print(window_data)
                save_data()
        time.sleep(0.1)

def on_move(x, y):
    global last_activity_time
    last_activity_time = time.time()
    if not is_active.is_set():
        is_active.set()
        print('Timer resumed')

def on_click(s, y, button, pressed):
    global last_activity_time
    last_activity_time = time.time()
    if not is_active.is_set():
        is_active.set()
        print('Timer resumed')

def on_key_press(key):
    global last_activity_time
    last_activity_time = time.time()
    if not is_active.is_set():
        is_active.set()
        print('Timer resumed')

def mouse_listener():
    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        while not stop_event.is_set():
            time.sleep(0.1)
        listener.stop()

def keyboard_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        while not stop_event.is_set():
            time.sleep(0.1)
        listener.stop()

def get_active_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid).name().lower()
        return process
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return ""

def monitor_inactivity():
    global last_activity_time
    browser_names = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'opera.exe', 'brave.exe']

    while not stop_event.is_set():
        current_process = get_active_process_name()

        if current_process in browser_names:
            time.sleep(1)
            continue

        if is_active.is_set() and (time.time() - last_activity_time > inactive_time_limit):
            is_active.clear()
            print('Timer paused')
        time.sleep(1)

def start_program():
    stop_event.clear()
    is_active.set()

    threading.Thread(target=timer_mechanics, daemon=True).start()
    threading.Thread(target=monitor_inactivity, daemon=True).start()
    threading.Thread(target=mouse_listener, daemon=True).start()
    threading.Thread(target=keyboard_listener, daemon=True).start()

def stop_program():
    stop_event.set()
    is_active.clear()
    print("Timer stopped.")