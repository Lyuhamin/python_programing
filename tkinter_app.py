# tkinter_app.py

import tkinter as tk
from tkinter import messagebox
import requests

def search_product():
    product = entry.get()
    response = requests.post('http://localhost:5000/search', data={'product': product})
    
    if response.status_code == 200:
        results = response.json()
        show_results(results)
    else:
        messagebox.showerror("Error", "Failed to fetch search results.")

def show_results(results):
    results_window = tk.Toplevel(app)
    results_window.title("Search Results")

    for index, (title, link) in enumerate(results):
        result_label = tk.Label(results_window, text=f"{index + 1}. {title}")
        result_label.pack()
        result_link = tk.Label(results_window, text=link, fg="blue", cursor="hand2")
        result_link.pack()
        result_link.bind("<Button-1>", lambda e, url=link: open_url(url))

def open_url(url):
    import webbrowser
    webbrowser.open_new(url)

app = tk.Tk()
app.title("Product Search")

label = tk.Label(app, text="Enter the product name:")
label.pack()

entry = tk.Entry(app)
entry.pack()

button = tk.Button(app, text="Search", command=search_product)
button.pack()

app.mainloop()
