import subprocess
import time
from pynput import keyboard as kb

stop = False

def on_press(key):
    global stop
    try:
        if key.char == 'q':
            stop = True
    except:
        pass

def get_active_window():
    script = 'tell application "System Events" to get name of first application process whose frontmost is true'
    result = subprocess.run(['osascript', '-e', script],
                           capture_output=True, text=True)
    return result.stdout.strip()

def get_chrome_url():
    script = '''
    tell application "Google Chrome"
        get URL of active tab of front window
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script],
                           capture_output=True, text=True)
    return result.stdout.strip()

def classify_activity():
    window = get_active_window().lower()
    try:
        url = get_chrome_url().lower()
    except:
        url = ""
    
    if "electron" in window:
        return "coding"
    elif "terminal" in window or "iterm" in window:
        return "coding"
    elif "pycharm" in window or "xcode" in window:
        return "coding"
    elif "youtube.com" in url:
        return "youtube"
    elif "instagram.com" in url or "x.com" in url:
        return "wasting"
    elif "netflix.com" in url or "primevideo.com" in url:
        return "wasting"
    elif "claude.ai" in url or "chatgpt.com" in url:
        return "studying"
    elif "gemini.google.com" in url or "grok.com" in url:
        return "studying"
    elif "colab.research.google.com" in url:
        return "coding"
    elif "github.com" in url:
        return "coding"
    elif "stackoverflow.com" in url:
        return "studying"
    else:
        return "browsing"

def current_activity():
    while not stop:
        activity = classify_activity()
        print(activity)
        time.sleep(10)
    print("Stopped")

listener = kb.Listener(on_press=on_press)
listener.start()
current_activity()