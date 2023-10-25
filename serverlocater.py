import socket
import requests
import tkinter as tk
from tkinter import ttk

class HostingProviderApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Hosting Provider Detector")
        
        self.domain_label = ttk.Label(self, text="Enter Domain:")
        self.domain_label.pack(pady=10)

        self.domain_entry = ttk.Entry(self)
        self.domain_entry.pack(pady=10, padx=20)

        self.submit_button = ttk.Button(self, text="Submit", command=self.detect_hosting)
        self.submit_button.pack(pady=10)

        self.result_text = tk.Text(self, height=15, width=60)
        self.result_text.pack(pady=10, padx=20)

    def detect_hosting(self):
        domain = self.domain_entry.get()
        if not domain:
            return

        self.result_text.delete(1.0, tk.END)
        
        try:
            ip = socket.gethostbyname(domain)
            self.result_text.insert(tk.END, f"IP Address: {ip}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error Resolving Domain: {e}\n")
            return
        
        try:
            response = requests.get(f'http://{domain}', timeout=5)
            if "server" in response.headers:
                server = response.headers["server"]
                if "cloudflare" in server.lower():
                    self.result_text.insert(tk.END, f"CDN/Proxy: Cloudflare\n")
                else:
                    self.result_text.insert(tk.END, f"Server: {server}\n")
            else:
                self.result_text.insert(tk.END, "Server header not found. Cannot determine CDN or proxy.\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error Fetching Details: {e}\n")
        
        self.get_ip_location(ip)

    def get_ip_location(self, ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
            data = response.json()
            location_info = f"Location: {data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}\n"
            org_info = f"Organization: {data.get('org', 'Unknown')}\n"
            self.result_text.insert(tk.END, location_info)
            self.result_text.insert(tk.END, org_info)
        except Exception as e:
            self.result_text.insert(tk.END, f"Error Fetching IP Location: {e}\n")

if __name__ == "__main__":
    app = HostingProviderApp()
    app.mainloop()

