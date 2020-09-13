import PIL 
import pytesseract
from desktopmagic.screengrab_win32 import getRectAsImage, getDisplaysAsImages
from tkinter import *


class Global_Hotkeys:
    import ctypes
    import pynput.keyboard
    MODIFIER_KEYS_INT = {"<cmd>" : 0x0008,  "<shift>" : 0x0004,    "<alt>" : 0x0001,  "<ctrl>" : 0x0002, "" : 0x0000}
    PYNPUT_TO_VK = {'<scroll_lock>' : 0x91,'<num_lock>' : 0x90,'<menu>' : 0xa5,'<page_up>' : 0x21,'<page_down>' : 0x22,'0' : 0x30,'1' : 0x31,'2' : 0x32,'3' : 0x33,'4' : 0x34,'5' : 0x35,'6' : 0x36,'7' : 0x37,'8' : 0x38,'9' : 0x39,'a' : 0x41,'b' : 0x42,'c' : 0x43,'d' : 0x44,'e' : 0x45,'f' : 0x46,'g' : 0x47,'h' : 0x48,'i' : 0x49,'j' : 0x4a,'k' : 0x4b,'l' : 0x4c,'m' : 0x4d,'n' : 0x4e,'o' : 0x4f,'p' : 0x50,'q' : 0x51,'r' : 0x52,'s' : 0x53,'t' : 0x54,'u' : 0x55,'v' : 0x56,'w' : 0x57,'x' : 0x58,'y' : 0x59,'z' : 0x5a,'<backspace>' : 0x8,'<tab>' : 0x9,'<clear>' : 0xc,'<enter>' : 0xd,'<shift>' : 0x10,'<control>' : 0x11,'<alt>' : 0x12,'<pause>' : 0x13,'<caps_lock>' : 0x14,'<esc>' : 0x1b,'<space>' : 0x20,'<end>' : 0x23,'<home>' : 0x24,'<left>' : 0x25,'<up>' : 0x26,'<right>' : 0x27,'<down>' : 0x28,'<select>' : 0x29,'<print>' : 0x2a,'<execute>' : 0x2b,'<print_screen>' : 0x2c,'<insert>' : 0x2d,'<delete>' : 0x2e,'<help>' : 0x2f,'<f1>' : 0x70,'<f2>' : 0x71,'<f3>' : 0x72,'<f4>' : 0x73,'<f5>' : 0x74,'<f6>' : 0x75,'<f7>' : 0x76,'<f8>' : 0x77,'<f9>' : 0x78,'<f10>' : 0x79,'<f11>' : 0x7a,'<f12>' : 0x7b,'<f13>' : 0x7c,'<f14>' : 0x7d,'<f15>' : 0x7e,'<f16>' : 0x7f,'<f17>' : 0x80,'<f18>' : 0x81,'<f19>' : 0x82,'<f20>' : 0x83}
    REGISTER_HOTKEY_WINDLL = ctypes.windll.user32.RegisterHotKey
    UNREGISTER_HOTKEY_WINDLL = ctypes.windll.user32.UnregisterHotKey
    REGISTER_HOTKEY_PYNPUT =  pynput.keyboard.GlobalHotKeys
    UNREGISTER_HOTKEY_PYNPUT = pynput.keyboard.GlobalHotKeys.stop


    @classmethod
    def create_hotkey(cls, hwnd : int, hotkey_id : int, modifier_keys : list, activate_key : int, callback, *args):
        """creates a blocking hotkey (Windows key modifier not blocked)\nhotkey_id must be int \nmodifier_keys should be any in [MOD_WINDOWS, MOD_SHIFT, MOD_ALT, MOD_CONTROL, NONE] \nactivate_key should be string"""
        activate_key = activate_key.lower()
        if cls.PYNPUT_TO_VK[activate_key]:
            modifier_int = 0; modifier_str = []
            for x, i in enumerate(modifier_keys):
                if i in cls.MODIFIER_KEYS_INT.keys():
                    modifier_int += cls.MODIFIER_KEYS_INT[i]
                    modifier_str.append(i) #if x != len(modifier_keys) -1 else i
                else: raise Exception(f"{i} is not in the modifier_key dictionary {cls.MODIFIER_KEYS_INT.keys()}")
            modifier_str = "+".join(modifier_str) + "+" if "+".join(modifier_str) != "" else ""
            windll_hotkey = cls.REGISTER_HOTKEY_WINDLL(hwnd, int(hotkey_id), modifier_int, cls.PYNPUT_TO_VK[activate_key])
            pynput_hotkey = cls.REGISTER_HOTKEY_PYNPUT({f"{modifier_str}{activate_key}" : lambda args = args: callback(args)}) if args != () else cls.REGISTER_HOTKEY_PYNPUT({f"{modifier_str}{activate_key}" : callback}); pynput_hotkey.start()
            return (pynput_hotkey, windll_hotkey, f"{modifier_str}{activate_key}", hotkey_id)

    @classmethod
    def remove_hotkey(cls, hwnd : int, hotkey_id : int, create_hotkey_return_object : object):
        """remove the hotkeys made"""
        windll_hotkey=cls.UNREGISTER_HOTKEY_WINDLL(hwnd, hotkey_id)
        pynput_hotkey = cls.UNREGISTER_HOTKEY_PYNPUT(create_hotkey_return_object)

        
    @classmethod
    def return_vk_detail(cls):
        data = b"VK_OEM_CLEAR : 0xFE, Clear key\\nVK_PA1 : 0xFD, PA1 key\\nVK_NONAME : 0xFC, Reserved\\nVK_ZOOM : 0xFB, Zoom key\\nVK_PLAY : 0xFA, Play key\\nVK_EREOF : 0xF9, Erase EOF key\\nVK_EXSEL : 0xF8, ExSel key\\nVK_CRSEL : 0xF7, CrSel key\\nVK_ATTN : 0xF6, Attn key\\n0xE9-F5 : OEM, specific\\n- : 0xE8, Unassigned\\nVK_PACKET : 0xE7, Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT, SendInput, WM_KEYDOWN, and WM_KEYUP\\n0xE6 : OEM, specific\\nVK_PROCESSKEY : 0xE5, IME PROCESS key\\n0xE3-E4 : OEM, specific\\nVK_OEM_102 : 0xE2, Either the angle bracket key or the backslash key on the RT 102-key keyboard\\n0xE1 : OEM, specific\\n- : 0xE0, Reserved\\nVK_OEM_8 : 0xDF, Used for miscellaneous characters; it can vary by keyboard.\\nVK_OEM_7 : 0xDE,  For the US standard keyboard, the 'single-quote/double-quote' key\\nVK_OEM_6 : 0xDD, Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ']}' key\\nVK_OEM_5 : 0xDC, Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '\\\\|' key\\nVK_OEM_4 : 0xDB, Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key\\n- : 0xD8-DA, Unassigned\\n- : 0xC1-D7, Reserved\\nVK_OEM_3 : 0xC0, Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '`~' key\\nVK_OEM_2 : 0xBF, Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key\\nVK_OEM_PERIOD : 0xBE, For any country/region, the '.' key\\nVK_OEM_MINUS : 0xBD, For any country/region, the '-' key\\nVK_OEM_COMMA : 0xBC, For any country/region, the ',' key\\nVK_OEM_PLUS : 0xBB, For any country/region, the '+' key\\nVK_OEM_1 : 0xBA, Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key\\n- : 0xB8-B9, Reserved\\nVK_LAUNCH_APP2 : 0xB7, Start Application 2 key\\nVK_LAUNCH_APP1 : 0xB6, Start Application 1 key\\nVK_LAUNCH_MEDIA_SELECT : 0xB5, Select Media key\\nVK_LAUNCH_MAIL : 0xB4, Start Mail key\\nVK_MEDIA_PLAY_PAUSE : 0xB3, Play/Pause Media key\\nVK_MEDIA_STOP : 0xB2, Stop Media key\\nVK_MEDIA_PREV_TRACK : 0xB1, Previous Track key\\nVK_MEDIA_NEXT_TRACK : 0xB0, Next Track key\\nVK_VOLUME_UP : 0xAF, Volume Up key\\nVK_VOLUME_DOWN : 0xAE, Volume Down key\\nVK_VOLUME_MUTE : 0xAD, Volume Mute key\\nVK_BROWSER_HOME : 0xAC, Browser Start and Home key\\nVK_BROWSER_FAVORITES : 0xAB, Browser Favorites key\\nVK_BROWSER_SEARCH : 0xAA, Browser Search key\\nVK_BROWSER_STOP : 0xA9, Browser Stop key\\nVK_BROWSER_REFRESH : 0xA8, Browser Refresh key\\nVK_BROWSER_FORWARD : 0xA7, Browser Forward key\\nVK_BROWSER_BACK : 0xA6, Browser Back key\\nVK_RMENU : 0xA5, Right MENU key\\nVK_LMENU : 0xA4, Left MENU key\\nVK_RCONTROL : 0xA3, Right CONTROL key\\nVK_LCONTROL : 0xA2, Left CONTROL key\\nVK_RSHIFT : 0xA1, Right SHIFT key\\nVK_LSHIFT : 0xA0, Left SHIFT key\\n0x97-9F : Unassigned, \\n0x92-96 : OEM, specific -\\nVK_SCROLL : 0x91, SCROLL LOCK key\\nVK_NUMLOCK : 0x90, NUM LOCK key\\n- : 0x88-8F, Unassigned\\nVK_F24 : 0x87, F24 key\\nVK_F230x86 : F23, key\\nVK_F22 : 0x85, F22 key\\nVK_F21 : 0x84, F21 key\\nVK_F20 : 0x83, F20 key\\nVK_F19 : 0x82, F19 key\\nVK_F18 : 0x81, F18 key\\nVK_F17 : 0x80, F17 key\\nVK_F16 : 0x7F, F16 key\\nVK_F15 : 0x7E, F15 key\\nVK_F14 : 0x7D, F14 key\\nVK_F13 : 0x7C, F13 key\\nVK_F12 : 0x7B, F12 key\\nVK_F11 : 0x7A, F11 key\\nVK_F10 : 0x79, F10 key\\nVK_F9 : 0x78, F9 key\\nVK_F8 : 0x77, F8 key\\nVK_F7 : 0x76, F7 key\\nVK_F6 : 0x75, F6 key\\nVK_F5 : 0x74, F5 key\\nVK_F4 : 0x73, F4 key\\nVK_F3 : 0x72, F3 key\\nVK_F2 : 0x71, F2 key\\nVK_F1 : 0x70, F1 key\\nVK_DIVIDE : 0x6F, Divide key\\nVK_DECIMAL : 0x6E, Decimal key\\nVK_SUBTRACT : 0x6D, Subtract key\\nVK_SEPARATOR : 0x6C, Separator key\\nVK_ADD : 0x6B, Add key\\nVK_MULTIPLY : 0x6A, Multiply key\\nVK_NUMPAD9 : 0x69, Numeric keypad 9 key\\nVK_NUMPAD8 : 0x68, Numeric keypad 8 key\\nVK_NUMPAD7 : 0x67, Numeric keypad 7 key\\nVK_NUMPAD6 : 0x66, Numeric keypad 6 key\\nVK_NUMPAD5 : 0x65, Numeric keypad 5 key\\nVK_NUMPAD4 : 0x64, Numeric keypad 4 key\\nVK_NUMPAD3 : 0x63, Numeric keypad 3 key\\nVK_NUMPAD2 : 0x62, Numeric keypad 2 key\\nVK_NUMPAD1 : 0x61, Numeric keypad 1 key\\nVK_NUMPAD0 : 0x60, Numeric keypad 0 key\\nVK_SLEEP : 0x5F, Computer Sleep key\\n- : 0x5E, Reserved\\nVK_APPS : 0x5D, Applications key (Natural keyboard)\\nVK_RWIN : 0x5C, Right Windows key (Natural keyboard)\\nVK_LWIN : 0x5B, Left Windows key (Natural keyboard)\\n0x5A : Z, key\\n0x59 : Y, key\\n0x58 : X, key\\n0x57 : W, key\\n0x56 : V, key\\n0x55 : U, key\\n0x54 : T, key\\n0x53 : S, key\\n0x52 : R, key\\n0x51 : Q, key\\n0x50 : P, key\\n0x4F : O, key\\n0x4E : N, key\\n0x4D : M, key\\n0x4C : L, key\\n0x4B : K, key\\n0x4A : J, key\\n0x49 : I, key\\n0x48 : H, key\\n0x47 : G, key\\n0x46 : F, key\\n0x45 : E, key\\n0x44 : D, key\\n0x43 : C, key\\n0x42 : B, key\\n0x41 : A, key\\n- : 0x3A-40, Undefined\\n0x39 : 9, key\\n0x38 : 8, key\\n0x37 : 7, key\\n0x36 : 6, key\\n0x35 : 5, key\\n0x34 : 4, key\\n0x33 : 3, key\\n0x32 : 2, key\\n0x31 : 1, key\\n0x30 : 0, key\\nVK_HELP : 0x2F, HELP key\\nVK_DELETE : 0x2E, DEL key\\nVK_INSERT : 0x2D, INS key\\nVK_SNAPSHOT : 0x2C, PRINT SCREEN key\\nVK_EXECUTE : 0x2B, EXECUTE key\\nVK_PRINT : 0x2A, PRINT key\\nVK_SELECT : 0x29, SELECT key\\nVK_DOWN : 0x28, DOWN ARROW key\\nVK_RIGHT : 0x27, RIGHT ARROW key\\nVK_UP : 0x26, UP ARROW key\\nVK_LEFT : 0x25, LEFT ARROW key\\nVK_HOME : 0x24, HOME key\\nVK_END : 0x23, END key\\nVK_NEXT : 0x22, PAGE DOWN key\\nVK_PRIOR : 0x21, PAGE UP key\\nVK_SPACE : 0x20, SPACEBAR\\nVK_MODECHANGE : 0x1F, IME mode change request\\nVK_ACCEPT : 0x1E, IME accept\\nVK_NONCONVERT : 0x1D, IME nonconvert\\nVK_CONVERT : 0x1C, IME convert\\nVK_ESCAPE : 0x1B, ESC key\\nVK_IME_OFF : 0x1A, IME Off\\nVK_KANJI : 0x19, IME Kanji mode\\nVK_HANJA : 0x19, IME Hanja mode\\nVK_FINAL : 0x18, IME final mode\\nVK_JUNJA : 0x17, IME Junja mode\\nVK_IME_ON : 0x16, IME On\\nVK_HANGUL : 0x15, IME Hangul mode\\nVK_HANGUEL : 0x15, IME Hanguel mode (maintained for compatibility; use VK_HANGUL)\\nVK_KANA : 0x15, IME Kana mode\\nVK_CAPITAL : 0x14, CAPS LOCK key\\nVK_PAUSE : 0x13, PAUSE key\\nVK_MENU : 0x12, ALT key\\nVK_CONTROL : 0x11, CTRL key\\nVK_SHIFT : 0x10, SHIFT key\\n- : 0x0E-0F, Undefined\\nVK_RETURN : 0x0D, ENTER key\\nVK_CLEAR : 0x0C, CLEAR key\\n- : 0x0A-0B, Reserved\\nVK_TAB : 0x09, TAB key\\nVK_BACK : 0x08, BACKSPACE key\\n- : 0x07, Undefined\\nVK_XBUTTON2 : 0x06, X2 mouse button\\nVK_XBUTTON1 : 0x05, X1 mouse button\\nVK_MBUTTON : 0x04, Middle mouse button (three-button mouse)\\nVK_CANCEL : 0x03, Control-break processing\\nVK_RBUTTON : 0x02, Right mouse button\\nVK_LBUTTON : 0x01, Left mouse button"
        return data.decode("unicode-escape")


class ScanChat():

    def __init__(self):
        pass


    def SelectPictureArea(self):
        pass

    def TakePictureOfChat(self):
        pass


if __name__ == "__main__":
    chat = ScanChat()
    root = Tk()
    root.mainloop()