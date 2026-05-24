from customtkinter import *
from socket import *
import threading
import base64
import io
from PIL import Image
from tkinter import filedialog
import os

class LogiTalk(CTk):
    def __init__(self):
        super().__init__(fg_color="#0707DA")

        self.geometry('400x300')
        self.title("LogiTalk")

       
        self.menu_frame = CTkFrame(
            self,
            width=30,
            height=300,
            corner_radius=0,
            fg_color="#FBFF00"
        )

        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)

        self.is_show_menu = False
        self.menu_speed = -5

        self.btn_menu = CTkButton(
            self.menu_frame,
            text="Menu",
            width=30,
            command=self.toggle_show_menu,
            fg_color="#F30707",
            hover_color="#A2DD00",
            text_color="white"
        )

        self.btn_menu.pack()

        self.username = "User"

        # Initialize menu attributes to prevent AttributeError
        self.label_name = None
        self.entry_name = None
        self.btn_name = None

#задній фон
        self.chat_field = CTkScrollableFrame(
            self,
            fg_color="#13007C"
        )

        self.chat_field.place(x=0, y=0)
#Уввід тексту і контур 
        self.message_entry = CTkEntry(
            self,
            placeholder_text="Введіть повідомлення...",
            height=40,
            fg_color="#A80092",
            border_color="#A30088",
            text_color="white",
            placeholder_text_color="#000000"
        )

        self.message_entry.place(x=0, y=0)
#кнопка відкритя файлів і вибір 
        self.send_img = CTkButton(
            self,
            text="",
            width=50,
            height=40,
            command=self.send_image,
            fg_color="#5902BD",
            hover_color="#2B0497",
            text_color="white"
        )

        self.send_img.place(x=0, y=0)
