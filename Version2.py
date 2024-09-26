    import tkinter as tk
from tkinter import messagebox

#This class represents a badminton Racket with a name and price
class Racket:
    def __init__(self, name, price):
        self.name = name
        self.price = price

#This class represents the Shop which sells badminton rackets
class Shop:
    def __init__(self):
        self.rackets = [
            Racket("Yonex Astrox 99", 250),
            Racket("Li-Ning N9ii", 200),
            Racket("Victor Thruster K 9900", 220),
            Racket("Yonex Duora Z-Strike", 230),
            Racket("Li-Ning Aeronaut 8000", 210),
            Racket("Victor Jetspeed S 12", 190),
            Racket("Yonex Nanoflare 700", 240),
            Racket("Li-Ning Turbo Charging 75", 215),
            Racket("Victor Auraspeed 90S", 225),
            Racket("Yonex Voltric Z-Force II", 260)
        ]
        self.cart = []

    #Method to add a selected racket to the shopping cart
    #Takes racket_index (index of the selected racket) and quantity as arguments
    def add_to_cart(self, racket_index, quantity):
        racket = self.rackets[racket_index]
        self.cart.append((racket, quantity))
        #Display a pop-up message to confirm the item has been added to the cart
        messagebox.showinfo("Added to Cart", f"Added {quantity} x {racket.name} to your cart.")

    #Method to generate the receipt after shopping
    def get_receipt(self):
        receipt = "Receipt:\n"
        total = 0
        for racket, quantity in self.cart:
            #Calculate the cost for the current item (price * quantity)
            cost = racket.price * quantity
            total += cost
            #Append the racket details and cost to the receipt string
            receipt += f"{racket.name} - ${racket.price} x {quantity} = ${cost}\n"
        receipt += f"Total: ${total}"
        return receipt

#This class defines the main application window for the badminton shop using tkinter
class Application(tk.Tk):
    def __init__(self, shop):
        super().__init__()
        self.shop = shop
        self.title("Badminton Shop")
        
        self.customer_name = tk.StringVar()

        #Create different frames for the application: start page, racket page, and receipt page
        self.start_page = self.create_start_page()
        self.racket_page = self.create_racket_page()
        self.receipt_page = self.create_receipt_page()

        self.show_frame(self.start_page)

    # Function to raise a specific frame (page) and display it in the window
    def show_frame(self, frame):
        frame.tkraise()

    #Function to create the start page where the customer enters their name
    def create_start_page(self):
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Enter your name:").pack(pady=10)
        name_entry = tk.Entry(frame, textvariable=self.customer_name)
        name_entry.pack(pady=10)

        #Add a button to start shopping (switch to the racket page)
        tk.Button(frame, text="Start Shopping", command=self.start_shopping).pack(pady=10)
        return frame

    def start_shopping(self):
        if self.customer_name.get():
            #If the customer has entered their name, proceed to the racket selection page
            self.show_frame(self.racket_page)
        else:
            #If no name is entered, display an error message
            messagebox.showerror("Error", "Please enter your name")

    #Function to create the racket selection page
    def create_racket_page(self):
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, textvariable=self.customer_name).pack(pady=10)

        # Create a Listbox to display available rackets for selection
        self.racket_listbox = tk.Listbox(frame, height=10)
        for racket in self.shop.rackets:
            self.racket_listbox.insert(tk.END, f"{racket.name} - ${racket.price}")
        self.racket_listbox.pack(pady=10)

        #Add a label and an entry field for the customer to specify the quantity of the racket
        tk.Label(frame, text="Quantity:").pack()
        self.quantity_entry = tk.Entry(frame)
        self.quantity_entry.pack(pady=10)

        #Add a button to add the selected racket to the cart
        tk.Button(frame, text="Add to Cart", command=self.add_to_cart).pack(pady=10)
        tk.Button(frame, text="Show Receipt", command=self.show_receipt).pack(pady=10)
        return frame

    #Function to add the selected racket and quantity to the cart
    def add_to_cart(self):
        try:
            racket_index = self.racket_listbox.curselection()[0]
            quantity = int(self.quantity_entry.get())
            self.shop.add_to_cart(racket_index, quantity)
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Invalid selection or quantity")

    #Function to create the receipt display page
    def create_receipt_page(self):
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(frame, text="Receipt").pack(pady=10)
        self.receipt_text = tk.Text(frame, height=10, width=50)
        self.receipt_text.pack(pady=10)

        tk.Button(frame, text="Back to Shopping", command=lambda: self.show_frame(self.racket_page)).pack(pady=10)
        return frame

    #Function to display the receipt in the Text widget
    def show_receipt(self):
        self.receipt_text.delete(1.0, tk.END)
        #Generate the receipt from the shop's cart and display it in the Text widget
        receipt = self.shop.get_receipt()
        self.receipt_text.insert(tk.END, receipt)
        self.show_frame(self.receipt_page)

#Main function to start the application
def main():
    shop = Shop()
    app = Application(shop)
    app.mainloop()

if __name__ == "__main__":
    main()

