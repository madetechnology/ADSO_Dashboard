import tkinter as tk
import requests
import hashlib
import time

# Define your Reseller ID and API Key
reseller_id = '26891'
api_key = '06397185d9b8b185da49d673ecb96187'

# Function to retrieve and display domains
def retrieve_domains():
    # Generate a unique Request ID
    request_id = hashlib.md5(f'{time.time()}{time.process_time()}'.encode()).hexdigest()

    # Create the API Signature
    signature = hashlib.md5(f'{request_id}{api_key}'.encode()).hexdigest()

    # Define the API endpoint for retrieving domains
    api_url = 'https://reseller-api.ds.network/domains'

    # Set the query parameters
    params = {
        'reseller_id': reseller_id,
    }

    # Set the HTTP headers
    headers = {
        'Api-Request-Id': request_id,
        'Api-Signature': signature,
    }

    try:
        # Send the GET request to the API
        response = requests.get(api_url, params=params, headers=headers)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and display domain names
            domains = data.get('domains', [])
            if domains:
                result_text.delete('1.0', tk.END)  # Clear previous results
                result_text.insert(tk.END, "Domain Name\n")
                for domain in domains:
                    domain_name = domain.get('name', '')
                    result_text.insert(tk.END, f"{domain_name}\n")
            else:
                result_text.delete('1.0', tk.END)
                result_text.insert(tk.END, "No domains found.")
        else:
            result_text.delete('1.0', tk.END)
            result_text.insert(tk.END, f"Failed to retrieve data. HTTP status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"An error occurred: {e}")

# Create a GUI window
window = tk.Tk()
window.title("Domain List")

# Create a button to trigger domain retrieval
retrieve_button = tk.Button(window, text="Retrieve Domains", command=retrieve_domains)
retrieve_button.pack()

# Create a text widget to display the results
result_text = tk.Text(window, height=20, width=80)
result_text.pack()

# Start the GUI event loop
window.mainloop()

