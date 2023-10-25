import hashlib
import time
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from datetime import datetime, timedelta

def fetch_domains():
    api_key = '06397185d9b8b185da49d673ecb96187'
    request_id = hashlib.md5((str(time.time()) + str(time.time())).encode()).hexdigest()
    signature = hashlib.md5((request_id + api_key).encode()).hexdigest()

    headers = {
        'accept': 'application/json',
        'Api-Request-Id': request_id,
        'Api-Signature': signature,
    }

    url = 'https://reseller-api.ds.network/domains'

    response = requests.get(url, headers=headers)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, dict):  # Check if data is a dictionary
                data = data.get('data', [])  # Access the 'data' key
        except json.JSONDecodeError:
            data = []  # Set data to an empty list if JSON decoding fails

        # Clear any previous data in the table
        for row in tree.get_children():
            tree.delete(row)

        # Get current date
        current_date = datetime.now()

        # Define time intervals for filtering domains
        expiry_within_next_7_days = current_date + timedelta(days=7)
        expired_within_last_7_days = current_date - timedelta(days=7)

        # Populate the table with domain data
        for domain_info in data:
            domain = domain_info.get('domain_name', 'N/A')
            expiry_date_str = domain_info.get('expiry_date', 'N/A')
            customer_id = domain_info.get('customer_id', 'N/A')

            # Parse the expiry date string into a datetime object
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%dT%H:%M:%S+00:00')
            except ValueError:
                expiry_date = None

            if expiry_date:
                # Check if the domain expires within the next 7 days or has expired in the last 7 days
                if expired_within_last_7_days <= expiry_date <= expiry_within_next_7_days:
                    tree.insert("", "end", values=(domain, expiry_date_str, customer_id))

    else:
        print(f"Error: Unable to fetch domains. Status code: {response.status_code}")

def fetch_customer_info(registrant_id):
    api_key = '06397185d9b8b185da49d673ecb96187'
    request_id = hashlib.md5((str(time.time()) + str(time.time())).encode()).hexdigest()
    signature = hashlib.md5((request_id + api_key).encode()).hexdigest()

    headers = {
        'accept': 'application/json',
        'Api-Request-Id': request_id,
        'Api-Signature': signature,
    }

    url = f'https://reseller-api.ds.network/domains/registrants/{registrant_id}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            if data.get('status') and data.get('data'):
                customer_data = data.get('data')
                name = customer_data.get('name', 'N/A')
                email = customer_data.get('email', 'N/A')
                phone = customer_data.get('phone', 'N/A')
                return f"Name: {name}\nEmail: {email}\nPhone: {phone}"
            else:
                return "Customer data not found."
        except json.JSONDecodeError:
            return "Error decoding customer data."
    elif response.status_code == 404:
        return "Customer not found (404)"
    else:
        return f"Error: Unable to fetch customer data. Status code: {response.status_code}"

def submit_registrant_id():
    registrant_id = registrant_id_entry.get()
    if registrant_id:
        customer_info = fetch_customer_info(registrant_id)
        messagebox.showinfo("Customer Info", customer_info)
    else:
        messagebox.showerror("Error", "Please enter a registrant ID.")

# Create the main window
root = tk.Tk()
root.title("Domain Info")

# Create a frame for the table
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a button to fetch domain info
fetch_button = ttk.Button(root, text="Fetch Domains", command=fetch_domains)
fetch_button.pack(pady=10)

# Create the table
tree = ttk.Treeview(frame, columns=("Domain", "Expiry Date", "Customer ID"), show="headings")
tree.heading("Domain", text="Domain")
tree.heading("Expiry Date", text="Expiry Date")
tree.heading("Customer ID", text="Customer ID")
tree.pack()

# Set column widths
tree.column("Domain", width=150)
tree.column("Expiry Date", width=150)
tree.column("Customer ID", width=100)

# Create a label and entry for registrant ID
registrant_id_label = ttk.Label(root, text="Enter Registrant ID:")
registrant_id_label.pack()
registrant_id_entry = ttk.Entry(root)
registrant_id_entry.pack()
submit_button = ttk.Button(root, text="Submit", command=submit_registrant_id)
submit_button.pack()

root.mainloop()

