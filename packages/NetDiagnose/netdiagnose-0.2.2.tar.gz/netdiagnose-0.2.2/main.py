import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr
import tkinter as tk
import sys
import customtkinter as ctk
from tkinter import Text, simpledialog, messagebox

# Allow import of modules from both Linux and Windows directories
sys.path.append('linux')
sys.path.append('windows')

if sys.platform == 'linux':
    from linux.network_con import ping_test, dns_lookup, trace_route
    from linux.speedtest import get_server, get_downspeed, get_upspeed, get_ping, get_jitter
    from linux.network_interface import network_interfaces_info
    from linux.wifianalysis import get_iw_info, get_wifi_signal_strength, get_wifi_info
    from linux.portscan import port_scan
    from linux.security import NetworkSecurityCheck
    from linux.logs_reporting import ReportManager
elif sys.platform == 'win32':
    from windows.network_con import ping_test, dns_lookup, trace_route
    from windows.speedtest import speed_test
    from windows.network_interface import network_interfaces_info
    from windows.wifianalysis import get_wireless_interface, get_iw_info, get_wifi_signal_strength, get_wifi_info
    from windows.portscan import port_scan
    from windows.security import NetworkSecurityCheck

class NetworkDiagnoseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NetDiagnose")
        self.geometry("1300x900")
        self.resizable(False, False)  # Prevent resizing

        self.report_manager = ReportManager()  # Initialize ReportManager

        # Set up the grid layout
        self.configure_grid()
        self.create_widgets()

    def configure_grid(self):
        self.columnconfigure(0, weight=0)  # Button frame
        self.columnconfigure(1, weight=1)  # Output area
        self.columnconfigure(2, weight=0)  # System info column
        self.rowconfigure(0, weight=1)

    def create_widgets(self):
        # Create a side panel for the buttons
        button_frame = ctk.CTkFrame(self, width=200)
        button_frame.grid(row=0, column=0, sticky="ns")

        # Create an output area for displaying diagnostics
        self.output_text = Text(self, wrap="word", width=50, height=30, font=("Monospace", 10), bg="#2B2B2B", fg="white", bd=0)
        self.output_text.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Create a system info panel
        system_info_frame = ctk.CTkFrame(self, width=700, fg_color="#2B2B2B")
        system_info_frame.grid(row=0, column=2, sticky="ns", padx=5, pady=5)

        # Display basic system information
        self.system_info_label = ctk.CTkLabel(system_info_frame, text="System Information", font=("Monospace", 14, "bold"))
        self.system_info_label.pack(pady=5)

        # Retrieve and display system information
        self.system_info_text = Text(system_info_frame, wrap="word", width=30, height=30, font=("Monospace", 10), bg="#2B2B2B", fg="white", bd=0)
        self.system_info_text.pack(padx=5, pady=5)
        self.display_system_info()

        # Set welcome message
        self.output_text.insert(tk.END, "Welcome to NetDiagnose, A network diagnostic assistant that will help you diagnose your network\nby providing you all the information you need about your network")

        # Diagnostic buttons
        buttons = [
            ("Network Information", self.network_information),
            ("Speed Test", self.run_speed_test),
            ("Wi-Fi Analysis", self.wifi_analysis),
            ("Port Scan", self.run_port_scan),
            ("Security Check", self.security_check),
            ("Run Full Report", self.log_save_email)
        ]

        for i, (name, command) in enumerate(buttons):
            button = ctk.CTkButton(button_frame, text=name, command=command, width=180, height=35)
            button.grid(row=i, column=0, padx=10, pady=5, sticky="ew")

        # Exit button
        exit_button = ctk.CTkButton(button_frame, text="Exit", command=self.quit, width=180, height=35)
        exit_button.grid(row=len(buttons) + 1, column=0, padx=10, pady=10, sticky="ew")

    def display_system_info(self):
        """Fetch and display system information in the third column."""
        network = network_interfaces_info()
        interface = network[0]
        address = network[1]

        for info in interface:
            self.system_info_text.insert(tk.END, f"{info}")

        for addr in address:
            self.system_info_text.insert(tk.END, f"{addr}")

    def append_to_output(self, text):
        """Append text to the output area and log it."""
        self.report_manager.append_to_report(text)  # Log to report
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    # Diagnostic functions
    def network_information(self):
        self.output_text.delete("1.0", tk.END)
        ip = self.custom_prompt_input("Enter IP (default: 8.8.8.8):", "8.8.8.8")
        dns = self.custom_prompt_input("Enter DNS (default: www.google.com):", "www.google.com")
        route = self.custom_prompt_input("Enter Route (default: 8.8.8.8):", "8.8.8.8")

        self.append_to_output(" Running Network Information Tests...\n")
        self.output_text.update_idletasks()  # Force the GUI to update

        self.append_to_output(f" Ping Test: {ping_test(ip)}")
        self.output_text.update_idletasks()
        self.append_to_output(f" DNS Lookup for {dns}")
        self.append_to_output(f" DNS Lookup: {dns_lookup(dns)}")
        self.output_text.update_idletasks()
        self.append_to_output(f" Tracing Route to {route}\n")
        self.append_to_output(f" Trace Route: {trace_route(route)}")    
       
    def run_speed_test(self):
        self.output_text.delete("1.0", tk.END)
        self.append_to_output(" Getting Server Info")
        self.output_text.update_idletasks()
        server = get_server()
        if type(server) == 'String':
            self.append_to_output(f" Server: {server}")
        else:
            self.append_to_output(f" Server:{server['sponsor']}, Location: {server['name']} in {server['country']}")

        self.append_to_output(" Running Speed Test...")
        self.output_text.update_idletasks()
        self.append_to_output(f" Calculating download speed")
        self.output_text.update_idletasks()
        download = get_downspeed()
        self.append_to_output(f" Download Speed {download: .2f} mbps \n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Calculating Upload speed\n")
        self.output_text.update_idletasks()
        upload = get_upspeed()
        self.append_to_output(f" Upload Speed {upload: .2f} mbps \n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Calculating Ping and Jitter speed\n")
        self.output_text.update_idletasks()
        ping = get_ping()
        self.append_to_output(f" Ping {ping: .2f} ms ")
        self.output_text.update_idletasks()
        jitter = get_jitter()
        self.append_to_output(f" Calculating Jitter")
        self.output_text.update_idletasks()
        self.append_to_output(f" Jitter {jitter} ms")

    def wifi_analysis(self):
        self.output_text.delete("1.0", tk.END)
        self.append_to_output(" Running Wi-Fi Analysis...")
        self.output_text.update_idletasks()
        self.append_to_output(f" Signal Strength: {get_wifi_signal_strength()} \n")
        self.output_text.update_idletasks()
        self.append_to_output(f" Interface Info: {get_iw_info()}")
        self.output_text.update_idletasks()
        netchan = get_wifi_info()
        networks = netchan[0]
        channels = netchan[1]
        self.append_to_output(f"\n Networks: ")
        for n in networks:
              self.append_to_output(f"{n}")
        self.output_text.update_idletasks()
        self.append_to_output("\n\n Channels info:")
        for c in channels:
            self.append_to_output(f"{c}")
   
    def run_port_scan(self):
        self.output_text.delete("1.0", tk.END)
        self.append_to_output(" Running Port Scan...")
        self.output_text.update_idletasks()
       
        ports = port_scan()
        used = ports[0]
        free = ports[1]
        self.append_to_output(f" Used Ports: ")
        for u in used:
            self.append_to_output(f" {u}")
        self.append_to_output(f" \n\n Free ports:")
        for f in free:
            self.append_to_output(f" {f}")
    def security_check(self):
        self.output_text.delete("1.0", tk.END)
        target_ip = self.custom_prompt_input(" Enter Target IP (default: 8.8.8.8):", "8.8.8.8")
        port = int(self.custom_prompt_input(" Enter Port (default: 300):", "300"))
        hostname = self.custom_prompt_input(" Enter Hostname (default: www.google.com):", "www.google.com")

        self.append_to_output(" Running Security Check...")
        self.append_to_output(f" Nmap Scan: {NetworkSecurityCheck.nmap_scan(target_ip, port)}")
        self.output_text.update_idletasks()
        self.append_to_output(f" Firewall Detection: {NetworkSecurityCheck.firewall_detection(target_ip, port)}")
        self.output_text.update_idletasks()
        #self.append_to_output(f"Inspeacting SSL/TLS")
        #self.output_text.update_idletasks()
        #self.append_to_output(f" SSL/TLS Inspection: {NetworkSecurityCheck.ssl_t

    def log_save_email(self):
        """Prompt to either save or email the report."""
        self.output_text.delete("1.0", tk.END)
        self.append_to_output("Saving Logs..")
        self.report_manager.save_report()
        choice = messagebox.askyesno("Run Full Report", "Do you want to email the report? (Click 'No' to save locally)")
        if choice:
            recipient_email = self.custom_prompt_input("Email Report", "Enter recipient email:")
            if recipient_email:
                self.report_manager.email_report(recipient_email)
                
                self.append_to_output(f"Email sent succesfully to {recipient_email}")

        self.append_to_output(f"Report saved locally")       
        

    def custom_prompt_input(self, message, default):
        #Custom dialog to get user input with a default value."
        dialog = ctk.CTkToplevel(self)
        dialog.title("Input")
    
    # Get the position of the main window to center the Toplevel window
        main_window_width = self.winfo_width()
        main_window_height = self.winfo_height()
        dialog_width = 300
        dialog_height = 150

    # Calculate the center position
        x_position = self.winfo_x() + (main_window_width // 2) - (dialog_width // 2)
        y_position = self.winfo_y() + (main_window_height // 2) - (dialog_height // 2)

    # Set the position and size of the Toplevel window
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    
    # Create the input dialog contents
        label = ctk.CTkLabel(dialog, text=message)
        label.pack(pady=10)
     
        entry = ctk.CTkEntry(dialog, width=250)
        entry.pack(pady=5)
        entry.insert(0, default)
    
        def on_ok():
            dialog.user_input = entry.get()
            dialog.destroy()
    
        ok_button = ctk.CTkButton(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)
    
        dialog.user_input = default
        dialog.wait_window()
        return dialog.user_input
    
if __name__ == "__main__":
    app = NetworkDiagnoseApp()
    app.mainloop()
