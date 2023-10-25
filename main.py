import os
import tkinter as tk
import subprocess

class OPMC_Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("OPMC Dashboard")

        self.create_buttons()

    def create_buttons(self):
        # Button to run app.py
        button_app = tk.Button(self.root, text="Domain Checker Tool", command=self.run_app)
        button_app.pack(pady=20)

        # Button to run domain_dns.py
        button_dns = tk.Button(self.root, text="DNS Lookup Tool", command=self.run_dns)
        button_dns.pack(pady=20)

        # Button to run serverlocater.py
        button_serverlocater = tk.Button(self.root, text="Server Locator Tool", command=self.run_serverlocater)
        button_serverlocater.pack(pady=20)

        # Button to run odoo_gui.py (this remains at the bottom)
        button_odoo = tk.Button(self.root, text="Odoo Credential Checker", command=self.run_odoo)
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
    app = OPMC_Dashboard(root)
    root.mainloop()
import os
import tkinter as tk
import subprocess

class OPMC_Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("OPMC Dashboard")

        self.create_buttons()

    def create_buttons(self):
        # Button to run app.py
        button_app = tk.Button(self.root, text="Domain Checker Tool", command=self.run_app)
        button_app.pack(pady=20)

        # Button to run domain_dns.py
        button_dns = tk.Button(self.root, text="DNS Lookup Tool", command=self.run_dns)
        button_dns.pack(pady=20)

        # Button to run serverlocater.py
        button_serverlocater = tk.Button(self.root, text="Server Locator Tool", command=self.run_serverlocater)
        button_serverlocater.pack(pady=20)

        # Button to run odoo_gui.py (this remains at the bottom)
        button_odoo = tk.Button(self.root, text="Odoo Credential Checker", command=self.run_odoo)
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
    app = OPMC_Dashboard(root)
    root.mainloop()
