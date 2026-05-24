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
        super().__init__(fg_color="#1a1a2e")

        self.geometry('400x300')
        self.title("LogiTalk")

       
        self.menu_frame = CTkFrame(
            self,
            width=30,
            height=300,
            corner_radius=0,
            fg_color="#16213e"
        )

        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)

        self.is_show_menu = False
        self.menu_speed = -5

        self.btn_menu = CTkButton(
            self.menu_frame,
            text="☰",
            width=30,
            command=self.toggle_show_menu,
            fg_color="#e94560",
            hover_color="#ff6b9d",
            text_color="white",
            font=("Helvetica", 14, "bold")
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
            fg_color="#0f3460"
        )

        self.chat_field.place(x=0, y=0)
#Уввід тексту і контур 
        self.message_entry = CTkEntry(
            self,
            placeholder_text="Введіть повідомлення...",
            height=40,
            fg_color="#16213e",
            border_color="#e94560",
            border_width=2,
            text_color="white",
            placeholder_text_color="#888888"
        )

        self.message_entry.place(x=0, y=0)
#кнопка відкритя файлів і вибір 
        self.send_img = CTkButton(
            self,
            text="🖼️",
            width=50,
            height=40,
            command=self.send_image,
            fg_color="#0f3460",
            hover_color="#533483",
            text_color="white",
            font=("Helvetica", 16)
        )

        self.send_img.place(x=0, y=0)
#кнобка вибору та відправки 
        self.send_button = CTkButton(
            self,
            text="➤",
            width=50,
            height=40,
            command=self.send_message,
            fg_color="#e94560",
            hover_color="#ff6b9d",
            text_color="white",
            font=("Helvetica", 14, "bold")
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
                text_color="#ff6b9d",
                font=("Helvetica", 14, "bold")
            )

            self.label_name.pack(pady=20)

            self.entry_name = CTkEntry(
                self.menu_frame,
                placeholder_text="Введіть ім'я",
                fg_color="#0f3460",
                border_color="#e94560",
                border_width=2,
                text_color="white",
                placeholder_text_color="#888888"
            )

            self.entry_name.pack(padx=10, pady=10)

            self.btn_name = CTkButton(
                self.menu_frame,
                text="Зберегти",
                command=self.save_name,
                fg_color="#e94560",
                hover_color="#ff6b9d",
                text_color="white",
                font=("Helvetica", 12, "bold")
            )

            self.btn_name.pack(pady=10)
    
    def save_name(self):
        self.username = self.entry_name.get() if self.entry_name.get() else "User"

        self.add_message(
            f"Ваш нікнейм змінено на {self.username}",
            is_system=True
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
            self.add_message(message, is_own=True)

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

    def add_message(self, message, img=None, is_own=False, is_system=False):
        if is_system:
            frame = CTkFrame(
                self.chat_field,
                fg_color="#533483",
                corner_radius=8
            )
            text_color = "#bb86fc"
        elif is_own:
            frame = CTkFrame(
                self.chat_field,
                fg_color="#e94560",
                corner_radius=8
            )
            text_color = "white"
        else:
            frame = CTkFrame(
                self.chat_field,
                fg_color="#16213e",
                corner_radius=8
            )
            text_color = "#00d4ff"
        
        frame.pack(
            padx=8,
            anchor="e" if is_own else "w",
            pady=5,
            fill="x"
        )
        
        wrap_size = self.winfo_width() - self.menu_frame.winfo_width() - 40
        if not img:
            CTkLabel(
                frame,
                text=message,
                wraplength=wrap_size,
                justify="left",
                text_color=text_color,
                font=("Helvetica", 11)
            ).pack(
                pady=8,
                padx=10,
                fill="both",
                expand=True)
        else:
            CTkLabel(
                frame,
                text=message,
                wraplength=wrap_size,
                image=img,
                compound="top",
                justify="left",
                text_color=text_color,
                font=("Helvetica", 11)
            ).pack(
                padx=10,
                pady=8,
                fill="both",
                expand=True)

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
                ),
                is_own=True
            )
            self.sock.sendall(data.encode())
        except Exception as e:
            self.add_message(f"Image Send Error: {str(e)}")

if __name__ == "__main__":
    win = LogiTalk()
    win.mainloop()
