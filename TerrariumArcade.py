import customtkinter as ctk
import random
import math

class TerrariumArcade(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#1a1a2e")
        
        self.geometry('800x600')
        self.title("🌿 Терраріум Аркада 🌿")
        self.resizable(False, False)
        
        # Гра стан
        self.running = False
        self.score = 0
        self.health = 100
        self.water = 100
        self.light = 100
        self.plant_size = 20
        self.level = 1
        
        # Позиції
        self.plant_x = 400
        self.plant_y = 400
        self.bugs = []
        self.resources = []
        
        # Швидкості
        self.bug_speed = 2
        self.spawn_rate = 50
        self.frame_count = 0
        
        # UI Фрейм (top)
        self.ui_frame = ctk.CTkFrame(self, fg_color="#16213e", height=60, corner_radius=0)
        self.ui_frame.pack(fill="x", padx=0, pady=0)
        self.ui_frame.pack_propagate(False)
        
        # Рахунок
        self.score_label = ctk.CTkLabel(
            self.ui_frame,
            text=f"💰 Очки: {self.score}",
            font=("Helvetica", 16, "bold"),
            text_color="#00d4ff"
        )
        self.score_label.pack(side="left", padx=20, pady=15)
        
        # Рівень
        self.level_label = ctk.CTkLabel(
            self.ui_frame,
            text=f"📊 Рівень: {self.level}",
            font=("Helvetica", 16, "bold"),
            text_color="#ff6b9d"
        )
        self.level_label.pack(side="left", padx=20, pady=15)
        
        # Статус рослини
        self.status_label = ctk.CTkLabel(
            self.ui_frame,
            text=f"❤️ Здоров'я: {self.health}% | 💧 Вода: {self.water}% | ☀️ Світло: {self.light}%",
            font=("Helvetica", 13),
            text_color="#bb86fc"
        )
        self.status_label.pack(side="right", padx=20, pady=15)
        
        # Канвас гри
        self.canvas = ctk.CTkCanvas(
            self,
            width=800,
            height=540,
            bg="#0f3460",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Кнопки
        self.button_frame = ctk.CTkFrame(self, fg_color="#1a1a2e")
        self.button_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_button = ctk.CTkButton(
            self.button_frame,
            text="▶️ Почати гру",
            command=self.start_game,
            fg_color="#e94560",
            hover_color="#ff6b9d",
            text_color="white",
            font=("Helvetica", 14, "bold"),
            width=150
        )
        self.start_button.pack(side="left", padx=10)
        
        self.pause_button = ctk.CTkButton(
            self.button_frame,
            text="⏸️ Пауза",
            command=self.toggle_pause,
            fg_color="#0f3460",
            hover_color="#533483",
            text_color="white",
            font=("Helvetica", 14, "bold"),
            width=150,
            state="disabled"
        )
        self.pause_button.pack(side="left", padx=10)
        
        self.info_label = ctk.CTkLabel(
            self.button_frame,
            text="Клікніть 'Почати гру' щоб розпочати! 🌱",
            font=("Helvetica", 12),
            text_color="#00d4ff"
        )
        self.info_label.pack(side="left", padx=20)
        
        self.paused = False
        
    def start_game(self):
        if not self.running:
            self.running = True
            self.score = 0
            self.health = 100
            self.water = 100
            self.light = 100
            self.plant_size = 20
            self.level = 1
            self.bugs = []
            self.resources = []
            self.frame_count = 0
            self.paused = False
            
            self.start_button.configure(state="disabled")
            self.pause_button.configure(state="normal")
            self.info_label.configure(text="Гра почалась! Рухайте рослину і збирайте ресурси! 🌿")
            
            self.game_loop()
    
    def toggle_pause(self):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.configure(text="▶️ Продовжити")
                self.info_label.configure(text="⏸️ Гра на паузі")
            else:
                self.pause_button.configure(text="⏸️ Пауза")
                self.info_label.configure(text="Гра продовжується! 🌿")
                self.game_loop()
    
    def on_mouse_move(self, event):
        if self.running and not self.paused:
            # Рослина слідує за мишею
            self.plant_x = event.x
            self.plant_y = event.y + 60  # Врахувати UI
    
    def spawn_bug(self):
        """Створити шкідника"""
        x = random.randint(50, 750)
        y = random.randint(100, 500)
        self.bugs.append({
            "x": x,
            "y": y,
            "vx": random.uniform(-1.5, 1.5),
            "vy": random.uniform(-1.5, 1.5),
            "size": 8
        })
    
    def spawn_resource(self):
        """Створити ресурс (вода, світло)"""
        x = random.randint(50, 750)
        y = random.randint(100, 500)
        resource_type = random.choice(["water", "light"])
        self.resources.append({
            "x": x,
            "y": y,
            "type": resource_type,
            "size": 6
        })
    
    def update_game(self):
        """Оновити стан гри"""
        if not self.running or self.paused:
            return
        
        self.frame_count += 1
        
        # Спавн шкідників
        if self.frame_count % self.spawn_rate == 0:
            self.spawn_bug()
        
        # Спавн ресурсів
        if self.frame_count % (self.spawn_rate + 20) == 0:
            self.spawn_resource()
        
        # Оновити рослину
        self.health -= 0.3
        self.water -= 0.2
        self.light -= 0.15
        
        # Перевірка здоров'я
        if self.health <= 0 or self.water <= 0 or self.light <= 0:
            self.game_over()
            return
        
        # Оновити шкідників
        for bug in self.bugs[:]:
            bug["x"] += bug["vx"]
            bug["y"] += bug["vy"]
            
            # Відбиток від стін
            if bug["x"] <= 0 or bug["x"] >= 800:
                bug["vx"] *= -1
            if bug["y"] <= 70 or bug["y"] >= 540:
                bug["vy"] *= -1
            
            # Перевірка колізії з рослиною
            dist = math.sqrt((bug["x"] - self.plant_x)**2 + (bug["y"] - self.plant_y)**2)
            if dist < self.plant_size + bug["size"]:
                self.health -= 5
                self.bugs.remove(bug)
                continue
            
            # Видалити шкідників за межами екрану
            if bug["x"] < -20 or bug["x"] > 820 or bug["y"] < 50 or bug["y"] > 560:
                if bug in self.bugs:
                    self.bugs.remove(bug)
        
        # Оновити ресурси
        for resource in self.resources[:]:
            # Перевірка колізії з рослиною
            dist = math.sqrt((resource["x"] - self.plant_x)**2 + (resource["y"] - self.plant_y)**2)
            if dist < self.plant_size + resource["size"]:
                if resource["type"] == "water":
                    self.water = min(100, self.water + 20)
                    self.score += 10
                else:  # light
                    self.light = min(100, self.light + 20)
                    self.score += 15
                self.resources.remove(resource)
                self.plant_size += 1
            
            # Видалити ресурси за межами екрану
            if resource["x"] < -20 or resource["x"] > 820 or resource["y"] < 50 or resource["y"] > 560:
                if resource in self.resources:
                    self.resources.remove(resource)
        
        # Рівень
        self.level = (self.score // 100) + 1
        self.bug_speed = 2 + (self.level * 0.3)
        self.spawn_rate = max(30, 60 - (self.level * 3))
        
        # Оновити UI
        self.score_label.configure(text=f"💰 Очки: {self.score}")
        self.level_label.configure(text=f"📊 Рівень: {self.level}")
        self.status_label.configure(
            text=f"❤️ Здоров'я: {int(self.health)}% | 💧 Вода: {int(self.water)}% | ☀️ Світло: {int(self.light)}%"
        )
    
    def draw_game(self):
        """Намалювати гру"""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, 800, 540, fill="#0f3460", outline="")
        
        # Сітка
        for i in range(0, 800, 50):
            self.canvas.create_line(i, 0, i, 540, fill="#16213e", width=1)
        for i in range(0, 540, 50):
            self.canvas.create_line(0, i, 800, i, fill="#16213e", width=1)
        
        # Намалювати ресурси
        for resource in self.resources:
            if resource["type"] == "water":
                self.canvas.create_oval(
                    resource["x"] - resource["size"],
                    resource["y"] - resource["size"],
                    resource["x"] + resource["size"],
                    resource["y"] + resource["size"],
                    fill="#00d4ff",
                    outline="#00d4ff",
                    width=2
                )
                self.canvas.create_text(
                    resource["x"], resource["y"],
                    text="💧",
                    font=("Arial", 12)
                )
            else:  # light
                self.canvas.create_oval(
                    resource["x"] - resource["size"],
                    resource["y"] - resource["size"],
                    resource["x"] + resource["size"],
                    resource["y"] + resource["size"],
                    fill="#ffeb3b",
                    outline="#ffeb3b",
                    width=2
                )
                self.canvas.create_text(
                    resource["x"], resource["y"],
                    text="☀️",
                    font=("Arial", 12)
                )
        
        # Намалювати шкідників
        for bug in self.bugs:
            self.canvas.create_oval(
                bug["x"] - bug["size"],
                bug["y"] - bug["size"],
                bug["x"] + bug["size"],
                bug["y"] + bug["size"],
                fill="#e94560",
                outline="#ff6b9d",
                width=2
            )
            self.canvas.create_text(
                bug["x"], bug["y"],
                text="🦗",
                font=("Arial", 10)
            )
        
        # Намалювати рослину
        self.canvas.create_oval(
            self.plant_x - self.plant_size,
            self.plant_y - self.plant_size,
            self.plant_x + self.plant_size,
            self.plant_y + self.plant_size,
            fill="#02D45A",
            outline="#00ff00",
            width=3
        )
        self.canvas.create_text(
            self.plant_x, self.plant_y,
            text="🌱",
            font=("Arial", int(self.plant_size))
        )
        
        # Паузу текст
        if self.paused:
            self.canvas.create_text(
                400, 270,
                text="⏸️ ПАУЗА",
                font=("Arial", 40, "bold"),
                fill="#bb86fc"
            )
    
    def game_over(self):
        """Кінець гри"""
        self.running = False
        self.paused = False
        
        self.start_button.configure(state="normal", text="🔄 Почати заново")
        self.pause_button.configure(state="disabled")
        
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 800, 540, fill="#0f3460", outline="")
        
        self.canvas.create_text(
            400, 150,
            text="💀 ГАМА ЗАКІНЧИЛАСЬ 💀",
            font=("Arial", 40, "bold"),
            fill="#e94560"
        )
        
        self.canvas.create_text(
            400, 250,
            text=f"Ваш рахунок: {self.score} очків",
            font=("Arial", 30, "bold"),
            fill="#00d4ff"
        )
        
        self.canvas.create_text(
            400, 310,
            text=f"Рівень: {self.level}",
            font=("Arial", 25),
            fill="#ff6b9d"
        )
        
        self.canvas.create_text(
            400, 380,
            text="Натисніть 'Почати заново' щоб грати ще раз!",
            font=("Arial", 16),
            fill="#bb86fc"
        )
        
        self.info_label.configure(text=f"Гра закінчилась! Ваш рахунок: {self.score}")
    
    def game_loop(self):
        """Основний цикл гри"""
        if self.running and not self.paused:
            self.update_game()
            self.draw_game()
            
            if self.running:
                self.after(30, self.game_loop)
        elif self.paused:
            self.draw_game()

if __name__ == "__main__":
    app = TerrariumArcade()
    app.mainloop()
