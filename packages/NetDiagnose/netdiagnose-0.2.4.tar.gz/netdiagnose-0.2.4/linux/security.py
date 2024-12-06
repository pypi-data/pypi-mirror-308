import socket
import ssl
import subprocess
from scapy.all import IP, TCP, sr1

class NetworkSecurityCheck:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    @staticmethod
    def is_nmap_installed():
        try:
            result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def nmap_scan(target_ip, port):
        
        try:
            # Assuming `target_ip` and `port` are already defined in security_check
            result = subprocess.run(["nmap", "-Pn", "-p", str(port), target_ip], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error running nmap: {e}"

    def firewall_detection(target_ip, port):
        try:
            packet = IP(dst=target_ip) / TCP(dport=port, flags='S')
            response = sr1(packet, timeout=2, verbose=0)

            if response is None:
                return f"Port {port} seems filtered or blocked by a firewall."
            elif response.haslayer(TCP):
                if response.getlayer(TCP).flags == 0x12:
                    return f"Port {port} is open and reachable."
                elif response.getlayer(TCP).flags == 0x14:
                    return f"Port {port} is closed but not filtered by a firewall."
            return f"Unexpected response on port {port}."
        except PermissionError:
            return "Firewall detection requires elevated permissions (e.g., run as root)."
        except Exception as e:
            return f"Error in firewall detection: {e}"

    def ssl_tls_inspection(hostname=None, port=443, target_ip='8.8.8.8'):
        hostname = hostname or target_ip
        result = {
            "hostname": hostname,
            "ssl_version": None,
            "certificate_valid": False,
            "issuer": None,
            "expiry_date": None,
            "error": None
        }

        try:
            context = ssl.create_default_context()
            with socket.create_connection((target_ip, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl_version"] = ssock.version()
                    common_names = [entry[1] for entry in cert.get('subject', []) if entry[0] == 'commonName']
                    subject_alt_names = [san[1] for san in cert.get('subjectAltName', [])]

                    if hostname in common_names or hostname in subject_alt_names:
                        result["certificate_valid"] = True
                    result["issuer"] = ', '.join(f"{name[0]}={name[1]}" for name in cert.get("issuer", []))
                    result["expiry_date"] = cert.get("notAfter")
        except ssl.SSLCertVerificationError as e:
            result["error"] = f"SSL Certificate Verification Error: {e}"
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"

        return result
