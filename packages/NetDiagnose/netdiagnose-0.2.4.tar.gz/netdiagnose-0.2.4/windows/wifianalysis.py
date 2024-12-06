import psutil
import subprocess
import re

# Function to get the wireless interface name on Windows
def get_wireless_interface():
    interfaces = psutil.net_if_addrs()
    for interface_name in interfaces:
        if 'Wi-Fi' in interface_name or 'wlan' in interface_name:
            return interface_name
    return None

# Function to retrieve Wi-Fi interface details using netsh
def get_netsh_interface_info():
    interface = get_wireless_interface()
    if not interface:
        return "No wireless interface found."
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interface"], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi interface info via netsh: {e}"

# Function to retrieve signal strength and link quality using netsh
def get_wifi_signal_strength():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interface"], universal_newlines=True)
        for line in result.splitlines():
            if "Signal" in line:
                return line.strip()
    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi signal strength via netsh: {e}"

# Function to retrieve available Wi-Fi networks info using netsh
def get_wifi_info():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=bssid"], universal_newlines=True)
        networks = []
        channels = {}
        chn = []
        
        current_network = {}
        for line in result.splitlines():
            line = line.strip()
            if line.startswith("SSID"):
                if current_network:
                    networks.append(current_network)
                current_network = {"SSID": line.split(": ")[1]}
            elif "Signal" in line:
                current_network["Signal"] = line.split(": ")[1]
            elif "Authentication" in line:
                current_network["Security"] = line.split(": ")[1]
            elif "Channel" in line:
                channel = line.split(": ")[1]
                current_network["Channel"] = channel
                channels[channel] = channels.get(channel, 0) + 1
        if current_network:
            networks.append(current_network)

        network_info = [f"SSID: {n['SSID']}, Signal: {n.get('Signal', 'N/A')}, Security: {n.get('Security', 'N/A')}, Channel: {n['Channel']}" for n in networks]
        channel_info = [f"Channel {channel}: {count} networks" for channel, count in channels.items()]

        return [network_info, channel_info]

    except subprocess.CalledProcessError as e:
        return f"Error retrieving Wi-Fi info via netsh: {e}"
