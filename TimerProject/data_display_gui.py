from customtkinter import *
from CTkTable import *
import json
import webbrowser
from PIL import Image
import timer_program

def run_app():
    # App setup
    app = CTk()
    app.geometry('1280x720')
    app.title('WorkPulse - Time Tracker')
    app.iconbitmap('Assets/icon.ico')
    github = Image.open('Assets/github.png')

    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f'{hours}h : {minutes}m : {secs}s'

    def to_seconds(time_str):
        final_time = time_str.split(' : ')
        hours = int(final_time[0].replace('h', ''))
        minutes = int(final_time[1].replace('m', ''))
        seconds = int(final_time[2].replace('s', ''))
        return hours * 3600 + minutes * 60 + seconds

    def link():
        webbrowser.open('https://github.com/Woltek1')

    def clean_time_history():
        if os.path.exists(timer_program.json_path):
            timer_program.window_data = {}
            timer_program.save_data()

    def clear_history():
        popup = CTkToplevel(app)
        popup.geometry('400x300')
        popup.title('Clear timer history')

        popup.lift()
        popup.attributes('-topmost', True)

        text1 = CTkLabel(popup, text='Are you sure you want to clear timer history?', font=('Roboto', 16))
        text2 = CTkLabel(popup, text="There's no coming back!", font=('Roboto', 16))
        text1.pack(pady=25)
        text2.pack()

        buttons = CTkFrame(popup, width=300, fg_color='transparent')
        buttons.pack(pady=25)

        def confirm_action():
            clean_time_history()
            popup.destroy()

        cancel_btn = CTkButton(buttons, text='Cancel', fg_color='#ff0f0f', hover_color='#D0342C', font=('Roboto', 32), command=popup.destroy)
        confirm_btn = CTkButton(buttons, text='Confirm', fg_color='#00A53C', hover_color='#13CC4E', font=('Roboto', 32), command=confirm_action)
        cancel_btn.pack(side='left', pady=10, padx=10)
        confirm_btn.pack(side='right', pady=10, padx=10)

    with open('time_data.json', 'r') as f:
        data = json.load(f)
    arr = []
    for i, (app_name, time) in enumerate(data.items()):
        formated_time = format_time(time)
        arr.append([app_name, formated_time])
    arr_sorted = sorted(arr, key=lambda x: to_seconds(x[1]), reverse=True)


    label = CTkLabel(app, text='Dashboard', font=('Roboto', 32), text_color='#fafcf9')
    label.pack(pady=10)

    frame = CTkScrollableFrame(app, 500, 500, fg_color='transparent')
    frame.pack()

    table = CTkTable(frame, values=[['Application', 'Time spent']] + arr_sorted, font=('Roboto', 24))
    table.pack(fill='both', expand=True)

    btn_frame = CTkFrame(app, width=700, fg_color='transparent')
    btn_frame.pack(side='bottom')

    github_image = CTkImage(light_image=github, dark_image=github, size=(32, 32))
    button = CTkButton(btn_frame, text='My Github', image=github_image, fg_color='#163832', hover_color='#235347', command=link, font=('Roboto', 32))
    button.pack(padx=10, pady=10, side='left')

    clear_button = CTkButton(btn_frame, text='Clear timer history', fg_color='#ff0f0f', hover_color='#D0342C', font=('Roboto', 32), command=clear_history)
    clear_button.pack(padx=10, pady=10, side='right')

    app.mainloop()