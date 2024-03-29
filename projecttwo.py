import tkinter as tk
from tkinter import messagebox

class ChessBoardGUI:
    def __init__(self, master, size=8, total_players=2, real_players=1):
        self.master = master
        self.size = size
        self.total_players = total_players
        self.real_players = real_players
        self.current_player = 1  # Başlangıçta 1. oyuncu sırası
        self.canvas = tk.Canvas(self.master, width=size*30, height=size*30, bg='black')
        self.canvas.pack()
        self.draw_board()
        self.create_warrior_placement_menu()

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i + j) % 2 == 0:
                    x1, y1 = j * 30, i * 30
                    x2, y2 = (j + 1) * 30, (i + 1) * 30
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='white')

    def place_warrior(self, row, col, warrior_type):
        x = col * 30 + 15
        y = row * 30 + 15
        self.canvas.create_text(x, y, text=warrior_type[0], font=('Arial', 12), fill='white')
        # Sıradaki oyuncunun numarasını güncelle
        self.current_player += 1
        if self.current_player > self.total_players:
            self.current_player = 1
        # Yerleştirme menüsünü yeniden oluştur veya sonraki turu başlat
        if self.current_player <= self.real_players:
            self.create_warrior_placement_menu()
        else:
            self.start_next_round()

    def create_warrior_placement_menu(self):
        # Eğer sıradaki oyuncu gerçek bir oyuncu ise, savaşçı yerleştirme menüsünü aç
        if self.current_player <= self.real_players:
            WarriorPlacementMenu(self.master, self)

    def start_next_round(self):
        # Bir sonraki turu başlat
        self.current_player = 1
        self.create_warrior_placement_menu()


class WarriorOption:
    def __init__(self, root, warrior_name, warrior_values):
        self.warrior_name = warrior_name
        self.warrior_values = warrior_values

        self.button = tk.Button(root, text=self.warrior_name)
        self.button.pack()
        self.button.bind("<Enter>", self.show_tooltip)
        self.button.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        tooltip_text = f"Name: {self.warrior_name}\nCost: {self.warrior_values[0]}\nHealth: {self.warrior_values[1]}\nTarget Type: {self.warrior_values[2]}\nDamage Percent: {self.warrior_values[3]}\nRange Yatay: {self.warrior_values[4]}\nRange Dikey: {self.warrior_values[5]}\nRange Capraz: {self.warrior_values[6]}"
        self.tooltip = tk.Toplevel(self.button)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{self.button.winfo_rootx() + 25}+{self.button.winfo_rooty() + 25}")
        label = tk.Label(self.tooltip, text=tooltip_text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=2)

    def hide_tooltip(self, event=None):
        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.destroy()

class WarriorPlacementMenu:
    def __init__(self, master, chess_board):
        self.master = master
        self.chess_board = chess_board

        self.top = tk.Toplevel(master)
        self.top.title("Savaşçı Yerleştirme")

        self.label_x = tk.Label(self.top, text="X Koordinatı:")
        self.label_x.pack()
        self.entry_x = tk.Entry(self.top)
        self.entry_x.pack()

        self.label_y = tk.Label(self.top, text="Y Koordinatı:")
        self.label_y.pack()
        self.entry_y = tk.Entry(self.top)
        self.entry_y.pack()

        self.label_warrior = tk.Label(self.top, text="Savaşçı Türünü Seçin:")
        self.label_warrior.pack()

        self.options_warrior = ["Muhafız", "Okçu", "Topçu", "Atlı","Sağlıkçı"]
        self.selected_warrior = tk.StringVar()
        self.selected_warrior.set(self.options_warrior[0])

        self.option_menu_warrior = tk.OptionMenu(self.top, self.selected_warrior, *self.options_warrior, command=self.show_warrior_info)
        self.option_menu_warrior.pack()

        self.label_warrior_info = tk.Label(self.top, text="")
        self.label_warrior_info.pack()

        self.confirm_button = tk.Button(self.top, text="Onayla", command=self.confirm_placement)
        self.confirm_button.pack()

    def show_warrior_info(self, selected_warrior):
            # Seçilen savaşçının özelliklerini al
        warrior_values = warrior_specs[selected_warrior]
            # Savaşçı özelliklerini görüntüle
        self.label_warrior_info.config(
            text=f"Savaşçı Özellikleri:\nCost: {warrior_values[0]}\nHealth: {warrior_values[1]}\nTarget Type: {warrior_values[2]}\nDamage Percent: {warrior_values[3]}\nRange Yatay: {warrior_values[4]}\nRange Dikey: {warrior_values[5]}\nRange Capraz: {warrior_values[6]}")

    def confirm_placement(self):
        x_coord = int(self.entry_x.get())
        y_coord = int(self.entry_y.get())
        if x_coord < 1 or x_coord > self.chess_board.size or y_coord < 1 or y_coord > self.chess_board.size:
            messagebox.showerror("Hata", "Geçersiz koordinatlar. Lütfen uygun değerlerde giriniz.")
            return
        warrior_type = self.selected_warrior.get()

        self.chess_board.place_warrior(x_coord - 1, y_coord - 1, warrior_type)
        messagebox.showinfo("Yerleştirme Onayı", f"{warrior_type} savaşçısı ({x_coord}, {y_coord}) konumuna yerleştirildi.")
        self.top.destroy()  # Yerleştirme işlemi tamamlandıktan sonra menü penceresini kapat

