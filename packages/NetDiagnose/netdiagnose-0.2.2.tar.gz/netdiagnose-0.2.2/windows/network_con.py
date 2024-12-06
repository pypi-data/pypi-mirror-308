import subprocess
import socket

def ping_test(destination):
    try:
        # Ping the destination (use "-n" for Windows instead of "-c")
        result = subprocess.run(["ping", "-n", "10", destination], capture_output=True, text=True, timeout=100)
        if result.returncode == 0:
            return f"Ping to {destination} successful \n" + result.stdout
        else:
            return f"Failed to ping {destination}."
    except subprocess.TimeoutExpired:
        return f"Ping to {destination} timed out."

def dns_lookup(domain):
    try:
        # DNS lookup for the given domain
        ip_address = socket.gethostbyname(domain)
        return f"{domain} has IP address {ip_address}"
    except socket.gaierror:
        return f"Failed to resolve DNS for {domain}"

def trace_route(destination):
    try:
        # Use "tracert" for Windows instead of "traceroute"
        result = subprocess.run(["tracert", destination], capture_output=True, text=True, timeout=30)
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"\nTracing route to {destination} timed out."
