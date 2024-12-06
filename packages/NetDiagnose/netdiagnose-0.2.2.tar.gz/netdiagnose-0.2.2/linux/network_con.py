import subprocess
import socket



def ping_test(destination):
    try:
        # Ping the destination
        result = subprocess.run(["ping", "-c", "10", "8.8.8.8"], capture_output=True, text=True, timeout=100)
        if result.returncode == 0:
            pass
            #print(f"Ping to {destination} successful.")
        else:
            return(f"Failed to ping to {destination}.")
        return(f"Ping to {destination} succesfull \n" + result.stdout)
    except subprocess.TimeoutExpired:
        return(f"Ping to {destination} timed out.")


def dns_lookup(domain):
    try:
        # DNS lookup for the given domain
        #print(f"DNS lookup for {domain}:")
        ip_address = socket.gethostbyname(domain)
        return(f"{domain} has IP address {ip_address}")
    except socket.gaierror:
        return(f"Failed to resolve DNS for {domain}")

def trace_route(destination):
    try:
        #print(f"\nTracing route to {destination}:")
        result = subprocess.run(["traceroute", destination], capture_output=True, text=True, timeout=30)
        return(result.stdout)
    except subprocess.TimeoutExpired:
        return(f"\nTracing route to {destination} timed out.")