def create_chess_board():
    selected_option = option_var.get()
    if selected_option == "Kullanıcı Seçimi":
        user_size = int(entry.get())
        if 8 <= user_size <= 32:
            total_players = int(selected_player.get())
            real_players = int(selected_real_player.get())
            chess_board_gui = ChessBoardGUI(root, user_size, total_players, real_players)
            label_option.pack_forget()
            option_menu.pack_forget()
            label_entry.pack_forget()
            entry.pack_forget()
            label_players.pack_forget()
            option_menu_players.pack_forget()
            label_real_players.pack_forget()
            option_menu_real_players.pack_forget()
            button.pack_forget()
        else:
            tk.messagebox.showerror("Hata", "Lütfen geçerli bir boyut girin (8 ile 32 arasında).")
    elif selected_option in ["16x16", "24x24", "32x32"]:
        total_players = int(selected_player.get())
        real_players = int(selected_real_player.get())
        chess_board_gui = ChessBoardGUI(root, int(selected_option.split("x")[0]), total_players, real_players)
        label_option.pack_forget()
        option_menu.pack_forget()
        label_entry.pack_forget()
        entry.pack_forget()
        label_players.pack_forget()
        option_menu_players.pack_forget()
        label_real_players.pack_forget()
        option_menu_real_players.pack_forget()
        button.pack_forget()
class Warrior:
    def __init__(self, name, cost, health, target_type, damage_percent, range_yatay, range_dikey, range_capraz):
        self.name = name
        self.cost = cost
        self.health = health
        self.target_type = target_type
        self.damage_percent = damage_percent
        self.range_yatay = range_yatay
        self.range_dikey = range_dikey
        self.range_capraz = range_capraz

    def __repr__(self):
        return self.__str__()

# Sınıf içindeki özelliklere göre sadece tek bir savaşçı tanımlama
warrior_specs = {
    "Muhafız": (10, 80, "Menzildeki tüm düşmanlar", -20, 1, 1, 1),
    "Okçu": (20, 30, "Menzilde en yüksek canı olan 3 düşman", -60, 2, 2, 2),
    "Topçu": (50, 30, "Menzilde en yüksek canı olan 1 düşman", -100, 2, 2, 0),
    "Atlı": (30, 40, "Menzildeki en pahalı 2 düşman", -30, 0, 0, 3),
    "Sağlıkçı": (10, 100, "Menzilde en az canı olan 3 dost birlik", 50, 2, 2, 2)
}

# Sadece tek bir savaşçı tanımlama


root = tk.Tk()
root.title("WarGame")

label_option = tk.Label(root, text="Board Boyutu:")
label_option.pack()

options = ["Kullanıcı Seçimi", "16x16", "24x24", "32x32"]
option_var = tk.StringVar(root)
option_var.set(options[0])

option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.pack()

label_entry = tk.Label(root, text="Ya da boyutunu özelleştiriniz:")
label_entry.pack()

entry = tk.Entry(root)
entry.pack()

label_players = tk.Label(root, text="Kaç oyuncuyla oynamak istiyorsunuz?")
label_players.pack()

player_options = ["2", "3", "4"]
selected_player = tk.StringVar(root)
selected_player.set(player_options[0])

option_menu_players = tk.OptionMenu(root, selected_player, *player_options)
option_menu_players.pack()

label_real_players = tk.Label(root, text="Kaç gerçek oyuncuyla oynamak istiyorsunuz?")
label_real_players.pack()

real_player_options = ["1", "2", "3", "4"]
selected_real_player = tk.StringVar(root)
selected_real_player.set(real_player_options[0])

option_menu_real_players = tk.OptionMenu(root, selected_real_player, *real_player_options)
option_menu_real_players.pack()

button = tk.Button(root, text="Oluştur", command=create_chess_board)
button.pack()

root.mainloop()