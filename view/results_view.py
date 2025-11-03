import tkinter as tk
from tkinter import ttk
import datetime

class ResultsView:
    def __init__(self, root, controller, scan_data):
        self.root = root
        self.controller = controller
        self.scan_data = scan_data
    
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
        """Mostra a página de resultados"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = self.create_scrollable_frame(self.root)
        container = ttk.Frame(main_frame, style='Modern.TFrame')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(container, style='Modern.TFrame')
        header_frame.pack(fill='x', pady=(10, 20))
        
        title_label = tk.Label(
            header_frame,
            text="Resultados da Análise",
            font=('Arial', 24, 'bold'),
            bg='#0f1b2d',
            fg='#ffffff'
        )
        title_label.pack()
        
        # Conteúdo principal
        content_frame = ttk.Frame(container, style='Modern.TFrame')
        content_frame.pack(expand=True, fill='both', pady=10)
        
        # Cards de métricas
        self._create_metrics_cards(content_frame)
        
        # Área de resultados
        results_container = ttk.Frame(content_frame, style='Modern.TFrame')
        results_container.pack(expand=True, fill='both', pady=10)
        
        # Vulnerabilidades
        self._create_vulnerabilities_section(results_container)
        
        # Dispositivos vulneráveis
        if self.scan_data['vulnerable_devices']:
            self._create_vulnerable_devices_section(results_container)
        
        # Recomendações
        self._create_recommendations_section(results_container)
        
        # Botões de ação
        self._create_action_buttons(content_frame)
        
        final_spacer = ttk.Frame(container, style='Modern.TFrame', height=20)
        final_spacer.pack(fill='x', side='bottom')
    
    def _create_metrics_cards(self, parent):
        """Cria os cards de métricas"""
        metrics_frame = ttk.Frame(parent, style='Modern.TFrame')
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        public_ip = self.scan_data['public_ip']
        device_count = self.scan_data['device_count']
        vulnerable_devices = self.scan_data['vulnerable_devices']
        
        # Card IP Público
        ip_card = tk.Frame(metrics_frame, bg='#1a2b3c', relief='flat', bd=0, highlightthickness=0)
        ip_card.pack(side='left', expand=True, fill='both', padx=(0, 10))
        
        tk.Label(ip_card, text="🌐", font=('Arial', 16), bg='#1a2b3c', fg='#3498db').pack(pady=(15, 5))
        tk.Label(ip_card, text="IP Público", font=('Arial', 10), bg='#1a2b3c', fg='#8899aa').pack()
        tk.Label(ip_card, text=public_ip, font=('Arial', 12, 'bold'), bg='#1a2b3c', fg='#ffffff').pack(pady=(0, 15))
        
        # Card Dispositivos
        devices_card = tk.Frame(metrics_frame, bg='#1a2b3c', relief='flat', bd=0, highlightthickness=0)
        devices_card.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(devices_card, text="📱", font=('Arial', 16), bg='#1a2b3c', fg='#3498db').pack(pady=(15, 5))
        tk.Label(devices_card, text="Dispositivos", font=('Arial', 10), bg='#1a2b3c', fg='#8899aa').pack()
        tk.Label(devices_card, text=str(device_count), font=('Arial', 12, 'bold'), bg='#1a2b3c', fg='#ffffff').pack(pady=(0, 15))
        
        # Card Vulnerabilidades
        vuln_card = tk.Frame(metrics_frame, bg='#1a2b3c', relief='flat', bd=0, highlightthickness=0)
        vuln_card.pack(side='left', expand=True, fill='both', padx=(10, 0))
        
        vuln_count = len(vulnerable_devices)
        vuln_color = '#e74c3c' if vuln_count > 0 else '#2ecc71'
        vuln_icon = '⚠️' if vuln_count > 0 else '✅'
        
        tk.Label(vuln_card, text=vuln_icon, font=('Arial', 16), bg='#1a2b3c', fg=vuln_color).pack(pady=(15, 5))
        tk.Label(vuln_card, text="Vulnerabilidades", font=('Arial', 10), bg='#1a2b3c', fg='#8899aa').pack()
        tk.Label(vuln_card, text=str(vuln_count), font=('Arial', 12, 'bold'), bg='#1a2b3c', fg=vuln_color).pack(pady=(0, 15))
    
    def _create_vulnerabilities_section(self, parent):
        """Cria seção de vulnerabilidades"""
        vuln_frame = tk.Frame(parent, bg='#1a2b3c', relief='flat', bd=0)
        vuln_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(
            vuln_frame,
            text="Relatório de Segurança",
            font=('Arial', 14, 'bold'),
            bg='#1a2b3c',
            fg='#ffffff'
        ).pack(anchor='w', pady=(10, 5))
        
        vuln_text = tk.Text(
            vuln_frame,
            font=('Arial', 9),
            fg='#e0e6ed',
            bg='#1a2b3c',
            wrap=tk.WORD,
            width=70,
            height=8,
            relief='flat',
            borderwidth=0
        )
        vuln_text.pack(fill='both', padx=10, pady=(0, 10))
        vuln_text.insert('1.0', self.scan_data['vulnerabilities'])
        vuln_text.config(state='disabled')
    
    def _create_vulnerable_devices_section(self, parent):
        """Cria seção de dispositivos vulneráveis - ATUALIZADA"""
        if not self.scan_data.get('vulnerable_devices'):
            return
            
        devices_frame = tk.Frame(parent, bg='#1a2b3c', relief='flat', bd=0)
        devices_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(
            devices_frame,
            text="Dispositivos com Vulnerabilidades",
            font=('Arial', 14, 'bold'),
            bg='#1a2b3c',
            fg='#ffffff'
        ).pack(anchor='w', pady=(10, 5))
        
        devices_text = tk.Text(
            devices_frame,
            font=('Arial', 8),
            fg='#f39c12',
            bg='#1a2b3c',
            wrap=tk.WORD,
            width=70,
            height=6,
            relief='flat',
            borderwidth=0
        )
        devices_text.pack(fill='both', padx=10, pady=(0, 10))
        
        devices_report = ""
        for device in self.scan_data['vulnerable_devices']:
            device_type = device.get('device_type', 'Desconhecido')
            devices_report += f"IP: {device['ip']}\n"
            devices_report += f"Hostname: {device['hostname']}\n"
            devices_report += f"Tipo: {device_type}\n"  # ← NOVA LINHA
            devices_report += f"Portas abertas: {device['open_ports']}\n"
            devices_report += f"Riscos: {', '.join(device['risks'])}\n"
            devices_report += "─" * 60 + "\n\n"
        
        devices_text.insert('1.0', devices_report)
        devices_text.config(state='disabled')
    
    def _create_recommendations_section(self, parent):
        """Cria seção de recomendações"""
        recommendations_frame = tk.Frame(parent, bg='#1a2b3c', relief='flat', bd=0)
        recommendations_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(
            recommendations_frame,
            text="Recomendações de Segurança",
            font=('Arial', 14, 'bold'),
            bg='#1a2b3c',
            fg='#ffffff'
        ).pack(anchor='w', pady=(10, 5))
        
        rec_text = tk.Text(
            recommendations_frame,
            font=('Arial', 9),
            fg='#2ecc71',
            bg='#1a2b3c',
            wrap=tk.WORD,
            width=70,
            height=6,
            relief='flat',
            borderwidth=0
        )
        rec_text.pack(fill='both', padx=10, pady=(0, 10))
        
        recommendations = """
