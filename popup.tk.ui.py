import threading
from tkinter import messagebox
import socket
import customtkinter
from customtkinter import CTk, CTkToplevel, CTkFrame, CTkButton, CTkImage, CTkLabel , CTkEntry
from PIL import Image

customtkinter.set_appearance_mode("dark")

class ToplevelWindow(CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x400")
        self.overrideredirect(1)  # Make it borderless
        self.master = master
        # Create a frame for each row of buttons
        top_frame = CTkFrame(self)
        top_frame.pack()
        bottom_frame = CTkFrame(self)
        bottom_frame.pack()

        # Create buttons with images and pack them in their respective frames
        image = CTkImage(dark_image=Image.open("./images/wand.png"), size=(30, 30))
        wand = CTkButton(top_frame, image=image, width=90, height=90, text="")
        wand.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/notes.png"), size=(30, 30))
        notes = CTkButton(top_frame, image=image, width=90, height=90, text="")
        notes.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/screenshare.png"), size=(30, 30))
        share = CTkButton(bottom_frame, image=image, width=90, height=90, text="")
        share.pack(side="left", padx=5, pady=5)

        image = CTkImage(dark_image=Image.open("./images/synced-clip.png"), size=(30, 30))
        clip = CTkButton(bottom_frame, image=image, width=90, height=90, text="")
        clip.pack(side="left", padx=5, pady=5)

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("10x40+0+0")
        self.wm_attributes("-alpha", 0.5)
        self.overrideredirect(1)
        self.drag_data = {"y": 0}
        self.screen_height = self.winfo_screenheight()
        self.additional_window = None  # Initialize as None
        self.wm_attributes("-topmost", 1)

        self.bind("<Double-Button-1>", self.show_message_popup)

        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<FocusOut>", self.focus_out)

        # Start the thread to listen for data from the server
        self.listen_thread = threading.Thread(target=self.listen_server)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def show_message_popup(self, event):
        popup = CTkToplevel(self)
        popup.geometry("+100+100")
        popup.wm_attributes("-topmost", 1)
        popup.wm_attributes("-alpha", 0.9)
        popup.overrideredirect(1)

        # Create entry widget for user input
        entry = CTkEntry(popup)
        entry.pack()

        # Bind the Enter key to send message and close popup
        entry.bind("<Return>", lambda event: self.send_message_and_close_popup(entry,popup, entry.get()))

        entry.focus_set()
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

    def focus_out(self, event):
        if self.additional_window:
            self.additional_window.destroy()
            self.additional_window = None

    def listen_server(self):
        server_address = ('localhost', 5000)
        buffer_size = 1024
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(server_address)
            print("Connected to server at", server_address)
            while True:
                data = client_socket.recv(buffer_size)
                if data:
                    print("Received data:", data.decode())
                    self.show_popup()

    def send_message_and_close_popup(self,entry, popup, message):
        server_address = ('localhost', 5000)
        buffer_size = 1024
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(server_address)
                client_socket.sendall(message.encode())
                entry.destroy()
                info = CTkLabel(popup, text="Sent!").pack()
                messagebox.showinfo("Success", "Message sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
        finally:
            popup.destroy()

    def show_popup(self):
        popup = CTkToplevel(self)
        popup.geometry(f"+{self.winfo_x() + 60}+{self.winfo_y()}")
        popup.wm_attributes("-topmost", 1)
        popup.wm_attributes("-alpha", 0.9)
        popup.overrideredirect(1)

        # Load the image
        image_path = "./images/synced-clip.png"
        img = CTkImage(dark_image=Image.open(image_path),size=(60,60))  # Resize the image

        # Display the image on a label with padding
        label = CTkLabel(popup, text="", image=img, padx=20, pady=20)
        label.image = img  # Keep a reference to avoid garbage collection
        label.pack()

        popup.after(3000, popup.destroy)  # Destroy popup after 3 seconds


if __name__ == "__main__":
    app = App()
    app.mainloop()