#кнобка вибору та відправки 
        self.send_button = CTkButton(
            self,
            text="->",
            width=50,
            height=40,
            command=self.send_message,
            fg_color="#00B38C",
            hover_color="#01DFAF",
            text_color="white"
        )

        self.send_button.place(x=0, y=0)

        self.adaptive_ui()

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("7.tcp.eu.ngrok.io", 29483))

            hello = f"TEXT@{self.username}@{self.username} приєднався до чату! \n"

            self.sock.send(hello.encode())

            threading.Thread(
                target=self.recv_message,
                daemon=True
            ).start()

        except Exception as e:
            self.add_message(f"Connection Error: {str(e)}")

    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.menu_speed *= -1
            self.show_menu()

        else:
            self.is_show_menu = True
            self.menu_speed *= -1
            self.show_menu()

            self.label_name = CTkLabel(
                self.menu_frame,
                text="Ім'я",
                text_color="#002C58"
            )

            self.label_name.pack(pady=20)

            self.entry_name = CTkEntry(
                self.menu_frame,
                placeholder_text="Введіть ім'я",
                fg_color="#001D46",
                border_color="#B41111",
                text_color="white",
                placeholder_text_color="#FDFEFF"
            )

            self.entry_name.pack()

            self.btn_name = CTkButton(
                self.menu_frame,
                text="Зберегти",
                command=self.save_name,
                fg_color="#0000E2",
                hover_color="#0118EBFF",
                text_color="white"
            )

            self.btn_name.pack()
    
    def save_name(self):
        self.username = self.entry_name.get() if self.entry_name.get() else "User"

        self.add_message(
            f"Ваш нікнейм змінено на {self.username}"
        )

    def show_menu(self):
        self.menu_frame.configure(
            width=self.menu_frame.winfo_width() + self.menu_speed
        )

        if not self.menu_frame.winfo_width() >= 200 and self.is_show_menu:
            self.after(10, self.show_menu)

        elif self.menu_frame.winfo_width() >= 40 and not self.is_show_menu:
            self.after(10, self.show_menu)

            if self.label_name is not None and self.entry_name is not None and self.btn_name is not None:
                self.label_name.destroy()
                self.entry_name.destroy()
                self.btn_name.destroy()
                self.label_name = None
                self.entry_name = None
                self.btn_name = None

    def adaptive_ui(self):
        self.menu_frame.configure(height=self.winfo_height())

        self.chat_field.place(
            x=self.menu_frame.winfo_width()
        )

        chat_width = self.winfo_width() - self.menu_frame.winfo_width()

        self.chat_field.configure(
            width=chat_width,
            height=self.winfo_height()
        )

        self.message_entry.place(
            x=self.menu_frame.winfo_width(), 
            y=self.winfo_height() - self.message_entry.winfo_height()
        )

        self.message_entry.configure(
            width=chat_width-self.send_button.winfo_width()
        )

        self.send_img.place(
            x=self.winfo_width() - self.send_button.winfo_width() * 2, 
            y=self.winfo_height() - self.message_entry.winfo_height()
        )

        self.send_button.place(
            x=self.winfo_width() - self.send_button.winfo_width(),
            y=self.winfo_height() - self.message_entry.winfo_height()
        )

        self.after(50, self.adaptive_ui)

    def send_message(self):
        message = self.message_entry.get()

        if message:
            self.add_message(message)

            data = f"TEXT@{self.username}@{message}\n"

            try:
                self.sock.sendall(data.encode())

            except Exception as e:
                self.add_message(f"Send Error: {str(e)}")

        self.message_entry.delete(0, END)

    def recv_message(self):
        buffer = ""

        while True:
            try:
                chunk = self.sock.recv(4096)

                if not chunk:
                    break

                buffer += chunk.decode()

                while "\n" in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())

            except Exception as e:
                self.add_message(f"Receive Error: {str(e)}")
                break
        self.sock.close()

    def add_message(self, message, img=None):
        frame = CTkFrame(
            self.chat_field,
            fg_color="#02D45A"
        )
        frame.pack(
            padx=5,
            anchor="w",
            pady=3
        )
        wrap_size = self.winfo_width() - self.menu_frame.winfo_width() - 40
        if not img:
            CTkLabel(
                frame,
                text=message,
                wraplength=wrap_size,
                justify="left",
                text_color="#FFFFFF"
            ).pack(
                pady=5,
                padx=5)
        else:
            CTkLabel(
                frame,
                text=message,
                wraplength=wrap_size,
                image=img,
                compound="top",
                justify="left",
                text_color="#FFFFFF"
            ).pack(
                padx=5,
                pady=5)

    def handle_line(self, line):
        if not line:
            return 
        parts = line.split("@", 3)
        msg_type = parts[0]
        if msg_type == "TEXT":
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(
                    f"{author}: {message}"
                )
        elif msg_type == "IMAGE":
            if len(parts) >= 4:
                author = parts[1]
                message = parts[2]
                b64_img = parts[3]
                try:
                    img_data = base64.b64decode(b64_img)
                    pil_img = Image.open(io.BytesIO(img_data))
                    ctk_img = CTkImage(
                        pil_img,
                        size=(300, 300)
                    )
                    self.add_message(
                        f"{author}: {message}",
                        img=ctk_img
                    )
                except Exception as e:
                    self.add_message(f"Image Error: {str(e)}")

    def send_image(self):
        filename = filedialog.askopenfilename()
        if not filename:
            return
        try:
            with open(filename, "rb") as f:
                raw = f.read()
            b64_data = base64.b64encode(raw).decode()
            shortname = os.path.basename(filename)
            data = f"IMAGE@{self.username}@{shortname}@{b64_data}\n"
            self.add_message(
                '',
                CTkImage(
                    light_image=Image.open(filename),
                    size=(300, 300)
                )
            )
            self.sock.sendall(data.encode())
        except Exception as e:
            self.add_message(f"Image Send Error: {str(e)}")

if __name__ == "__main__":
    win = LogiTalk()
    win.mainloop()
