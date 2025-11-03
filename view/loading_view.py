import tkinter as tk
from tkinter import ttk

class LoadingView:
    def __init__(self, root):
        self.root = root
        self.animation_running = False
    
    def create_scrollable_frame(self, parent):
        """Cria um frame com scrollbar"""
        main_frame = ttk.Frame(parent, style='Modern.TFrame')
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame, bg='#0f1b2d', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", configure_canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return scrollable_frame
    
    def show(self):
        """Mostra a página de loading"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = self.create_scrollable_frame(self.root)
        container = ttk.Frame(main_frame, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        content_frame = ttk.Frame(container, style='Card.TFrame')
        content_frame.pack(expand=True, fill='both', padx=40, pady=60)
        
        title_label = tk.Label(
            content_frame,
            text="Analisando sua Rede",
            font=('Arial', 24, 'bold'),
            bg='#1a2b3c',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 30))
        
        self.loading_label = tk.Label(
            content_frame,
            text="🛡️",
            font=('Arial', 40),
            bg='#1a2b3c',
            fg='#3498db'
        )
        self.loading_label.pack(pady=20)
        
        loading_text = tk.Label(
            content_frame,
            text="Estamos escaneando sua rede em busca de dispositivos\n e verificando possíveis vulnerabilidades...\n\n"
                 "Este processo pode levar alguns minutos dependendo do tamanho da sua rede.\n"
                 "Por favor, aguarde enquanto coletamos todas as informações.",
            font=('Arial', 11),
            bg='#1a2b3c',
            fg='#8899aa',
            justify='center'
        )
        loading_text.pack(pady=10)
        
        self.progress = ttk.Progressbar(
            content_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(pady=30)
        self.progress.start()
        
        info_frame = ttk.Frame(content_frame, style='Card.TFrame')
        info_frame.pack(fill='x', pady=20)
        
        info_text = tk.Label(
            info_frame,
            text="🔍 O que estamos fazendo:\n"
                 "• Escaneando dispositivos na rede\n"
                 "• Verificando portas abertas\n"
                 "• Analisando vulnerabilidades\n"
                 "• Gerando relatório de segurança\n\n"
                 "💡 Dica: Execute como Administrador para melhor detecção!",
            font=('Arial', 10),
            bg='#1a2b3c',
            fg='#bdc3c7',
            justify='left'
        )
        info_text.pack()
        
        self.animation_running = True
        self.animate_loading()
    
    def animate_loading(self):
        """Anima o ícone de loading"""
        if not self.animation_running:
            return
            
        current_text = self.loading_label.cget("text")
        icons = ["🛡️", "🔍", "⚠️", "🛡️", "🌐", "📱", "🔒"]
        
        if current_text in icons:
            next_index = (icons.index(current_text) + 1) % len(icons)
        else:
            next_index = 0
            
        self.loading_label.config(text=icons[next_index])
        self.root.after(500, self.animate_loading)
    
    def stop_animation(self):
        """Para a animação"""
        self.animation_running = False