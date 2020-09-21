import sys, os
import ctypes
from GlobalHotkeys import Global_Hotkeys
from tkinter import *
from tkinter import messagebox
import time
import threading
import base64
import keyboard
import pynput

SendInput = ctypes.windll.user32.SendInput
KEYBOARD_MAPPING = {
    'escape': 0x01,
    'esc': 0x01,
    'f1': 0x3B,
    'f2': 0x3C,
    'f3': 0x3D,
    'f4': 0x3E,
    'f5': 0x3F,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'f11': 0x57,
    'f12': 0x58,
    'printscreen': 0xB7,
    'prntscrn': 0xB7,
    'prtsc': 0xB7,
    'prtscr': 0xB7,
    'scrolllock': 0x46,
    'pause': 0xC5,
    '`': 0x29,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    '0': 0x0B,
    '-': 0x0C,
    '=': 0x0D,
    'backspace': 0x0E,
    'insert': 0xD2 + 1024,
    'home': 0xC7 + 1024,
    'pageup': 0xC9 + 1024,
    'pagedown': 0xD1 + 1024,
    # numpad
    'numlock': 0x45,
    'divide': 0xB5 + 1024,
    'multiply': 0x37,
    'subtract': 0x4A,
    'add': 0x4E,
    'decimal': 0x53,
    #KEY_NUMPAD_ENTER: 0x9C + 1024,
    #KEY_NUMPAD_1: 0x4F,
    #KEY_NUMPAD_2: 0x50,
    #KEY_NUMPAD_3: 0x51,
    #KEY_NUMPAD_4: 0x4B,
    #KEY_NUMPAD_5: 0x4C,
    #KEY_NUMPAD_6: 0x4D,
    #KEY_NUMPAD_7: 0x47,
    #KEY_NUMPAD_8: 0x48,
    #KEY_NUMPAD_9: 0x49,
    #KEY_NUMPAD_0: 0x52,
    # end numpad
    'tab': 0x0F,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '[': 0x1A,
    ']': 0x1B,
    '\\': 0x2B,
    'del': 0xD3 + 1024,
    'delete': 0xD3 + 1024,
    'end': 0xCF + 1024,
    'capslock': 0x3A,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    ';': 0x27,
    "'": 0x28,
    'enter': 0x1C,
    'return': 0x1C,
    'shift': 0x2A,
    'shiftleft': 0x2A,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    ',': 0x33,
    '.': 0x34,
    '/': 0x35,
    'shiftright': 0x36,
    'ctrl': 0x1D,
    'ctrlleft': 0x1D,
    'win': 0xDB + 1024,
    'winleft': 0xDB + 1024,
    'alt': 0x38,
    'altleft': 0x38,
    ' ': 0x39,
    'space': 0x39,
    'altright': 0xB8 + 1024,
    'winright': 0xDC + 1024,
    'apps': 0xDD + 1024,
    'ctrlright': 0x9D + 1024 }
def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

class cooldown:
    def __init__(self, timeout):
        self.timeout = timeout
        self.calltime = time.time() - timeout
        self.func = None
        self.obj = None
    def __call__(self, *args, **kwargs):
        if self.func is None:
            self.func = args[0]
            return self
        now = time.time()
        if now - self.calltime >= self.timeout:
            self.calltime = now
            if self.obj is None:
                return self.func.__call__(*args, **kwargs)
            else:
                return self.func.__get__(self.obj, self.objtype)(*args, **kwargs)
    def __get__(self, obj, objtype):
        self.obj = obj
        self.objtype = objtype
        return self
    @property
    def remaining(self):
        now = time.time()
        delta = now - self.calltime
        if delta >= self.timeout:
            return 0
        return self.timeout - delta
    @remaining.setter
    def remaining(self, value):
        self.calltime = time.time() - self.timeout + value


class EncryptText():

    @classmethod
    def xencode(cls, text):
        return str(base64.b64encode(text.encode()))[2:]
        
        
        

    @classmethod
    def xdecode(cls, text):
        return base64.b64decode(text).decode()


class ReadFile():
    CHATLINES = ["[Client thread/INFO]: [CHAT]", "[main/INFO]: [CHAT]"]
    filternames = []

    @classmethod
    def __init__(self):
        self.name = "namespace bro"
        logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
        loglines = self.follow(logfile)
        for line in loglines:
            if self.CHATLINES[0] in line:
                #print(line)
                if any(i for i in self.filternames if i in line):
                    print (line)
                    if line.find("117487") != -1:
                        line = line.split("117487")[1]
                        line = EncryptText.xdecode(text = line)
                        print(line)

    @classmethod
    def follow(self, thefile):
        thefile.seek(0,2)
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

class RootConfig():

    def __init__(self, root):
        self.root = root

        filter_name_entry = Entry(self.root)

threads = []

def send():
    time.sleep(0.5)
    PressKeyPynput(KEYBOARD_MAPPING["ctrl"])
    time.sleep(0.03)
    PressKeyPynput(KEYBOARD_MAPPING["a"])
    time.sleep(0.03)
    PressKeyPynput(KEYBOARD_MAPPING["x"])
    time.sleep(0.03)
    ReleaseKeyPynput(KEYBOARD_MAPPING["ctrl"])
    ReleaseKeyPynput(KEYBOARD_MAPPING["a"])
    ReleaseKeyPynput(KEYBOARD_MAPPING["x"])
    print(root.selection_get(selection = "CLIPBOARD"))
    encrypted = "117487" + EncryptText.xencode(text = root.selection_get(selection = "CLIPBOARD"))
    print(encrypted)
    root.clipboard_clear()
    root.clipboard_append(encrypted)
    root.update()
    time.sleep(0.03)
    PressKeyPynput(KEYBOARD_MAPPING["ctrl"])
    time.sleep(0.03)
    PressKeyPynput(KEYBOARD_MAPPING["v"])
    time.sleep(0.03)
    ReleaseKeyPynput(KEYBOARD_MAPPING["ctrl"])
    ReleaseKeyPynput(KEYBOARD_MAPPING["v"])

def encrypt_text():
    thread = threading.Thread(target = send)
    threads.append(thread)
    thread.start()
    for i in threads: 
        if not i.is_alive(): i.join()
    print('hotkey pressed')


if __name__ == "__main__":
    #keyboard.press_and_release("ctrl+a")
    #pydirectinput.press("a")
    
    root = Tk()
    chat = ReadFile
    threading.Thread(target = chat, args = (), daemon = False).start()
    chat.filternames.append("firekitty")
    
    Global_Hotkeys.create_hotkey(root.winfo_id(), 0, ["<ctrl>", "<alt>"], "e", encrypt_text)
    root.mainloop()