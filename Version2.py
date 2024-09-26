import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os


# Function to load user data from an external JSON file
def load_user_data():
    file_path = "user_data.json"
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


# Function to save user data to an external JSON file
def save_user_data(user_data):
    with open("user_data.json", 'w') as file:
        json.dump(user_data, file)


class Product:
    def __init__(self, name, price, description, image_path):
        self.name = name
        self.price = price
        self.description = description
        self.image_path = image_path


class Shop:
    def __init__(self):
        self.rackets = [
            Product("Yonex Astrox 99", 250, "High-performance racket for advanced players.", "Images/astrox99.PNG"),
            Product("Li-Ning Axforce 80", 200, "Great for intermediate players.", "Images/axf80.PNG"),
            Product("Victor Thrusterk9900", 220, "Powerful racket for attacking play.", "Images/VicThruster.PNG"),
            Product("Yonex Duora Z-Strike", 230, "Versatile racket for all-round play.", "Images/zstrike.PNG"),
            Product("Yonex Astrox 88D Pro", 210, "Aerodynamic design for faster swings.", "Images/88Dpro.PNG"),
            Product("Victor Jetspeed S 12", 190, "Lightweight and fast.", "Images/jetspeeds12.PNG"),
            Product("Yonex Nanoflare 800", 240, "Great control and speed.", "Images/NF800.PNG"),
            Product("Li-Ning HB 800000", 215, "Optimized for speed and power.", "Images/HB8000.PNG"),
            Product("Yonex 100zz Navy Blue", 225, "Fast and powerful.", "Images/100zzNB.PNG"),
            Product("Yonex Voltric Z-Force II", 260, "Top choice for professionals.", "Images/VZFORCE2.PNG")
        ]
        self.shoes = [
            Product("Yonex EclipsionZ ", 130, "Comfortable and durable shoes.", "Images/shoe1.PNG"),
            Product("Li-Ning Ranger 2 Shoe", 120, "Great for stability and traction.", "Images/shoe2.PNG"),
            Product("Victor A960 Shoe", 140, "Designed for speed and agility.", "Images/shoe3.PNG"),
           
            Product("Yonex SHB 65Z3 Shoe", 125, "Perfect for quick movements.", "Images/shoe6.PNG"),
            Product("Victor P9200 Shoe", 145, "Premium shoes with great support.", "Images/shoe7.PNG"),
            Product("Li-Ning Cloud Lite ", 110, "Light and breathable design.", "Images/shoe8.PNG"),
            Product("Yonex Eclipsion X2 Shoe", 150, "High cushioning for intense play.", "Images/shoe9.PNG"),
            Product("Victor A830 Shoe", 115, "Affordable and reliable.", "Images/shoe10.PNG")
        ]
        self.cart = []

    def add_to_cart(self, product_index, quantity, product_type):
        if product_type == "Rackets":
            product = self.rackets[product_index]
        else:
            product = self.shoes[product_index]
        self.cart.append((product, quantity))
        messagebox.showinfo("Added to Cart", f"Added {quantity} x {product.name} to your cart.")

    def remove_from_cart(self, cart_index):
        if 0 <= cart_index < len(self.cart):
            removed_item = self.cart.pop(cart_index)
            messagebox.showinfo("Removed from Cart", f"Removed {removed_item[0].name} from your cart.")
        else:
            messagebox.showerror("Error", "Invalid cart selection")

    def get_receipt(self):
        receipt = "Receipt:\n"
        total = 0
        for product, quantity in self.cart:
            cost = product.price * quantity
            total += cost
            receipt += f"{product.name} - ${product.price} x {quantity} = ${cost}\n"
        receipt += f"Total: ${total}"
        return receipt

    def get_cart_items(self):
        cart_details = ""
        for i, (product, quantity) in enumerate(self.cart):
            cart_details += f"{i + 1}. {product.name} - ${product.price} x {quantity}\n"
        return cart_details


