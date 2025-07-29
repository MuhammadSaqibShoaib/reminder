import tkinter as tk
import winsound
import os
import time
import threading
import ctypes
import sys

# PyInstaller-compatible path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller bundle
    except AttributeError:
        base_path = os.path.abspath(".")  # For script
    return os.path.join(base_path, relative_path)

WAV_PATH = resource_path("beep.wav")


def is_screen_locked():
    return ctypes.windll.user32.GetForegroundWindow() == 0


def monitor_win_l():
    print("🟢 Monitoring for Win + L...")
    was_locked = False

    while True:
        locked = is_screen_locked()

        if locked and not was_locked:
            print("🔒 Screen locked — attempting to play sound")
            if os.path.exists(WAV_PATH):
                try:
                    winsound.PlaySound(WAV_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC)
                    print("🔊 Sound played")
                except RuntimeError as e:
                    print("⚠️ Failed to play sound:", e)
            else:
                print(f"❌ Sound file not found: {WAV_PATH}")
            was_locked = True

        elif not locked:
            was_locked = False

        time.sleep(0.1)


def start_monitoring(button):
    button.config(state="disabled", text="Monitoring...")
    threading.Thread(target=monitor_win_l, daemon=True).start()


def simple_gui():
    window = tk.Tk()
    window.title("Win+L Beep Reminder")
    window.geometry("300x120")
    window.resizable(False, False)

    label = tk.Label(window, text="Click Start, then press Win + L to test.")
    label.pack(pady=10)

    start_btn = tk.Button(window, text="Start Monitoring", command=lambda: start_monitoring(start_btn))
    start_btn.pack(pady=10)

    window.mainloop()


if __name__ == "__main__":
    simple_gui()
