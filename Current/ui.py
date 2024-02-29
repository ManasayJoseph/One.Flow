import customtkinter
from tkinter import *
from customtkinter import *
from PIL import Image

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x100")
        self.overrideredirect(1)  # Make it borderless

        self.button = customtkinter.CTkButton(app,image=CTkImage(dark_image=Image.open("./public/wand.PNG"),size=(20,20)))
        self.button.pack(padx=20,pady=20)
        # self.label = customtkinter.CTkLabel(self, text="Window")
        # self.label.pack(padx=20, pady=20)


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