class Application(tk.Tk):
    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self.title("Badminton Shop")

        # Increased the window size
        self.geometry("500x450")

        self.customer_name = tk.StringVar()
        self.selected_product_type = tk.StringVar(value="Rackets")

        self.user_data = load_user_data()  # Load user data from JSON file
        self.current_user = None

        self.start_page = self.create_start_page()
        self.login_page = self.create_login_page()  # Add login page
        self.product_page = self.create_product_page()
        self.receipt_page = self.create_receipt_page()
        self.cart_page = self.create_cart_page()

        self.show_frame(self.login_page)  # Start with the login page

    def show_frame(self, frame):
        frame.tkraise()

    def create_login_page(self):
        frame = tk.Frame(self, bg="#E3F2FD")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Username:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(frame)
        self.username_entry.pack(pady=10)

        tk.Label(frame, text="Password:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(frame, text="Login", command=self.login, bg="#64B5F6", fg="white").pack(pady=10)
        tk.Button(frame, text="Create Account", command=self.create_account, bg="#64B5F6", fg="white").pack(pady=10)

        return frame

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.user_data and self.user_data[username] == password:
            self.current_user = username
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            self.show_frame(self.start_page)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists")
        else:
            if username and password:
                self.user_data[username] = password
                save_user_data(self.user_data)
                messagebox.showinfo("Account Created", "Account successfully created!")
            else:
                messagebox.showerror("Error", "Please provide both username and password")

    def create_start_page(self):
        frame = tk.Frame(self, bg="#E3F2FD")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, text="Enter your name:", bg="#E3F2FD", font=("Arial", 14)).pack(pady=10)
        name_entry = tk.Entry(frame, textvariable=self.customer_name)
        name_entry.pack(pady=10)

        tk.Button(frame, text="Start Shopping", command=self.start_shopping, bg="#64B5F6", fg="white").pack(pady=10)

        home_image = Image.open("images/homepage.PNG")
        home_image = home_image.resize((300, 200), Image.LANCZOS)
        home_image_tk = ImageTk.PhotoImage(home_image)
        home_image_label = tk.Label(frame, image=home_image_tk, bg="#E3F2FD")
        home_image_label.image = home_image_tk
        home_image_label.pack(pady=10)

        return frame

    def start_shopping(self):
        if self.customer_name.get():
            self.show_frame(self.product_page)
        else:
            messagebox.showerror("Error", "Please enter your name")

    # The rest of the code remains the same...

    def create_product_page(self):
        frame = tk.Frame(self, bg="#E8F5E9")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tk.Label(frame, textvariable=self.customer_name, bg="#E8F5E9", font=("Arial", 14)).pack(pady=10)

        radio_frame = tk.Frame(frame, bg="#E8F5E9")
        radio_frame.pack(pady=10)

        tk.Radiobutton(radio_frame, text="Rackets", variable=self.selected_product_type, value="Rackets", command=self.update_product_grid, bg="#E8F5E9").pack(side=tk.LEFT, padx=20)
        tk.Radiobutton(radio_frame, text="Shoes", variable=self.selected_product_type, value="Shoes", command=self.update_product_grid, bg="#E8F5E9").pack(side=tk.LEFT, padx=20)

        # Center the products display
        center_frame = tk.Frame(frame, bg="#E8F5E9")
        center_frame.pack(expand=True, padx=50, pady=20)

        # Adding a canvas for scroll functionality
        self.canvas = tk.Canvas(center_frame, bg="#E8F5E9")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adding a scrollbar linked to the canvas
        self.scrollbar = tk.Scrollbar(center_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Creating a frame inside the canvas to hold the products
        self.product_frame = tk.Frame(self.canvas, bg="#E8F5E9")

        # Creating a window in the canvas
        self.canvas.create_window((0, 0), window=self.product_frame, anchor="nw")

        # Binding the canvas to the scroll functionality
        self.product_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Buttons at the bottom
        button_frame = tk.Frame(frame, bg="#E8F5E9")
        button_frame.pack(side=tk.BOTTOM, pady=10)

        tk.Button(button_frame, text="View Cart", command=self.show_cart, bg="#81C784", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Show Receipt", command=self.show_receipt, bg="#4CAF50", fg="white").pack(side=tk.RIGHT, padx=10)

        self.update_product_grid()

        return frame

    def update_product_grid(self):
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        product_list = self.shop.rackets if self.selected_product_type.get() == "Rackets" else self.shop.shoes

        # Define grid layout for products
        max_columns = 5  # Adjust this number to change the number of columns
        row = 0
        col = 0

        for idx, product in enumerate(product_list):
            image = Image.open(product.image_path)
            image = image.resize((100, 200), Image.LANCZOS)
            image_tk = ImageTk.PhotoImage(image)

            frame = tk.Frame(self.product_frame, bd=2, relief="groove", bg="#FFFFFF")
            frame.grid(row=row, column=col, padx=5, pady=5)

            image_label = tk.Label(frame, image=image_tk, bg="#FFFFFF")
            image_label.image = image_tk
            image_label.pack()

            tk.Label(frame, text=product.name, bg="#FFFFFF").pack()
            tk.Label(frame, text=f"${product.price}", bg="#FFFFFF").pack()

            tk.Button(frame, text="Add to Cart", command=lambda idx=idx: self.add_to_cart(idx)).pack()

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def add_to_cart(self, product_index):
        quantity = simpledialog.askinteger("Quantity", "Enter the quantity:")
        if quantity is not None and quantity > 0:
            self.shop.add_to_cart(product_index, quantity, self.selected_product_type.get())
        else:
            messagebox.showerror("Error", "Invalid quantity")

    def show_cart(self):
        self.update_cart_display()
        self.show_frame(self.cart_page)

    def update_cart_display(self):
        cart_items = self.shop.get_cart_items()
        self.cart_text.configure(state='normal')
        self.cart_text.delete(1.0, tk.END)
        self.cart_text.insert(tk.END, cart_items)
        self.cart_text.configure(state='disabled')

    def create_cart_page(self):
        frame = tk.Frame(self, bg="#FFEBEE")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.cart_text = tk.Text(frame, state='disabled', width=60, height=20)
        self.cart_text.pack(pady=20)

        remove_button = tk.Button(frame, text="Remove from Cart", command=self.remove_from_cart, bg="#E57373", fg="white")
        remove_button.pack(pady=10)

        back_button = tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.product_page), bg="#EF5350", fg="white")
        back_button.pack(pady=10)

        return frame

    def remove_from_cart(self):
        if self.shop.cart:
            cart_index = simpledialog.askinteger("Remove Item", "Enter the cart item number to remove:")
            if cart_index is not None:
                self.shop.remove_from_cart(cart_index - 1)
                self.update_cart_display()
        else:
            messagebox.showinfo("Cart Empty", "No items to remove from the cart.")

    def create_receipt_page(self):
        frame = tk.Frame(self, bg="#FFFDE7")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.receipt_text = tk.Text(frame, state='disabled', width=60, height=20)
        self.receipt_text.pack(pady=20)

        receipt_button = tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.product_page), bg="#FDD835", fg="black")
        receipt_button.pack(pady=10)

        return frame

    def show_receipt(self):
        self.receipt_text.configure(state='normal')
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, self.shop.get_receipt())
        self.receipt_text.configure(state='disabled')
        self.show_frame(self.receipt_page)
shop = Shop()
app = Application(shop)
app.mainloop()
