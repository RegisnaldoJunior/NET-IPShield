import socket
import requests
import subprocess
import platform
import re
import datetime

class NetworkScanner:
    def __init__(self):
        self.scan_data = {}
    
    def get_public_ip(self):
        """Obtém o IP público"""
        try:
            response = requests.get('https://api.ipify.org', timeout=10)
            return response.text
        except:
            return "Não disponível"
    
    def scan_network_comprehensive(self):
        """Método COMPLETO para escanear rede"""
        devices = []
        
        try:
            print("🛰️ Iniciando scan COMPLETO de rede...")
            
            # 1. IP local
            local_ip = self.get_local_ip()
            devices.append({"ip": local_ip, "hostname": socket.gethostname(), "type": "Local"})
            print(f"✅ IP local: {local_ip}")
            
            # 2. Gateway
            gateway = self.get_gateway()
            if gateway and gateway not in [d["ip"] for d in devices]:
                devices.append({"ip": gateway, "hostname": "Gateway", "type": "Router"})
                print(f"✅ Gateway: {gateway}")
            
            # 3. Tabela ARP (dispositivos ativos)
            arp_devices = self.get_arp_direct()
            devices.extend(arp_devices)
            print(f"✅ ARP: {len(arp_devices)} dispositivos")
            
            # 4. SCAN DE REDE ATIVO
            network_devices = self.active_network_scan()
            devices.extend(network_devices)
            print(f"✅ Scan ativo: {len(network_devices)} dispositivos")
            
            # Remover duplicatas
            unique_devices = []
            seen_ips = set()
            for device in devices:
                if device["ip"] not in seen_ips:
                    unique_devices.append(device)
                    seen_ips.add(device["ip"])
            
            print(f"🎯 Total de dispositivos únicos: {len(unique_devices)}")
            
            return unique_devices
            
        except Exception as e:
            print(f"❌ Erro no scan completo: {e}")
            return devices

    def advanced_network_scan(self):
        """Scan avançado com detecção de tipos de dispositivos"""
        devices = self.scan_network_comprehensive()
        
        # Detecta tipos de dispositivos baseado em portas abertas
        for device in devices:
            device["device_type"] = self.detect_device_type(device["ip"])
        
        return devices

    def detect_device_type(self, ip):
        """Tenta detectar o tipo de dispositivo baseado nas portas abertas"""
        common_ports = {
            "Router": [80, 443, 22, 23, 53],
            "Windows": [135, 139, 445, 3389, 49152],
            "Linux/Unix": [22, 111, 631, 2049, 5432],
            "Printer": [80, 443, 515, 631, 9100],
            "Camera IP": [80, 443, 554, 8554, 8000],
            "IoT/Smart": [80, 443, 1883, 8883, 8080],
            "NAS/Storage": [21, 22, 80, 443, 2049, 3260],
            "Web Server": [80, 443, 8080, 8443],
            "Database": [1433, 3306, 5432, 27017]
        }
        
        open_ports_for_device = []
        
        # Testa portas rapidamente
        for device_type, ports in common_ports.items():
            for port in ports[:3]:  # Testa apenas 3 portas por tipo para velocidade
                if self.check_port(ip, port, 0.3):  # Timeout menor
                    open_ports_for_device.append(port)
                    # Se encontrou porta característica, já retorna
                    if self.is_characteristic_port(port, device_type):
                        return device_type
        
        # Se não detectou por porta característica, faz inferência
        return self.infer_device_type(open_ports_for_device)

    def is_characteristic_port(self, port, device_type):
        """Verifica se é uma porta característica do dispositivo"""
        characteristic_ports = {
            "Router": [53, 23],           # DNS, Telnet
            "Windows": [445, 3389],       # SMB, RDP
            "Linux/Unix": [22, 111],      # SSH, RPC
            "Printer": [515, 9100],       # LPR, JetDirect
            "Camera IP": [554, 8554],     # RTSP
            "IoT/Smart": [1883, 8883],    # MQTT
            "NAS/Storage": [2049, 3260],  # NFS, iSCSI
            "Database": [1433, 3306]      # SQL Server, MySQL
        }
        
        return port in characteristic_ports.get(device_type, [])

    def infer_device_type(self, open_ports):
        """Infere o tipo de dispositivo baseado nas portas abertas"""
        if not open_ports:
            return "Desconhecido"
        
        port_rules = [
            (["53", "23"], "Router"),
            (["445", "3389", "135"], "Windows"),
            (["22", "111", "2049"], "Linux/Unix"),
            (["515", "631", "9100"], "Printer"),
            (["554", "8554", "8000"], "Camera IP"),
            (["1883", "8883", "8080"], "IoT/Smart"),
            (["2049", "3260", "21"], "NAS/Storage"),
            (["80", "443", "8080"], "Web Server"),
            (["1433", "3306", "5432"], "Database")
        ]
        
        for ports, device_type in port_rules:
            if any(str(port) in ports for port in open_ports):
                return device_type
        
        return "Dispositivo de Rede"

    def active_network_scan(self):
        """Scan ativo de rede - similar ao NMAP"""
        devices_found = []
        
        try:
            local_ip = self.get_local_ip()
            network_prefix = ".".join(local_ip.split(".")[:3])  # ex: 192.168.1
            
            print(f"🔍 Escaneando rede {network_prefix}.0/24...")
            
            # Portas comuns para testar conectividade
            test_ports = [80, 443, 22, 135, 445, 3389]
            
            # Escaneia os primeiros 50 IPs (para não demorar muito)
            for i in range(1, 255):
                ip = f"{network_prefix}.{i}"
                
                # Pula o IP local e gateway
                if ip == local_ip or ip == self.get_gateway():
                    continue
                
                # Testa se o IP está ativo
                if self.is_host_alive(ip, test_ports):
                    try:
                        hostname = self.get_hostname_simple(ip)
                        devices_found.append({
                            "ip": ip, 
                            "hostname": hostname, 
                            "type": "Network"
                        })
                        print(f"✅ Host ativo: {ip} ({hostname})")
                    except:
                        devices_found.append({
                            "ip": ip, 
                            "hostname": "Desconhecido", 
                            "type": "Network"
                        })
                        print(f"✅ Host ativo: {ip} (Desconhecido)")
        
        except Exception as e:
            print(f"❌ Erro no scan ativo: {e}")
        
        return devices_found

    def is_host_alive(self, ip, ports, timeout=1):
        """Verifica se um host está ativo testando múltiplas portas"""
        for port in ports:
            if self.check_port(ip, port, timeout):
                return True
        
        # Se nenhuma porta comum responde, tenta ping ICMP
        return self.ping_host(ip)

    def ping_host(self, ip, timeout=1):
        """Faz ping no host sem abrir janela"""
        try:
            if platform.system().lower() == "windows":
                # CONFIGURAÇÃO PARA EVITAR JANELAS
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', str(timeout * 1000), ip],
                    capture_output=True,
                    text=True,
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                return result.returncode == 0
            else:
                # Linux/Mac - não precisa esconder janela
                result = subprocess.run(
                    ['ping', '-c', '1', '-W', str(timeout), ip],
                    capture_output=True,
                    text=True
                )
                return result.returncode == 0
        except:
            return False

    def get_arp_direct(self):
        """Obtém dispositivos da tabela ARP sem abrir janela"""
        devices = []
        
        try:
            # CONFIGURAÇÃO PARA EVITAR JANELAS
            if platform.system().lower() == "windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                creationflags = subprocess.CREATE_NO_WINDOW
            else:
                startupinfo = None
                creationflags = 0
            
            result = subprocess.run(
                ['arp', '-a'],
                capture_output=True,
                text=True,
                encoding='cp850',
                startupinfo=startupinfo,
                creationflags=creationflags
            )
            
            output = result.stdout
            
            # Divide por interfaces
            interfaces = output.split('Interface:')
            for interface in interfaces:
                if not interface.strip():
                    continue
                    
                lines = interface.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Tenta diferentes padrões de parsing
                    ip = self.extract_ip_from_line(line)
                    if ip and self.is_valid_ip(ip):
                        hostname = self.get_hostname_simple(ip)
                        devices.append({
                            "ip": ip, 
                            "hostname": hostname, 
                            "type": "Network"
                        })
            
        except Exception as e:
            print(f"❌ Erro no ARP direto: {e}")
        
        return devices
    
    def extract_ip_from_line(self, line):
        """Extrai IP de uma linha do arp -a"""
        # Padrões comuns no Windows
        patterns = [
            r'(\d+\.\d+\.\d+\.\d+)\s+',  # IP no início
            r'\s+(\d+\.\d+\.\d+\.\d+)\s+',  # IP no meio
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                ip = match.group(1)
                # Verifica se é um IP válido para rede
                if (ip.startswith('192.168.') or 
                    ip.startswith('10.') or 
                    ip.startswith('172.') or
                    ip.startswith('169.254.')):
                    return ip
        
        return None
    
    def scan_vulnerabilities(self, devices):
        """Escaneia portas vulneráveis nos dispositivos"""
        vulnerable_devices = []
        
        # Portas comuns e seus riscos
        common_ports = {
            21: "FTP - Transferência não criptografada",
            22: "SSH - Acesso remoto (verificar autenticação)",
            23: "Telnet - Protocolo inseguro",
            80: "HTTP - Tráfego não criptografado",
            443: "HTTPS - Geralmente seguro",
            135: "RPC - Potencial vulnerabilidade Windows",
            139: "NetBIOS - Compartilhamento de arquivos",
            445: "SMB - Compartilhamento Windows (eternalblue)",
            1433: "SQL Server - Banco de dados",
            1434: "SQL Server - Browser",
            3306: "MySQL - Banco de dados",
            3389: "RDP - Área de trabalho remota",
            5432: "PostgreSQL - Banco de dados",
            5900: "VNC - Acesso remoto",
            8080: "HTTP Alternativo - Serviço web",
            8443: "HTTPS Alternativo - Geralmente seguro"
        }
        
        print("🔍 Escaneando portas vulneráveis...")
        
        # Escaneia apenas alguns dispositivos principais para não demorar muito
        scan_targets = devices[:10]  # Limita a 10 dispositivos para teste
        
        for device in scan_targets:
            ip = device["ip"]
            print(f"📡 Escaneando {ip}...")
            
            open_ports = []
            risks = []
            
            # Testa portas comuns
            for port, description in common_ports.items():
                if self.check_port(ip, port):
                    open_ports.append(port)
                    
                    # Classifica o risco
                    if port in [21, 23, 135, 139, 445]:
                        risks.append(f"ALTO RISCO: Porta {port} ({description})")
                    elif port in [22, 3389, 5900]:
                        risks.append(f"RISCO MÉDIO: Porta {port} ({description})")
                    else:
                        risks.append(f"BAIXO RISCO: Porta {port} ({description})")
            
            if open_ports:
                vulnerable_devices.append({
                    "ip": ip,
                    "hostname": device["hostname"],
                    "device_type": device.get("device_type", "Desconhecido"),
                    "open_ports": open_ports,
                    "risks": risks
                })
                print(f"⚠️  {ip} tem {len(open_ports)} portas abertas")
        
        return vulnerable_devices
    
    def check_port(self, ip, port, timeout=1):
        """Verifica se uma porta está aberta"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((ip, port))
                return result == 0
        except:
            return False
    
    def generate_vulnerability_report(self, vulnerable_devices, total_devices):
        """Gera relatório de vulnerabilidades"""
        report = ""
        
        if not vulnerable_devices:
            report = "✅ Nenhuma vulnerabilidade crítica encontrada.\n"
            report += "🔒 Sua rede parece estar bem protegida."
        else:
            report = f"⚠️  FORAM ENCONTRADAS VULNERABILIDADES!\n\n"
            report += f"📊 {len(vulnerable_devices)} de {total_devices} dispositivos analisados têm portas abertas.\n\n"
            report += "🔴 RISCOS IDENTIFICADOS:\n"
            
            high_risk_count = 0
            medium_risk_count = 0
            
            for device in vulnerable_devices:
                for risk in device["risks"]:
                    if "ALTO RISCO" in risk:
                        high_risk_count += 1
                    elif "RISCO MÉDIO" in risk:
                        medium_risk_count += 1
            
            if high_risk_count > 0:
                report += f"• {high_risk_count} vulnerabilidades de ALTO RISCO\n"
            if medium_risk_count > 0:
                report += f"• {medium_risk_count} vulnerabilidades de RISCO MÉDIO\n"
            
            report += "\n💡 RECOMENDAÇÕES:\n"
            report += "• Feche portas desnecessárias\n"
            report += "• Use firewall nos dispositivos\n"
            report += "• Atualize sistemas e aplicativos\n"
            report += "• Use senhas fortes\n"
            report += "• Considere usar VPN"
        
        return report
    
    def get_gateway(self):
        """Obtém o gateway padrão sem abrir janela"""
        try:
            if platform.system().lower() == "windows":
                # CONFIGURAÇÃO PARA EVITAR JANELAS
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                
                result = subprocess.run(
                    ['ipconfig'], 
                    capture_output=True, 
                    text=True, 
                    encoding='cp850',
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line or 'Gateway Padrão' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            gateway = parts[1].strip()
                            # FILTRA APENAS IPv4
                            if gateway and gateway != '' and self.is_valid_ip(gateway):
                                return gateway
            return None
        except:
            return None
    
    def get_local_ip(self):
        """Obtém o IP local"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def is_valid_ip(self, ip):
        """Verifica se é um IP válido"""
        try:
            socket.inet_aton(ip)
            if (ip.startswith('0.') or ip.startswith('127.') or 
                ip.startswith('224.') or ip.startswith('239.') or 
                ip.startswith('255.') or ip == '0.0.0.0'):
                return False
            return True
        except:
            return False
    
    def get_hostname_simple(self, ip):
        """Tenta obter hostname de forma simples"""
        try:
            socket.setdefaulttimeout(1)
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Desconhecido"