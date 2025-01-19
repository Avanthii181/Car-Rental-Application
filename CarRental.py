import tkinter as tk
from tkinter import messagebox

class CarRentalSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Rental System")
        self.geometry("600x500")

        self.available_cars = {
            1: {"model": "Toyota Corolla", "price_per_day": 50, "availability": True},
            2: {"model": "Honda Civic", "price_per_day": 60, "availability": True},
            3: {"model": "Ford Focus", "price_per_day": 55, "availability": True},
            4: {"model": "Chevrolet Malibu", "price_per_day": 70, "availability": False},
        }

        # Frame for car list
        self.frame = tk.Frame(self)
        self.frame.pack(pady=20)

        self.car_listbox = tk.Listbox(self.frame, height=6, width=40)
        self.car_listbox.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.car_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.car_listbox.config(yscrollcommand=self.scrollbar.set)
        self.populate_car_list()

        # Book button
        self.book_button = tk.Button(self, text="Book Car", command=self.book_car)
        self.book_button.pack(pady=10)

        # Frame for booking details
        self.booking_frame = tk.Frame(self)
        self.booking_frame.pack(pady=20)

        self.booking_label = tk.Label(self.booking_frame, text="Booking Information", font=("Arial", 14))
        self.booking_label.pack()

        self.name_label = tk.Label(self.booking_frame, text="Name:")
        self.name_label.pack(padx=10, pady=5)

        self.name_entry = tk.Entry(self.booking_frame)
        self.name_entry.pack(padx=10, pady=5)

        self.days_label = tk.Label(self.booking_frame, text="Number of Days:")
        self.days_label.pack(padx=10, pady=5)

        self.days_entry = tk.Entry(self.booking_frame)
        self.days_entry.pack(padx=10, pady=5)

        self.rent_button = tk.Button(self.booking_frame, text="Confirm Rental", command=self.confirm_rental)
        self.rent_button.pack(pady=10)

    def populate_car_list(self):
        """Populate the listbox with available cars."""
        self.car_listbox.delete(0, tk.END)
        for car_id, car in self.available_cars.items():
            availability = "Available" if car["availability"] else "Not Available"
            self.car_listbox.insert(tk.END, f"{car['model']} - ${car['price_per_day']} per day - {availability}")

    def book_car(self):
        """Handle car selection and booking."""
        try:
            selected_car_index = self.car_listbox.curselection()[0]
            car_id = selected_car_index + 1
            selected_car = self.available_cars[car_id]

            if not selected_car["availability"]:
                messagebox.showwarning("Unavailable", f"{selected_car['model']} is not available.")
                return

            self.selected_car = selected_car
            self.selected_car_id = car_id
            self.selected_car_model = selected_car["model"]
            self.populate_booking_details()
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a car to book.")

    def populate_booking_details(self):
        """Display the booking details after selecting a car."""
        self.booking_label.config(text=f"Booking {self.selected_car_model}")
        self.days_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.rent_button.config(state=tk.NORMAL)

    def confirm_rental(self):
        """Confirm the rental and calculate the total."""
        if not hasattr(self, 'selected_car'):
            messagebox.showwarning("No Car Selected", "Please select a car before confirming the rental.")
            return

        name = self.name_entry.get()
        days = self.days_entry.get()

        if not name or not days.isdigit():
            messagebox.showwarning("Invalid Input", "Please provide valid name and number of days.")
            return

        days = int(days)
        total_price = self.selected_car["price_per_day"] * days

        self.available_cars[self.selected_car_id]["availability"] = False
        self.populate_car_list()

        messagebox.showinfo("Rental Confirmed", f"Thank you {name}! Your rental of {self.selected_car_model} "
                                               f"for {days} days is confirmed. Total: ${total_price}")
        self.reset_booking_form()

    def reset_booking_form(self):
        """Reset the booking form after confirmation."""
        self.booking_label.config(text="Booking Information")
        self.name_entry.delete(0, tk.END)
        self.days_entry.delete(0, tk.END)
        self.rent_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = CarRentalSystem()
    app.mainloop()
