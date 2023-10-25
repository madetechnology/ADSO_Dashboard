import tkinter as tk
from tkinter import scrolledtext
import socket
import dns.resolver

# Define known IP addresses and their associated servers
known_ips = {
    "WIX": ["185.230.63.171", "185.230.63.186", "185.230.63.107"],
    "Shopify": ["23.227.38.32", "23.227.38.65", "23.227.38.34"],
    "OPMC": [
        "221.121.154.4", "116.90.60.2", "116.90.60.7", "116.90.60.53",
        "116.90.60.63", "116.90.61.74", "103.16.130.181",
        "112.213.32.35", "110.232.113.249"
    ],
}

# Define known servers associated with specific IPs
known_servers = {
    "nicer3.com": "116.90.60.2",
    "nicer.com.au": "116.90.60.7",
    "nicer.net.au": "116.90.60.53",
    "nicer.co.nz": "116.90.60.63",
    "nicer5": "103.16.130.181",
    "nicer7": "112.213.32.35",
    "nicer8": "110.232.113.249",
}

def check_known_service(ip_address):
    for service, ips in known_ips.items():
        if ip_address in ips:
            return service
    return "Unknown"

def get_server_name(ip_address):
    for server, ip in known_servers.items():
        if ip_address == ip:
            return server
    return "Unknown"

def get_dns_mx_records():
    domain_name = entry.get()
    ip_text.config(state=tk.NORMAL)
    mx_text.config(state=tk.NORMAL)
    ip_text.delete(1.0, tk.END)  # Clear previous IP results
    mx_text.delete(1.0, tk.END)  # Clear previous MX results

    try:
        # Get IP address using socket
        ip_address = socket.gethostbyname(domain_name)
        ip_text.insert(tk.END, f'IP Address for {domain_name}:\n{ip_address}\n')

        # Get MX records using dnspython
        mx_records = dns.resolver.query(domain_name, 'MX')
        if mx_records:
            mx_text.insert(tk.END, f'MX Records for {domain_name}:\n')
            for mx in mx_records:
                mx_text.insert(tk.END, f'MX Priority: {mx.preference}, Mail Server: {mx.exchange}\n')
        else:
            mx_text.insert(tk.END, 'No MX Records found.\n')

        # Check if the domain uses Gmail
        if any("google.com" in mx.exchange.to_text() for mx in mx_records):
            mx_text.insert(tk.END, '\nThe email is hosted on Gmail.\n')
        else:
            mx_text.insert(tk.END, '\nThe email is hosted on another service.\n')

        # Check if the IP matches a known service
        service = check_known_service(ip_address)
        ip_text.insert(tk.END, f'\nDomain is associated with: {service}\n')

        # Check if the IP matches a known server
        server = get_server_name(ip_address)
        ip_text.insert(tk.END, f'Server Name: {server}\n')

    except socket.gaierror:
        ip_text.insert(tk.END, 'Error: Unable to resolve the domain name.\n')

    ip_text.config(state=tk.DISABLED)
    mx_text.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("DNS and MX Record Lookup")

# Create an input field
entry_label = tk.Label(root, text="Enter Domain Name:")
entry_label.pack()
entry = tk.Entry(root)
entry.pack()

# Create a button to perform the lookup
lookup_button = tk.Button(root, text="Lookup", command=get_dns_mx_records)
lookup_button.pack()

# Create a text box for displaying IP results
ip_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=8)
ip_text.pack()
ip_text.config(state=tk.DISABLED)

# Create a text box for displaying MX results
mx_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=12)
mx_text.pack()
mx_text.config(state=tk.DISABLED)

root.mainloop()

