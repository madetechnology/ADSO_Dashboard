import xmlrpc.client
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

def connect_to_odoo(url, database, username, api_key):
    # XML-RPC Common endpoint
    common_url = '{}/xmlrpc/2/common'.format(url)
    
    try:
        common = xmlrpc.client.ServerProxy(common_url)
        
        # Authenticate to get the user id (uid)
        uid = common.authenticate(database, username, api_key, {})
        
        # If authentication fails
        if not uid:
            return None, [], 401, "Auth failed."

        # Get the version details
        version_info = common.version()

        # XML-RPC Object endpoint
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Check if the specified modules are installed
        module_names = ['sale', 'account', 'account_accountant', 'stock']
        module_search = models.execute_kw(database, uid, api_key, 'ir.module.module', 'search',
                                          [['&', ('name', 'in', module_names), ('state', '=', 'installed')]])
        installed_modules = models.execute_kw(database, uid, api_key, 'ir.module.module', 'read', [module_search],
                                              {'fields': ['name']})
        installed_module_names = [module['name'] for module in installed_modules]
        return version_info, installed_module_names, 200, None

    except xmlrpc.client.Fault as e:
        return None, [], 500, "Server error."
    except Exception as e:
        return None, [], 503, "Connection error."

def on_submit():
    url = url_entry.get()
    database = db_entry.get()
    username = user_entry.get()
    api_key = api_key_entry.get()

    version_info, installed_modules, status_code, error_msg = connect_to_odoo(url, database, username, api_key)

    # Insert the results in the Treeview table
    modules = ['sale', 'account', 'account_accountant', 'stock']
    module_status = [int(module in installed_modules) for module in modules]
    color = 'green' if status_code == 200 else 'red'
    tree.insert("", "end", values=(url, database, username, version_info['server_version'] if version_info else '-', 
                                   *module_status, status_code, error_msg), tags=(color,))
    tree.tag_configure(color, background=color)

# GUI setup
root = tk.Tk()
root.title("Connect to Odoo")

# Entries for user input
tk.Label(root, text="Odoo URL:").grid(row=0, sticky=tk.W)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1)

tk.Label(root, text="Database Name:").grid(row=1, sticky=tk.W)
db_entry = tk.Entry(root, width=50)
db_entry.grid(row=1, column=1)

tk.Label(root, text="Username:").grid(row=2, sticky=tk.W)
user_entry = tk.Entry(root, width=50)
user_entry.grid(row=2, column=1)

tk.Label(root, text="API Key:").grid(row=3, sticky=tk.W)
api_key_entry = tk.Entry(root, width=50, show="*")
api_key_entry.grid(row=3, column=1)

tk.Button(root, text="Submit", command=on_submit).grid(row=4, columnspan=2)

# Treeview for displaying logs
columns = ('URL', 'Database', 'Username', 'Odoo Version', 'Sale', 'Account', 'Accounting', 'Inventory', 'Status', 'Error')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

