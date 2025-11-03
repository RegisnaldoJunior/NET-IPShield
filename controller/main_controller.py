import threading
from tkinter import messagebox
import datetime
from model.network_scanner import NetworkScanner
from view.home_view import HomeView
from view.loading_view import LoadingView
from view.results_view import ResultsView

class MainController:
    def __init__(self, root):
        self.root = root
        self.scanner = NetworkScanner()
        self.current_view = None
        
    def show_home(self):
        """Mostra a página inicial"""
        if self.current_view and hasattr(self.current_view, 'stop_animation'):
            self.current_view.stop_animation()
        
        self.current_view = HomeView(self.root, self)
        self.current_view.show()
    
    def start_scan(self):
        """Inicia o scan em thread separada"""
        self.show_loading()
        scan_thread = threading.Thread(target=self.perform_scan)
        scan_thread.daemon = True
        scan_thread.start()
    
    def show_loading(self):
        """Mostra a página de loading"""
        if self.current_view and hasattr(self.current_view, 'stop_animation'):
            self.current_view.stop_animation()
        
        self.current_view = LoadingView(self.root)
        self.current_view.show()
    
    def perform_scan(self):
        """Executa o scan de rede"""
        try:
            public_ip = self.scanner.get_public_ip()
            
            # Use o método de scan avançado
            devices = self.scanner.advanced_network_scan()
            device_count = len(devices)
            
            vulnerable_devices = self.scanner.scan_vulnerabilities(devices)
            vulnerabilities = self.scanner.generate_vulnerability_report(vulnerable_devices, device_count)
            
            scan_data = {
                'public_ip': public_ip,
                'device_count': device_count,
                'vulnerabilities': vulnerabilities,
                'vulnerable_devices': vulnerable_devices,
                'devices_with_types': devices,
                'timestamp': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            self.scanner.scan_data = scan_data
            
            # CORREÇÃO: Passe os dados como argumento
            self.root.after(0, self.show_results, scan_data)
            
        except Exception as e:
            # CORREÇÃO: Passe o erro como argumento
            error_msg = str(e)
            self.root.after(0, self.show_error, error_msg)
    
    def show_results(self, scan_data):
        """Mostra a página de resultados"""
        if self.current_view and hasattr(self.current_view, 'stop_animation'):
            self.current_view.stop_animation()
        
        self.current_view = ResultsView(self.root, self, scan_data)
        self.current_view.show()
    
    def save_report(self):
        """Salva relatório em arquivo de texto"""
        try:
            filename = f"NetIPShield_Relatorio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("NET IPShield - Relatório de Segurança\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Data da análise: {self.scanner.scan_data['timestamp']}\n")
                f.write(f"IP Público: {self.scanner.scan_data['public_ip']}\n")
                f.write(f"Dispositivos encontrados: {self.scanner.scan_data['device_count']}\n\n")
                
                f.write("VULNERABILIDADES ENCONTRADAS:\n")
                f.write("-" * 40 + "\n")
                f.write(self.scanner.scan_data['vulnerabilities'] + "\n\n")
                
                if self.scanner.scan_data['vulnerable_devices']:
                    f.write("DISPOSITIVOS COM PORTAS ABERTAS:\n")
                    f.write("-" * 40 + "\n")
                    for device in self.scanner.scan_data['vulnerable_devices']:
                        f.write(f"IP: {device['ip']}\n")
                        f.write(f"Hostname: {device['hostname']}\n")
                        f.write(f"Tipo: {device.get('device_type', 'Desconhecido')}\n")
                        f.write(f"Portas abertas: {device['open_ports']}\n")
                        for risk in device['risks']:
                            f.write(f"- {risk}\n")
                        f.write("\n")
            
            messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso!\nArquivo: {filename}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o relatório:\n{str(e)}")
    
    def show_error(self, error_msg):
        """Mostra mensagem de erro"""
        messagebox.showerror("Erro", f"Ocorreu um erro durante o scan:\n{error_msg}")
        self.show_home()