import tkinter as tk
from tkinter import messagebox
import winsound
import ctypes
import os
import sys

import win32con
import win32gui
import win32ts
import win32api

# Constants
WM_WTSSESSION_CHANGE = 0x02B1
WTS_SESSION_LOCK = 0x7
WTS_SESSION_UNLOCK = 0x8

# Path to sound file
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

SOUND_FILE = resource_path("beep.wav")


class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder")
        self.root.geometry("300x100")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="Click Start to enable reminder")
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_reminder)
        self.start_button.pack()

        self.hwnd = None

        self.root.after(100, self.setup_window_message_hook)

    def setup_window_message_hook(self):
        self.hwnd = self.get_hwnd()
        if self.hwnd:
            win32ts.WTSRegisterSessionNotification(self.hwnd, win32ts.NOTIFY_FOR_THIS_SESSION)
        else:
            messagebox.showerror("Error", "Could not register session notification.")

    def get_hwnd(self):
        # Get HWND from the tkinter window
        root_window_title = self.root.title()
        hwnd = win32gui.FindWindow(None, root_window_title)
        return hwnd

    def start_reminder(self):
        self.label.config(text="Reminder is running...")
        self.start_button.config(state=tk.DISABLED)

        # Set a custom window procedure to intercept Windows messages
        GWL_WNDPROC = -4
        self.old_proc = win32gui.SetWindowLong(self.hwnd, GWL_WNDPROC, self.window_proc)

    def window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_WTSSESSION_CHANGE:
            if wparam == WTS_SESSION_LOCK:
                self.play_beep()
        return win32gui.CallWindowProc(self.old_proc, hwnd, msg, wparam, lparam)

    def play_beep(self):
        if os.path.exists(SOUND_FILE):
            winsound.PlaySound(SOUND_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            print("Sound file not found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
