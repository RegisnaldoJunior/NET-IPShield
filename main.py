import tkinter as tk
from controller.main_controller import MainController

class NetIPShield:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Net IPShield")
        self.root.geometry("900x700")
        self.root.configure(bg='#0f1b2d')
        self.root.resizable(True, True)
        
        self.controller = MainController(self.root)
        self.center_window()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 900
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def run(self):
        """Inicia a aplicação"""
        self.controller.show_home()
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 Iniciando Net IPShield...")
    print("⚠️  Execute como Administrador para melhor detecção!")
    
    app = NetIPShield()
    app.run()