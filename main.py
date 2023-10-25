import os
import tkinter as tk
import subprocess

class ADSO_Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ADSO Dashboard")

        # Set the dark theme
        self.bg_color = "#2E2E2E"
        self.fg_color = "#FFFFFF"
        self.root.configure(bg=self.bg_color)

        self.create_buttons()

    def create_buttons(self):
        button_style = {
            'bg': self.bg_color,
            'fg': self.fg_color,
            'activebackground': '#3E3E3E',
            'activeforeground': '#FFFFFF',
            'borderwidth': 0,
            'relief': 'flat',
            'highlightbackground': self.bg_color
        }

        # Button to run app.py
        button_app = tk.Button(self.root, text="Domain Checker Tool", command=self.run_app, **button_style)
        button_app.pack(pady=20)

        # Button to run domain_dns.py
        button_dns = tk.Button(self.root, text="DNS Lookup Tool", command=self.run_dns, **button_style)
        button_dns.pack(pady=20)

        # Button to run serverlocater.py
        button_serverlocater = tk.Button(self.root, text="Server Locator Tool", command=self.run_serverlocater, **button_style)
        button_serverlocater.pack(pady=20)

        # Button to run odoo_gui.py (this remains at the bottom)
        button_odoo = tk.Button(self.root, text="Odoo Credential Checker", command=self.run_odoo, **button_style)
        button_odoo.pack(pady=20)

    def run_app(self):
        script_path = os.path.join(os.path.dirname(__file__), "app.py")
        subprocess.Popen(["python", script_path], cwd=os.path.dirname(script_path))

    def run_dns(self):
        script_path = os.path.join(os.path.dirname(__file__), "domain_dns.py")
        subprocess.Popen(["python", script_path], cwd=os.path.dirname(script_path))

    def run_serverlocater(self):
        script_path = os.path.join(os.path.dirname(__file__), "serverlocater.py")
        subprocess.Popen(["python", script_path], cwd=os.path.dirname(script_path))

    def run_odoo(self):
        script_path = os.path.join(os.path.dirname(__file__), "odoo_gui.py")
        subprocess.Popen(["python", script_path], cwd=os.path.dirname(script_path))

if __name__ == "__main__":
    root = tk.Tk()
    app = ADSO_Dashboard(root)
    root.mainloop()
