import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data():
    try:
        tree.delete(*tree.get_children())

        url = "https://books.toscrape.com/"
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        data = []

        for book in books:
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p["class"][1]

            data.append([name, price, rating])

            tree.insert(
                "",
                tk.END,
                values=(name, price, rating)
            )

        df = pd.DataFrame(
            data,
            columns=["Product", "Price", "Rating"]
        )

        df.to_csv("products.csv", index=False)

        status_label.config(
            text=f"{len(data)} Products Scraped & Saved"
        )

        messagebox.showinfo(
            "Success",
            "Data saved to products.csv"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

root = tk.Tk()
root.title("Product Scraper")
root.geometry("900x600")

title = tk.Label(
    root,
    text="WEB SCRAPING DASHBOARD",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

scrape_btn = tk.Button(
    root,
    text="Start Scraping",
    command=scrape_data,
    bg="green",
    fg="white"
)
scrape_btn.pack(pady=10)

columns = ("Product", "Price", "Rating")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250)

tree.pack(fill="both", expand=True)

status_label = tk.Label(
    root,
    text="Ready"
)
status_label.pack(pady=10)

root.mainloop()