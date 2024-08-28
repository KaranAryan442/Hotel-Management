import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'hotel_management'
}


def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def add_guest(name, phone, email):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO guests (name, phone, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, phone, email))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Guest added successfully!")
    else:
        messagebox.showerror("Error", "Failed to connect to the database")


def book_room(guest_id, room_id, check_in, check_out):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO bookings (guest_id, room_id, check_in, check_out) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (guest_id, room_id, check_in, check_out))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Room booked successfully!")
    else:
        messagebox.showerror("Error", "Failed to connect to the database")


def check_availability(room_id, check_in, check_out):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
        SELECT * FROM bookings 
        WHERE room_id = %s AND 
        ((check_in <= %s AND check_out >= %s) OR 
        (check_in <= %s AND check_out >= %s))
        """
        cursor.execute(query, (room_id, check_out, check_in, check_in, check_out))
        result = cursor.fetchall()
        connection.close()
        if result:
            messagebox.showinfo("Availability", "Room is not available.")
        else:
            messagebox.showinfo("Availability", "Room is available.")
    else:
        messagebox.showerror("Error", "Failed to connect to the database")


class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")


        tk.Label(root, text="Name").grid(row=0, column=0)
        tk.Label(root, text="Phone").grid(row=1, column=0)
        tk.Label(root, text="Email").grid(row=2, column=0)
        self.name_entry = tk.Entry(root)
        self.phone_entry = tk.Entry(root)
        self.email_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.email_entry.grid(row=2, column=1)
        tk.Button(root, text="Add Guest", command=self.add_guest).grid(row=3, column=1)


        tk.Label(root, text="Guest ID").grid(row=4, column=0)
        tk.Label(root, text="Room ID").grid(row=5, column=0)
        tk.Label(root, text="Check-in Date").grid(row=6, column=0)
        tk.Label(root, text="Check-out Date").grid(row=7, column=0)
        self.guest_id_entry = tk.Entry(root)
        self.room_id_entry = tk.Entry(root)
        self.check_in_entry = tk.Entry(root)
        self.check_out_entry = tk.Entry(root)
        self.guest_id_entry.grid(row=4, column=1)
        self.room_id_entry.grid(row=5, column=1)
        self.check_in_entry.grid(row=6, column=1)
        self.check_out_entry.grid(row=7, column=1)
        tk.Button(root, text="Book Room", command=self.book_room).grid(row=8, column=1)

        
        tk.Label(root, text="Room ID").grid(row=9, column=0)
        tk.Label(root, text="Check-in Date").grid(row=10, column=0)
        tk.Label(root, text="Check-out Date").grid(row=11, column=0)
        self.check_room_id_entry = tk.Entry(root)
        self.check_check_in_entry = tk.Entry(root)
        self.check_check_out_entry = tk.Entry(root)
        self.check_room_id_entry.grid(row=9, column=1)
        self.check_check_in_entry.grid(row=10, column=1)
        self.check_check_out_entry.grid(row=11, column=1)
        tk.Button(root, text="Check Availability", command=self.check_availability).grid(row=12, column=1)

    def add_guest(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        add_guest(name, phone, email)

    def book_room(self):
        guest_id = int(self.guest_id_entry.get())
        room_id = int(self.room_id_entry.get())
        check_in = self.check_in_entry.get()
        check_out = self.check_out_entry.get()
        book_room(guest_id, room_id, check_in, check_out)

    def check_availability(self):
        room_id = int(self.check_room_id_entry.get())
        check_in = self.check_check_in_entry.get()
        check_out = self.check_check_out_entry.get()
        check_availability(room_id, check_in, check_out)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()
