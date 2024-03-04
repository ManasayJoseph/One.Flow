import socket 
import threading
import customtkinter
from customtkinter import *
from PIL import Image
import pyperclip

import client_helper

HOST = 'localhost'  # Replace with the server's IP address if needed
PORT = 5000


class AdditionalWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x400")
        self.overrideredirect(1) # Make it borderless
        self.wm_attributes("-topmost", 1)
        # Create a frame for each row of buttons
        self.top_frame = CTkFrame(self)
        self.top_frame.pack()
        self.bottom_frame = CTkFrame(self)
        self.bottom_frame.pack()

        # Create buttons with images and pack them in their respective frames
        image = CTkImage(dark_image=Image.open("./images/wand.png"), size=(30, 30))
        wand = CTkButton(self.top_frame, image=image, width=90, height=90, text="" , command=self.wand)
        wand.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/notes.png"), size=(30, 30))
        notes = CTkButton(self.top_frame, image=image, width=90, height=90, text="",command=self.note)
        notes.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/screenshare.png"), size=(30, 30))
        share = CTkButton(self.bottom_frame, image=image, width=90, height=90, text="",command=self.share)
        share.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/sync.png"), size=(30, 30))
        clip = CTkButton(self.bottom_frame, image=image, width=90, height=90, text="",command=self.Sync_Clipboard)
        clip.pack(side="left", padx=5, pady=5)

    def Sync_Clipboard(self):
        clipboard = pyperclip.paste()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5000))
            s.sendall(clipboard.encode())



    def note(self):
        print("Note button CLicked")
        
    def share(self):
        print("Share button CLicked")
        
    def wand(self):
        print("wand button CLicked")
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("10x40+0+0")
        self.wm_attributes("-alpha", 0.5)
        self.overrideredirect(1)
        self.drag_data = {"y": 0}
        self.screen_height = self.winfo_screenheight()

        self.additional_window = None # Initialize as None
        self.wm_attributes("-topmost", 1)
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<Button-1>", self.check_click_outside) # Bind to all clicks
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.server_thread = threading.Thread(target=self.receive_from_server)
        self.server_thread.start()

    def create_popup(self):
        
        popup = CTkToplevel(self)
        # Adjust size as needed
        popup.geometry("80x80")
        popup.overrideredirect(1)
        # popup.wm_attributes("-topmost", 1)


        image = CTkImage(dark_image=Image.open("./images/sync.png"), size=(60, 60))
        label = CTkLabel(popup, text="",image=image)
        label.pack(padx=5,pady=5)



        # Schedule popup destruction after 5 seconds using after
        popup.after(5000, popup.destroy)

        # Get the geometry of the main app window
        size , app_x , app_y = self.geometry().split("+")

        app_x = int(app_x)
        app_y = int(app_y)

        # Position the popup to the left of the app window
        popup_geometry = f"{app_x + 30}+{app_y}"  # Adjust margin as needed
        popup.geometry(popup_geometry)

    def receive_from_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5000))
            while True:
                data = s.recv(1024)
                if data:
                    pyperclip.copy(data.decode())
                    self.create_popup()  # Create popup when data is received

    def on_enter(self, event):
        self.wm_attributes("-alpha", 0.8)

    def on_leave(self, event):
        self.wm_attributes("-alpha", 0.5)

    def start_drag(self, event):
        self.drag_data["y"] = event.y_root

    def drag(self, event):
        new_y = self.winfo_y() + (event.y_root - self.drag_data["y"])
        if new_y < 0:
            new_y = 0
        elif new_y > self.screen_height - self.winfo_height():
            new_y = self.screen_height - self.winfo_height()
        self.geometry(f"+{self.winfo_x()}+{new_y}")
        self.drag_data["y"] = event.y_root

        # Check if the drag ends on the right side
        if event.x_root > self.winfo_x() + self.winfo_width():
            self.create_window()

    def stop_drag(self, event):
        pass

    def create_window(self):
        if self.additional_window is None:
            self.additional_window = AdditionalWindow(self)
            self.additional_window.geometry(
                f"+{self.winfo_x() + self.winfo_width() + 20}+{self.winfo_y()}"
            )
            

    def check_click_outside(self, event):
    # Check if additional window exists and click is outside its bounds
        print("Here")
        if self.additional_window and (
        event.x < self.winfo_x()
        or event.x > self.winfo_x() + self.winfo_width()
        or event.y < self.winfo_y()
        or event.y > self.winfo_y() + self.winfo_height()
        ):
            print("adfasdfasdfsafasdfasdfsfad")
            self.additional_window.destroy()
            self.additional_window = None

if __name__ == "__main__":
  app = App()
  app.mainloop()