• FECHAR PORTAS DESNECESSÁRIAS: Desative serviços que não estão em uso
• ATUALIZAR SISTEMAS: Mantenha todos os dispositivos atualizados
• USAR FIREWALL: Configure firewall em todos os dispositivos
• SENHAS FORTES: Use senhas complexas e únicas
• REDE SEGMENTADA: Separe dispositivos críticos em VLANs diferentes
• MONITORAMENTO CONTÍNUO: Use ferramentas de monitoramento de rede
• BACKUP REGULAR: Faça backup dos dados importantes
• VPN PARA ACESSO REMOTO: Use VPN em vez de abrir portas diretamente
"""
        rec_text.insert('1.0', recommendations)
        rec_text.config(state='disabled')
    
    def _create_action_buttons(self, parent):
        """Cria botões de ação"""
        buttons_frame = ttk.Frame(parent, style='Modern.TFrame')
        buttons_frame.pack(fill='x', pady=20)
        
        # Botão Gerar Relatório
        report_btn = tk.Button(
            buttons_frame,
            text="📄 Salvar Relatório",
            font=('Arial', 10, 'bold'),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=10,
            command=self.controller.save_report
        )
        report_btn.pack(side='left', padx=5)
        
        # Botão Nova Varredura
        rescan_btn = tk.Button(
            buttons_frame,
            text="🔍 Refazer Varredura",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=10,
            command=self.controller.start_scan
        )
        rescan_btn.pack(side='left', padx=5)
        
        # Botão Voltar ao Início
        home_btn = tk.Button(
            buttons_frame,
            text="🏠 Voltar ao Início",
            font=('Arial', 10, 'bold'),
            bg='#7f8c8d',
            fg='white',
            padx=20,
            pady=10,
            command=self.controller.show_home
        )
        home_btn.pack(side='left', padx=5)