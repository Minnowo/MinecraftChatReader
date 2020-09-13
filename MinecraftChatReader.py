import PIL 
import pytesseract
import sys, os
import ctypes
from GlobalHotkeys import Global_Hotkeys
from screeninfo import get_monitors
from desktopmagic.screengrab_win32 import getRectAsImage, getDisplaysAsImages
from tkinter import *
from tkinter import messagebox
import time

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

class ScanChat():

    def __init__(self, root):
        self.root = root
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.dragbox = None
        self.monitorid = None

        self.picture_rect = [0, 0, 0, 0]

        # Create hotkeys 
        self.select_scan_area = Global_Hotkeys.create_hotkey(self.root.winfo_id(), 0, ["<ctrl>", "<alt>"], "z", self.CreateClippingWindow)
        self.scan_chat =        Global_Hotkeys.create_hotkey(self.root.winfo_id(), 1, ["<ctrl>", "<alt>"], "x", self.TakePictureOfChat)
        print(self.select_scan_area)
        print(self.scan_chat)

        # Hide root window 
        root.attributes("-alpha", 0)
        root.attributes("-topmost", "true")
        root.withdraw()


    #***************** Chat scan functions *************. 

    @cooldown(0.5)
    def TakePictureOfChat(self):   
        print("picture taken")
        try:
            chat_image = getRectAsImage((self.picture_rect))
            pytesseract.pytesseract.tesseract_cmd = '{}\\tess_folder\\tesseract.exe'.format(os.getcwd())
            image_text = pytesseract.image_to_string(chat_image, lang='eng', config= "--psm 1")
            self.root.clipboard_clear()
            self.root.clipboard_append(image_text)
            print(image_text.encode("unicode-escape"))
            self.root.after(10, lambda title = "OCR-Output", message = image_text, parent = self.root : self.ShowMsgBox(title, message, parent))
        except Exception as e: 
            self.root.after(10, lambda title = "Error", message = f"error with ocr:\n {e}", parent = self.root : self.ShowMsgBox(title, message, parent))

    def ShowMsgBox(self, title, message, parent = None):
        if parent:
            messagebox.showinfo(title=title, message=message, parent=parent)
        else:
            messagebox.showinfo(title=title, message=message)


    #***************** Tkinter clipping window / other functions *************.
    
    def CreateClippingWindow(self):
        self.DestroyToplevel("clipping_window", match = False)

        self.monitors = get_monitors()
        for index, monitor in enumerate(self.monitors):
            print(index, monitor)
            monx = int(monitor.x); mony = int(monitor.y); monwidth = int(monitor.width); monheight = int(monitor.height)

            clip_window_master = Toplevel(self.root)
            clip_window_master.title(f"clipping_window_{index}")
            clip_window_master.minsize(monwidth, monheight)
            clip_window_master.geometry(f"+{monx + 1}+{mony}")
            clip_window_master.attributes("-transparent", "blue")
            clip_window_master.attributes("-alpha", 0.3)            
            clip_window_master.overrideredirect(1)
            clip_window_master.state("zoomed")
            clip_window_master.attributes("-topmost", True)
            clip_window_master.deiconify()

            clip_canvas = Canvas(clip_window_master, bg="grey11", highlightthickness = 0)
            clip_canvas.pack(fill = BOTH, expand = True)

            clip_canvas.bind("<ButtonRelease-3>", self.OnRightClick)
            clip_canvas.bind("<ButtonPress-1>", self.OnLeftClick)
            clip_canvas.bind("<B1-Motion>", self.OnDrag)
            clip_canvas.bind("<ButtonRelease-1>", self.OnRelease)

            clip_window_master.lift()
            clip_window_master.update()

    def OnRightClick(self, event):
        event.widget.delete(self.dragbox)
        self.dragbox = None
        self.DestroyToplevel("clipping_window", match = False)

    def OnLeftClick(self, event):
        self.start_x = event.widget.canvasx(event.x)
        self.start_y = event.widget.canvasy(event.y)
        self.monitorid = ctypes.windll.user32.MonitorFromPoint(int(self.root.winfo_pointerx()), int(self.root.winfo_pointery()), 2)
        self.dragbox = event.widget.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=1, fill="blue")

    def OnDrag(self, event):
        self.end_x, self.end_y = (event.x, event.y)
        event.widget.coords(self.dragbox, self.start_x, self.start_y, self.end_x, self.end_y)

    def OnRelease(self, event):
        monitor_ids = {} 
        for i in get_monitors(): monitor_ids[ctypes.windll.user32.MonitorFromPoint(i.x, i.y, 2)] = i

        event.widget.delete(self.dragbox)
        self.dragbox = None
        self.DestroyToplevel("clipping_window", match = False)

        if self.start_x <= self.end_x and self.start_y <= self.end_y:   x1, y1, x2, y2 = (self.start_x, self.start_y, self.end_x, self.end_y) # Right Down
        elif self.start_x >= self.end_x and self.start_y <= self.end_y: x1, y1, x2, y2 = (self.end_x, self.start_y, self.start_x, self.end_y)  # Left Down
        elif self.start_x <= self.end_x and self.start_y >= self.end_y: x1, y1, x2, y2 = (self.start_x, self.end_y, self.end_x, self.start_y) # Right Up 
        elif self.start_x >= self.end_x and self.start_y >= self.end_y: x1, y1, x2, y2 = (self.end_x, self.end_y, self.start_x, self.start_y) # Left Up
        monitor = monitor_ids[self.monitorid] 
        for index, i in enumerate([int(self.start_x + monitor.x), int(self.start_y + monitor.y), int(self.end_x + monitor.x), int(self.end_y + monitor.y)]):
            self.picture_rect[index] = i
        print(self.picture_rect)

    def DestroyToplevel(self, specific_title_only = None, match = True):
        if specific_title_only:
            for widget in self.root.winfo_children():
                if isinstance(widget, Toplevel):
                    if match and widget.title() == specific_title_only: widget.destroy()
                    elif not match and widget.title().find(specific_title_only) != -1: widget.destroy()
        else:
            for widget in self.root.winfo_children():
                if isinstance(widget, Toplevel):
                    widget.destroy()



if __name__ == "__main__":
    #***************** Set process DPI aware for all monitors *************. 
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(ctypes.c_int()))
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
    success = ctypes.windll.user32.SetProcessDPIAware()

    root = Tk()
    chat = ScanChat(root)
    root.mainloop()