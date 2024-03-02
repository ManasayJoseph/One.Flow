from tkinter import *
from tkinter import ttk  # Import themed Tkinter

class MovableWindow:
    def __init__(self, root):
        self.root = root
        self.root.geometry('10x40')
        self.root.overrideredirect(1)

        # Set window attributes
        self.root.wm_attributes('-alpha', 0.9)
        self.root.wm_attributes('-transparentcolor', 'white')

        # Make the window stay on top of other windows
        self.root.wm_attributes("-topmost", 1)

        # Initialize variables for dragging
        self.drag_data = {'y': 0}

        # Get the screen height
        self.screen_height = self.root.winfo_screenheight()

        # Flag to check if additional window is open
        self.additional_window_open = False

        # Bind mouse events for dragging
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)

        # Bind mouse click event to show or hide additional window
        self.root.bind("<Button-1>", self.toggle_additional_window)

    def start_drag(self, event):
        self.drag_data['y'] = event.y_root

    def drag(self, event):

        new_y = self.root.winfo_y() + (event.y_root - self.drag_data['y'])
        
        # Ensure the window stays within the screen bounds
        if new_y < 0:
            new_y = 0
        elif new_y > self.screen_height - self.root.winfo_height():
            new_y = self.screen_height - self.root.winfo_height()
        
        self.root.geometry(f'+{self.root.winfo_x()}+{new_y}')
        self.drag_data['y'] = event.y_root

        # Check if the drag is happening on the right side
        if event.x_root > self.root.winfo_x() + self.root.winfo_width():
            self.show_additional_window()
        else:
            self.hide_additional_window()

    def stop_drag(self, event):
        pass

    def toggle_additional_window(self, event):
        # Toggle additional window only if the click is on the right side
        if event.x > self.root.winfo_x() + self.root.winfo_width():
            if not self.additional_window_open:
                self.show_additional_window()
            else:
                self.hide_additional_window()

    def show_additional_window(self):
        if not self.additional_window_open:
            # Create and configure the additional window
            self.additional_window = Toplevel(self.root)
            self.additional_window.geometry('200x200+{}+{}'.format(
                self.root.winfo_x() + 20 + self.root.winfo_width(), self.root.winfo_y()))
            self.additional_window.overrideredirect(1)

            # Add images to be used as buttons, scaled down to 10x10
            ai_image = PhotoImage(file="ai.png").subsample(9)  # 50% scaling
            clipboard_image = PhotoImage(file="clipboard.png").subsample(9)
            screenshare_image = PhotoImage(file="screenshare.png").subsample(9)
            devices_image = PhotoImage(file="devices.png").subsample(9)

            # Set background color for buttons
            button_bg_color = 'white'

            # Add buttons to the additional window with images and background color
            ai_button = Button(self.additional_window, image=ai_image, command=self.perform_ai_action, bg=button_bg_color)
            ai_button.image = ai_image  # To prevent image from being garbage collected
            ai_button.grid(row=0, column=0, sticky="nsew")

            clipboard_button = Button(self.additional_window, image=clipboard_image, command=self.perform_clipboard_action, bg=button_bg_color)
            clipboard_button.image = clipboard_image
            clipboard_button.grid(row=0, column=1, sticky="nsew")

            screenshare_button = Button(self.additional_window, image=screenshare_image, command=self.perform_screenshare_action, bg=button_bg_color)
            screenshare_button.image = screenshare_image
            screenshare_button.grid(row=1, column=0, sticky="nsew")

            devices_button = Button(self.additional_window, image=devices_image, command=self.perform_devices_action, bg=button_bg_color)
            devices_button.image = devices_image
            devices_button.grid(row=1, column=1, sticky="nsew")

            # Configure grid to make buttons fill the entire window
            self.additional_window.grid_rowconfigure(0, weight=1)
            self.additional_window.grid_rowconfigure(1, weight=1)
            self.additional_window.grid_columnconfigure(0, weight=1)
            self.additional_window.grid_columnconfigure(1, weight=1)

            # Set flag to indicate additional window is open
            self.additional_window_open = True

    def hide_additional_window(self):
        if self.additional_window_open:
            # Destroy the additional window if it's open
            self.additional_window.destroy()
            # Reset the flag
            self.additional_window_open = False

    def perform_ai_action(self):
        print("AI action")

    def perform_clipboard_action(self):
        print("Clipboard action")

    def perform_screenshare_action(self):
        print("Screenshare action")

    def perform_devices_action(self):
        print("Devices action")

if __name__ == "__main__":
    root = Tk()
    app = MovableWindow(root)
    root.mainloop()
