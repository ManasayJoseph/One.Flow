import customtkinter
from tkinter import *
from customtkinter import *
from PIL import Image


class ToplevelWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x400")
        self.overrideredirect(1)  # Make it borderless

        # Create a frame for each row of buttons
        top_frame = CTkFrame(self)
        top_frame.pack()
        bottom_frame = CTkFrame(self)
        bottom_frame.pack()

        # Create buttons with images and pack them in their respective frames
        image = CTkImage(dark_image=Image.open("./images/wand.png"), size=(30, 30))
        button = CTkButton(top_frame, image=image, width=90, height=90, text="")
        button.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/notes.png"), size=(30, 30))
        button = CTkButton(top_frame, image=image, width=90, height=90, text="")
        button.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/screenshare.png"), size=(30, 30))
        button = CTkButton(bottom_frame, image=image, width=90, height=90, text="")
        button.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/scripts.png"), size=(30, 30))
        button = CTkButton(bottom_frame, image=image, width=90, height=90, text="")
        button.pack(side="left", padx=5, pady=5)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("10x40+0+0")

        self.wm_attributes("-alpha", 0.5)
        self.overrideredirect(1)
        self.drag_data = {"y": 0}
        self.screen_height = self.winfo_screenheight()

        self.additional_window = None  # Initialize as None
        self.wm_attributes("-topmost", 1)
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<Button-1>", self.check_click_outside)  # Bind to all clicks
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

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
            self.additional_window = ToplevelWindow(self)
            self.additional_window.geometry(
                f"+{self.winfo_x() + self.winfo_width() + 20}+{self.winfo_y()}"
            )

    def check_click_outside(self, event):
        # Check if additional window exists and click is outside its bounds
        if self.additional_window and (
            event.x < self.winfo_x()
            or event.x > self.winfo_x() + self.winfo_width()
            or event.y < self.winfo_y()
            or event.y > self.winfo_y() + self.winfo_height()
        ):
            self.additional_window.destroy()
            self.additional_window = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
