import socket
import ssl
import subprocess
from datetime import datetime

class NetworkSecurityCheck:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    @staticmethod
    def is_nmap_installed():
        # Check if Nmap is installed (useful if running Windows with Nmap installed)
        try:
            result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def nmap_scan(self, port):
        if not self.is_nmap_installed():
            return "Nmap is not installed on this system."
        try:
            result = subprocess.run(["nmap", "-Pn", "-p", str(port), self.target_ip], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error running nmap: {e}"

    def firewall_detection(self, port):
        # Simple socket connection test for open/closed ports (no raw packet manipulation)
        try:
            with socket.create_connection((self.target_ip, port), timeout=2) as s:
                return f"Port {port} is open and reachable."
        except (socket.timeout, ConnectionRefusedError):
            return f"Port {port} seems closed or blocked by a firewall."
        except Exception as e:
            return f"Error in firewall detection: {e}"

    def ssl_tls_inspection(self, hostname=None, port=443):
        # SSL/TLS certificate inspection for HTTPS ports
        hostname = hostname or self.target_ip
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
            with socket.create_connection((self.target_ip, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl_version"] = ssock.version()
                    common_names = [entry[1] for entry in cert.get('subject', []) if entry[0] == 'commonName']
                    subject_alt_names = [san[1] for san in cert.get('subjectAltName', [])]

                    if hostname in common_names or hostname in subject_alt_names:
                        result["certificate_valid"] = True
                    result["issuer"] = ', '.join(f"{name[0]}={name[1]}" for name in cert.get("issuer", []))
                    result["expiry_date"] = cert.get("notAfter")
                    # Convert expiry_date to a datetime object for easier processing
                    if result["expiry_date"]:
                        result["expiry_date"] = datetime.strptime(result["expiry_date"], "%b %d %H:%M:%S %Y %Z")
        except ssl.SSLCertVerificationError as e:
            result["error"] = f"SSL Certificate Verification Error: {e}"
        except Exception as e:
            result["error"] = f"Unexpected error: {e}"

        return result

# Example usage
target_ip = "8.8.8.8"
security_check = NetworkSecurityCheck(target_ip)

print("Nmap Scan (if available):")
print(security_check.nmap_scan(80))

print("\nFirewall Detection:")
print(security_check.firewall_detection(80))

print("\nSSL/TLS Inspection:")
print(security_check.ssl_tls_inspection())
