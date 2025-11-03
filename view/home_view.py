import tkinter as tk
from tkinter import ttk

class HomeView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_styles()
    
    def setup_styles(self):
        """Configura os estilos visuais"""
        self.style = ttk.Style()
        self.style.configure('Modern.TFrame', background='#0f1b2d')
        self.style.configure('Card.TFrame', background='#1a2b3c', relief='flat', borderwidth=0)
        self.style.configure('Title.TLabel', background='#0f1b2d', foreground='#ffffff', font=('Arial', 28, 'bold'))
        self.style.configure('Subtitle.TLabel', background='#0f1b2d', foreground='#8899aa', font=('Arial', 12))
    
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
    
    def load_logo(self, header_frame):
        """Carrega a logo - VERSÃO CORRIGIDA PARA PYINSTALLER"""
        try:
            from PIL import Image, ImageTk
            import os
            import sys
            
            print("🔍 Tentando carregar logo...")
            
            # CORRETO: Detecta caminho do PyInstaller
            if getattr(sys, 'frozen', False):
                # Modo PyInstaller
                base_path = sys._MEIPASS
                print(f"📁 Modo PyInstaller - Base path: {base_path}")
            else:
                # Modo script Python
                base_path = os.path.dirname(os.path.abspath(__file__))
                print(f"📁 Modo Script - Base path: {base_path}")
            
            # Tenta diferentes caminhos
            possible_paths = [
                os.path.join(base_path, "logo.png"),
                os.path.join(os.getcwd(), "logo.png"),
                "logo.png"
            ]
            
            logo_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    logo_path = path
                    print(f"✅ Logo encontrada em: {path}")
                    break
            
            if logo_path and os.path.exists(logo_path):
                logo_image_pil = Image.open(logo_path)
                logo_image_pil = logo_image_pil.resize((300, 300), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image_pil)
                
                logo_label = tk.Label(
                    header_frame,
                    image=logo_photo,
                    bg='#0f1b2d'
                )
                logo_label.image = logo_photo  # Manter referência
                logo_label.pack(pady=(0, 5))
                print("✅ Logo carregada com sucesso na interface!")
                return True
            else:
                print("❌ Logo não encontrada em nenhum caminho tentado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao carregar logo: {e}")
            return False
    
    def _create_emoji_logo(self, header_frame):
        """Cria fallback com emoji"""
        print("🛡️ Usando fallback com emoji personalizado")
        logo_frame = tk.Frame(header_frame, bg='#0f1b2d', highlightthickness=2, highlightbackground='#3498db')
        logo_frame.pack(pady=5)
        
        logo_emoji = tk.Label(
            logo_frame,
            text="🛡️",
            font=('Arial', 48),
            bg='#0f1b2d',
            fg='#3498db',
            padx=30,
            pady=20
        )
        logo_emoji.pack()
        
        logo_text = tk.Label(
            logo_frame,
            text="NET\nIPSHIELD",
            font=('Arial', 12, 'bold'),
            bg='#0f1b2d',
            fg='#3498db',
            justify='center'
        )
        logo_text.pack(pady=(0, 15))
    
    def show(self):
        """Mostra a página inicial"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame scrollable
        main_frame = self.create_scrollable_frame(self.root)
        
        # Container principal que garante expansão
        container = ttk.Frame(main_frame, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Header com logo
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(30, 20))
        
        # Tenta carregar a logo - se falhar, usa fallback
        logo_loaded = self.load_logo(header_frame)
        if not logo_loaded:
            self._create_emoji_logo(header_frame)
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text="Net IPShield",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            header_frame,
            text="Proteção inteligente para sua rede doméstica",
            style='Subtitle.TLabel'
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Card de conteúdo PRINCIPAL - Este vai expandir
        content_frame = ttk.Frame(container, style='Card.TFrame')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Mensagem de boas-vindas
        welcome_label = tk.Label(
            content_frame,
            text="Bem-vindo ao Net IPShield",
            font=('Arial', 18, 'bold'),
            bg='#1a2b3c',
            fg='#ffffff'
        )
        welcome_label.pack(pady=(25, 15))
        
        # Instrução
        instruction_label = tk.Label(
            content_frame,
            text="Proteja sua rede com nossa solução completa de segurança\nClique abaixo para iniciar a análise da sua rede",
            font=('Arial', 11),
            bg='#1a2b3c',
            fg='#8899aa',
            justify='center'
        )
        instruction_label.pack(pady=(0, 30))
        
        # Features em cards
        features_frame = ttk.Frame(content_frame, style='Card.TFrame')
        features_frame.pack(fill='x', pady=(0, 40))
        
        features = [
            {"icon": "🔍", "text": "Detecta dispositivos\nconectados"},
            {"icon": "⚠️", "text": "Identifica\nvulnerabilidades"},
            {"icon": "🛡️", "text": "Recomendações de\nsegurança"}
        ]
        
        for feature in features:
            feature_frame = tk.Frame(features_frame, bg='#1a2b3c', relief='flat', bd=0)
            feature_frame.pack(side='left', expand=True, fill='both', padx=15)
            
            icon_label = tk.Label(
                feature_frame,
                text=feature["icon"],
                font=('Arial', 24),
                bg='#1a2b3c',
                fg='#3498db'
            )
            icon_label.pack(pady=(15, 8))
            
            text_label = tk.Label(
                feature_frame,
                text=feature["text"],
                font=('Arial', 10, 'bold'),
                bg='#1a2b3c',
                fg='#e0e6ed',
                wraplength=120,
                justify='center'
            )
            text_label.pack(pady=(0, 15))
        
        # Botão moderno - CENTRALIZADO
        button_container = ttk.Frame(content_frame, style='Card.TFrame')
        button_container.pack(pady=30)
        
        scan_button = tk.Button(
            button_container,
            text="INICIAR ANÁLISE DA REDE",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            padx=40,
            pady=15,
            border=0,
            cursor='hand2',
            command=self.controller.start_scan
        )
        scan_button.pack()
        
        # Efeitos hover
        def on_enter(e):
            scan_button.config(bg='#2980b9', relief='raised')
        
        def on_leave(e):
            scan_button.config(bg='#3498db', relief='flat')
        
        scan_button.bind("<Enter>", on_enter)
        scan_button.bind("<Leave>", on_leave)
        
        # Espaço extra para garantir expansão
        bottom_spacer = ttk.Frame(content_frame, style='Card.TFrame', height=20)
        bottom_spacer.pack(fill='x', side='bottom')
        
        # Footer - DENTRO do container principal
        footer_label = tk.Label(
            container,
            text="Net IPShield © 2025 - Segurança em Primeiro Lugar",
            font=('Arial', 9),
            bg='#0f1b2d',
            fg='#556677'
        )
        footer_label.pack(side='bottom', pady=20)
        
        # Forçar atualização do layout
        self.root.update_idletasks()