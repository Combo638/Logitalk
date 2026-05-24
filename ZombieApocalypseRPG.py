import customtkinter as ctk
import random
import math

class ZombieApocalypseRPG(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#1a1a2e")
        
        self.geometry('1000x700')
        self.title("🧟 Зомбі Апокаліпсис RPG 🧟")
        self.resizable(False, False)
        
        # Гравець
        self.player = {
            "x": 500,
            "y": 400,
            "health": 100,
            "max_health": 100,
            "level": 1,
            "exp": 0,
            "exp_to_level": 100,
            "strength": 10,
            "speed": 3,
            "weapon": "pistol",
            "ammo": 30,
            "inventory": [],
            "size": 15
        }
        
        # Світ
        self.world_width = 2000
        self.world_height = 2000
        self.camera_x = self.player["x"] - 400
        self.camera_y = self.player["y"] - 300
        
        # Зомбі
        self.zombies = []
        self.spawn_zombies(10)
        
        # Лут
        self.loot = []
        self.spawn_loot(15)
        
        # NPC
        self.npcs = [
            {"x": 300, "y": 300, "name": "Павло", "dialog": "Врятуй нас!"},
            {"x": 1700, "y": 1700, "name": "Марія", "dialog": "База тут безпечна..."},
            {"x": 1000, "y": 500, "name": "Сергій", "dialog": "Зомбі повсюди!"}
        ]
        
        # Керування
        self.keys_pressed = set()
        self.bind('<KeyPress>', self.key_press)
        self.bind('<KeyRelease>', self.key_release)
        
        # Стан гри
        self.game_running = True
        self.paused = False
        self.selected_npc = None
        
        # UI
        self.create_ui()
        
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        self.mouse_x = 500
        self.mouse_y = 400
        
        self.game_loop()
    
    def key_press(self, event):
        """Клавіша натиснута"""
        self.keys_pressed.add(event.keysym.lower())
        
        if event.keysym == 'space':
            self.toggle_pause()
    
    def key_release(self, event):
        """Клавіша відпущена"""
        self.keys_pressed.discard(event.keysym.lower())
    
    def create_ui(self):
        """Створити UI"""
        # Верхня панель
        self.top_frame = ctk.CTkFrame(self, fg_color="#16213e", height=80, corner_radius=0)
        self.top_frame.pack(fill="x", padx=0, pady=0)
        self.top_frame.pack_propagate(False)
        
        # Статус гравця
        info_text = f"👤 Рівень: {self.player['level']} | ❤️ HP: {self.player['health']}/{self.player['max_health']}"
        self.info_label = ctk.CTkLabel(
            self.top_frame,
            text=info_text,
            font=("Helvetica", 14, "bold"),
            text_color="#00d4ff"
        )
        self.info_label.pack(side="left", padx=20, pady=15)
        
        # Досвід
        self.exp_label = ctk.CTkLabel(
            self.top_frame,
            text=f"⭐ Досвід: {self.player['exp']}/{self.player['exp_to_level']}",
            font=("Helvetica", 12),
            text_color="#ff6b9d"
        )
        self.exp_label.pack(side="left", padx=20, pady=15)
        
        # Зброя
        weapon_text = f"🔫 Зброя: {self.player['weapon'].upper()} ({self.player['ammo']} патронів)"
        self.weapon_label = ctk.CTkLabel(
            self.top_frame,
            text=weapon_text,
            font=("Helvetica", 12),
            text_color="#bb86fc"
        )
        self.weapon_label.pack(side="left", padx=20, pady=15)
        
        # Місцезнаходження
        self.location_label = ctk.CTkLabel(
            self.top_frame,
            text=f"📍 Позиція: ({self.player['x']}, {self.player['y']})",
            font=("Helvetica", 12),
            text_color="#00ff00"
        )
        self.location_label.pack(side="right", padx=20, pady=15)
        
        # Канвас
        self.canvas = ctk.CTkCanvas(
            self,
            width=1000,
            height=620,
            bg="#0a0e27",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Нижня панель
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#16213e", height=60, corner_radius=0)
        self.bottom_frame.pack(fill="x", padx=0, pady=0)
        self.bottom_frame.pack_propagate(False)
        
        self.help_label = ctk.CTkLabel(
            self.bottom_frame,
            text="🖱️ ЛМ: Стрільба | ПМ: Взяти лут | W/A/S/D: Рух | SPACE: Пауза",
            font=("Helvetica", 11),
            text_color="#888888"
        )
        self.help_label.pack(side="left", padx=20, pady=15)
    
    def spawn_zombies(self, count):
        """Спавн зомбі"""
        for _ in range(count):
            x = random.randint(100, self.world_width - 100)
            y = random.randint(100, self.world_height - 100)
            self.zombies.append({
                "x": x,
                "y": y,
                "health": 30,
                "speed": random.uniform(1.5, 2.5),
                "size": 12
            })
    
    def spawn_loot(self, count):
        """Спавн луту"""
        loot_types = ["ammo", "health", "exp_boost"]
        for _ in range(count):
            x = random.randint(100, self.world_width - 100)
            y = random.randint(100, self.world_height - 100)
            self.loot.append({
                "x": x,
                "y": y,
                "type": random.choice(loot_types),
                "size": 8
            })
    
    def on_mouse_move(self, event):
        """Рух миші"""
        self.mouse_x = event.x
        self.mouse_y = event.y
    
    def on_click(self, event):
        """Ліва кнопка - стрільба"""
        if self.game_running and not self.paused:
            self.shoot()
    
    def on_right_click(self, event):
        """Права кнопка - взяти лут"""
        if self.game_running and not self.paused:
            self.pickup_loot()
    
    def toggle_pause(self):
        """Пауза"""
        self.paused = not self.paused
    
    def shoot(self):
        """Стрільба"""
        if self.player["ammo"] > 0:
            self.player["ammo"] -= 1
            
            # Розраховуємо напрям до миші
            dx = self.mouse_x - 500
            dy = self.mouse_y - 350
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                dx /= dist
                dy /= dist
                
                # Урон зомбі
                for zombie in self.zombies[:]:
                    z_dx = zombie["x"] - self.player["x"]
                    z_dy = zombie["y"] - self.player["y"]
                    z_dist = math.sqrt(z_dx**2 + z_dy**2)
                    
                    # Перевіряємо чи в межах прицілу
                    if z_dist > 0:
                        angle = math.atan2(z_dy, z_dx) - math.atan2(dy, dx)
                        if abs(angle) < 0.3 and z_dist < 300:
                            damage = self.player["strength"] + random.randint(5, 15)
                            zombie["health"] -= damage
                            
                            if zombie["health"] <= 0:
                                self.zombies.remove(zombie)
                                self.player["exp"] += 50
                                
                                # Нові зомбі
                                if len(self.zombies) < 20:
                                    self.spawn_zombies(1)
    
    def pickup_loot(self):
        """Взяти лут"""
        for loot in self.loot[:]:
            dist = math.sqrt((loot["x"] - self.player["x"])**2 + (loot["y"] - self.player["y"])**2)
            if dist < 50:
                if loot["type"] == "ammo":
                    self.player["ammo"] += 30
                elif loot["type"] == "health":
                    self.player["health"] = min(self.player["max_health"], self.player["health"] + 30)
                elif loot["type"] == "exp_boost":
                    self.player["exp"] += 25
                
                self.loot.remove(loot)
                break
    
    def move_player(self):
        """Рух гравця"""
        if not self.game_running or self.paused:
            return
        
        speed = self.player["speed"]
        
        # W - вверх
        if 'w' in self.keys_pressed:
            self.player["y"] = max(0, self.player["y"] - speed)
        
        # S - вниз
        if 's' in self.keys_pressed:
            self.player["y"] = min(self.world_height, self.player["y"] + speed)
        
        # A - влево
        if 'a' in self.keys_pressed:
            self.player["x"] = max(0, self.player["x"] - speed)
        
        # D - вправо
        if 'd' in self.keys_pressed:
            self.player["x"] = min(self.world_width, self.player["x"] + speed)
    
    def update_game(self):
        """Оновити гру"""
        if not self.game_running or self.paused:
            return
        
        # Рух гравця
        self.move_player()
        
        # Оновити зомбі
        for zombie in self.zombies[:]:
            # Рух до гравця
            dx = self.player["x"] - zombie["x"]
            dy = self.player["y"] - zombie["y"]
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                dx /= dist
                dy /= dist
                zombie["x"] += dx * zombie["speed"]
                zombie["y"] += dy * zombie["speed"]
            
            # Атака гравця
            if dist < 30:
                self.player["health"] -= 1
        
        # Камера слідує за гравцем
        self.camera_x = self.player["x"] - 400
        self.camera_y = self.player["y"] - 300
        
        # Межі світу
        self.camera_x = max(0, min(self.camera_x, self.world_width - 800))
        self.camera_y = max(0, min(self.camera_y, self.world_height - 600))
        
        # Прокачка
        if self.player["exp"] >= self.player["exp_to_level"]:
            self.level_up()
        
        # Гра закінчилась?
        if self.player["health"] <= 0:
            self.game_over()
            return
        
        # Оновити UI
        self.update_ui()
    
    def level_up(self):
        """Підвищити рівень"""
        self.player["exp"] -= self.player["exp_to_level"]
        self.player["level"] += 1
        self.player["max_health"] += 20
        self.player["health"] = self.player["max_health"]
        self.player["strength"] += 5
        self.player["exp_to_level"] = int(self.player["exp_to_level"] * 1.5)
    
    def update_ui(self):
        """Оновити UI"""
        info_text = f"👤 Рівень: {self.player['level']} | ❤️ HP: {int(self.player['health'])}/{self.player['max_health']} | 🧟 Зомбі: {len(self.zombies)}"
        self.info_label.configure(text=info_text)
        
        self.exp_label.configure(text=f"⭐ Досвід: {self.player['exp']}/{self.player['exp_to_level']}")
        
        weapon_text = f"🔫 Зброя: {self.player['weapon'].upper()} ({self.player['ammo']} патронів)"
        self.weapon_label.configure(text=weapon_text)
        
        self.location_label.configure(text=f"📍 Позиція: ({int(self.player['x'])}, {int(self.player['y'])})")
    
    def draw_game(self):
        """Намалювати гру"""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, 1000, 620, fill="#0a0e27", outline="")
        
        # Сітка
        for i in range(-int(self.camera_x) % 50, 1000, 50):
            self.canvas.create_line(i, 0, i, 620, fill="#1a2a4a", width=1)
        for i in range(-int(self.camera_y) % 50, 620, 50):
            self.canvas.create_line(0, i, 1000, i, fill="#1a2a4a", width=1)
        
        # NPC
        for npc in self.npcs:
            sx = npc["x"] - self.camera_x
            sy = npc["y"] - self.camera_y
            
            if 0 <= sx <= 1000 and 0 <= sy <= 620:
                self.canvas.create_oval(sx-12, sy-12, sx+12, sy+12, fill="#00ff00", outline="#00ff00", width=2)
                self.canvas.create_text(sx, sy-25, text=npc["name"], font=("Arial", 10, "bold"), fill="#00ff00")
                self.canvas.create_text(sx, sy, text="👤", font=("Arial", 16))
        
        # Лут
        for loot in self.loot:
            sx = loot["x"] - self.camera_x
            sy = loot["y"] - self.camera_y
            
            if 0 <= sx <= 1000 and 0 <= sy <= 620:
                if loot["type"] == "ammo":
                    self.canvas.create_oval(sx-8, sy-8, sx+8, sy+8, fill="#ffeb3b", outline="#ffeb3b", width=2)
                    self.canvas.create_text(sx, sy, text="🔫", font=("Arial", 10))
                elif loot["type"] == "health":
                    self.canvas.create_oval(sx-8, sy-8, sx+8, sy+8, fill="#ff4081", outline="#ff4081", width=2)
                    self.canvas.create_text(sx, sy, text="❤️", font=("Arial", 10))
                else:
                    self.canvas.create_oval(sx-8, sy-8, sx+8, sy+8, fill="#00d4ff", outline="#00d4ff", width=2)
                    self.canvas.create_text(sx, sy, text="⭐", font=("Arial", 10))
        
        # Зомбі
        for zombie in self.zombies:
            sx = zombie["x"] - self.camera_x
            sy = zombie["y"] - self.camera_y
            
            if 0 <= sx <= 1000 and 0 <= sy <= 620:
                self.canvas.create_oval(sx-12, sy-12, sx+12, sy+12, fill="#e94560", outline="#ff6b9d", width=2)
                self.canvas.create_text(sx, sy, text="🧟", font=("Arial", 14))
                
                # Смужка здоров'я
                health_percent = zombie["health"] / 30
                self.canvas.create_rectangle(sx-15, sy-20, sx-15+30*health_percent, sy-18, fill="#00ff00", outline="white", width=1)
        
        # Гравець (центр екрану)
        px = 500
        py = 350
        self.canvas.create_oval(px-15, py-15, px+15, py+15, fill="#00d4ff", outline="#00ff00", width=3)
        self.canvas.create_text(px, py, text="🧑", font=("Arial", 18))
        
        # Приціл на мишу
        mx = self.mouse_x
        my = self.mouse_y
        self.canvas.create_line(mx-10, my, mx+10, my, fill="#ff6b9d", width=2)
        self.canvas.create_line(mx, my-10, mx, my+10, fill="#ff6b9d", width=2)
        
        # Паузу
        if self.paused:
            self.canvas.create_text(500, 310, text="⏸️ ПАУЗА", font=("Arial", 40, "bold"), fill="#bb86fc")
            self.canvas.create_text(500, 380, text="Натисніть SPACE щоб продовжити", font=("Arial", 14), fill="#bb86fc")
    
    def game_over(self):
        """Кінець гри"""
        self.game_running = False
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 1000, 620, fill="#0a0e27", outline="")
        
        self.canvas.create_text(
            500, 150,
            text="💀 ВИ МЕРТВІ 💀",
            font=("Arial", 50, "bold"),
            fill="#e94560"
        )
        
        self.canvas.create_text(
            500, 250,
            text=f"Рівень: {self.player['level']}",
            font=("Arial", 30),
            fill="#00d4ff"
        )
        
        self.canvas.create_text(
            500, 320,
            text=f"Вбито зомбі: {self.player['exp'] // 50}",
            font=("Arial", 25),
            fill="#ff6b9d"
        )
        
        self.canvas.create_text(
            500, 400,
            text="Закрийте вікно щоб вийти...",
            font=("Arial", 16),
            fill="#bb86fc"
        )
    
    def game_loop(self):
        """Основний цикл"""
        if self.game_running:
            self.update_game()
            self.draw_game()
            
            self.after(30, self.game_loop)

if __name__ == "__main__":
    app = ZombieApocalypseRPG()
    app.mainloop()
