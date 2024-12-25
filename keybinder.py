import threading
import keyboard
import win32gui
import json
import time

chatOpen = False
foreground_window_name = ""

keybinds = [] 

def is_gta_san_andreas_foreground():
    """Check if the current foreground window belongs to GTA SA."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        window_text = win32gui.GetWindowText(hwnd)
        return "GTA" in window_text or "San Andreas" in window_text
    return False

def on_key_event(event):
    global chatOpen

    if not is_gta_san_andreas_foreground():
        return 

    if event.name == 't':
        chatOpen = True

    if event.name in ['enter', 'esc']:
        chatOpen = False

    if not chatOpen:
        for kb in keybinds:
            if kb["enabled"] and kb["key"].lower() == event.name.lower():
                send_text(kb["text"])
                break

def send_text(text):
    keyboard.press_and_release('t')
    #time.sleep(0.05)
    keyboard.write(text)
    keyboard.press_and_release('enter')

def setup_hook():
    """
    Set up the keyboard hook in a background thread so it doesn't block the main UI.
    """
    keyboard.on_press(on_key_event)
    thread = threading.Thread(target=keyboard.wait, daemon=True)
    thread.start()

def set_keybinds(new_keybinds):
    """Used by the GUI to update the in-memory keybinds."""
    global keybinds
    keybinds = new_keybinds
