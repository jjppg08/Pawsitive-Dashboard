import tkinter as tk
import sys, os
from tkinter import ttk, messagebox
from tkinter import filedialog
import sqlite3
import datetime

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller exe """
    try:
        # PyInstaller temporary folder
        base_path = sys._MEIPASS
    except AttributeError:
        # Normal running
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Example usage
db_path = resource_path("vet_clinic_v3.db")
img_folder = resource_path("Pet Images")


def ensure_pets_table_schema():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("PRAGMA table_info(pets)")
    cols = [row[1] for row in c.fetchall()]

    if "image_path" not in cols:
        c.execute("ALTER TABLE pets ADD COLUMN image_path TEXT")

    conn.commit()
    conn.close()

# --- Image Import Handling ---
try:
    from PIL import Image, ImageTk
    IMAGE_SUPPORT = True
except ImportError:
    Image = None
    ImageTk = None
    IMAGE_SUPPORT = False

# ================= DATABASE SETUP =================
DB_NAME = "vet_clinic_v3.db"
db_path = resource_path("vet_clinic_v3.db")
img_folder = resource_path("Pet Images")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 1. Appointments
    c.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            pet TEXT,
            owner TEXT,
            contact_number TEXT,
            service TEXT
        )
    """)

    # 2. Pet Records
    c.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            microchip_id TEXT,
            pet_name TEXT,
            species TEXT,
            breed TEXT,
            owner TEXT,
            age TEXT,
            gender TEXT,
            dob TEXT,
            color TEXT,
            image_path TEXT
        )
    """)

    # 3. Inventory
    c.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            category TEXT,
            quantity INTEGER,
            unit_measure TEXT,
            status TEXT
        )
    """)

    # 4. Invoices
    c.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            client_name TEXT,
            description TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()
    
def ensure_pets_table_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(pets)")
    columns = [col[1] for col in cursor.fetchall()]

    if "image_path" not in columns:
        cursor.execute("ALTER TABLE pets ADD COLUMN image_path TEXT")

    conn.commit()
    conn.close()


# ================= LOGIN WINDOW =================
class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("PAWSITIVE TREAT — Login")
        master.geometry("400x450")
        master.resizable(False, False)
        
        self.login_bg_color = "#ffe6f0"
        self.button_color = "#ff4da6"
        self.text_color = "#4a4a4a"
        self.valid_username = "z.lsjrdn"
        self.valid_password = "12345"

        master.configure(bg=self.login_bg_color)
        master.option_add("*Font", ("Roboto", 10, "bold"))
        self.center_window()
        self.setup_ui()

    def center_window(self):
        master = self.master
        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f'+{int(x)}+{int(y)}')

    def setup_ui(self):
        main_frame = tk.Frame(self.master, bg=self.login_bg_color, padx=30, pady=30)
        main_frame.pack(expand=True, fill=tk.BOTH)

        if IMAGE_SUPPORT:
            try:
                img = Image.open("logo.png").resize((100, 100))
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(main_frame, image=self.logo_img, bg=self.login_bg_color).pack(pady=(0, 10))
            except Exception:
                tk.Label(main_frame, text="🐾", font=("Arial", 40), bg=self.login_bg_color).pack(pady=(0, 10))
        else:
            tk.Label(main_frame, text="🐾", font=("Arial", 40), bg=self.login_bg_color).pack(pady=(0, 10))
        
        tk.Label(main_frame, text="PAWSITIVE TREAT", font=("Roboto", 20, "bold"), bg=self.login_bg_color, fg=self.text_color).pack()
        tk.Label(main_frame, text="PET CLINIC LOGIN", font=("Roboto", 12, "bold"), bg=self.login_bg_color, fg=self.button_color).pack(pady=(0, 20))

        tk.Label(main_frame, text="Username:", bg=self.login_bg_color, fg=self.text_color, anchor="w").pack(fill=tk.X, pady=(10, 0))
        self.username_entry = tk.Entry(main_frame, font=("Roboto", 12))
        self.username_entry.pack(fill=tk.X, ipady=5)

        tk.Label(main_frame, text="Password:", bg=self.login_bg_color, fg=self.text_color, anchor="w").pack(fill=tk.X, pady=(10, 0))
        self.password_entry = tk.Entry(main_frame, show="*", font=("Roboto", 12))
        self.password_entry.pack(fill=tk.X, ipady=5)
        
        self.master.bind('<Return>', lambda event=None: self.login())
        tk.Button(main_frame, text="Login", command=self.login, bg=self.button_color, fg="white", relief=tk.FLAT, font=("Roboto", 12, "bold")).pack(fill=tk.X, pady=20, ipady=10)

    def login(self):
        if self.username_entry.get() == self.valid_username and self.password_entry.get() == self.valid_password:
            self.master.destroy()
            main_root = tk.Tk()
            VetApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

# ================= MAIN APP =================
class VetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PAWSITIVE TREAT — Pet Clinic Dashboard")
        self.root.geometry("1200x700")
        self.root.minsize(1100, 650)
        self.root.configure(bg='white')

        self.colors = {
            "dashboard_bg": "#ffd7ef",
            "upcoming": "#ffbae4",
            "lowstock": "#ff97d6",
            "vaccine": "#fd73c8",
            "nav_btn_bg": "#f9f9f9",
            "nav_btn_fg": "#4a4a4a",
            "active_tab_bg": "#ff4da6",
            "default_row_bg": "white", 
            "header_bg": "#ffcce0",
            "zebra_odd": "#ffe6f0",
            "zebra_even": "#ffffff"
        }

        self.root.option_add("*Font", ("Roboto", 10, "bold"))
        self.nav_buttons = {}
        self.current_view = ""
        
        # ID Trackers
        self.selected_apt_id = None
        self.selected_pet_id = None
        self.selected_inv_id = None

        # Search Vars
        self.apt_search_var = tk.StringVar()
        self.pet_search_var = tk.StringVar()
        self.inv_search_var = tk.StringVar()
        self.invc_search_var = tk.StringVar()

        self.setup_header()
        self.body_frame = tk.Frame(self.root, bg='white')
        self.body_frame.pack(fill=tk.BOTH, expand=True)
        self.switch_view("Appointment")

        self.original_pet_img = None
        self.pet_img_preview = None

    # ================= HEADER =================
    def setup_header(self):
        header = tk.Frame(self.root, bg="white")
        header.pack(fill=tk.X)
        if IMAGE_SUPPORT:
            try:
                img = Image.open("logo.png").resize((80, 80))
                self.logo_img = ImageTk.PhotoImage(img)
                tk.Label(header, image=self.logo_img, bg="white").pack(side=tk.LEFT, padx=10, pady=5)
            except Exception: pass
        
        title_frame = tk.Frame(header, bg="white")
        title_frame.pack(side=tk.LEFT, pady=5)
        tk.Label(title_frame, text="PAWSITIVE TREAT", font=("Roboto", 20, "bold"), bg="white").pack()
        tk.Label(title_frame, text="PET CLINIC", font=("Roboto", 15, "bold"), fg="#ff4da6", bg="white").pack()

        nav_frame = tk.Frame(header, bg="white")
        nav_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        nav_items = ["Invoice", "Stock Inventory", "Pet Records", "Appointment"]
        for b_text in nav_items:
            btn = tk.Button(nav_frame, text=b_text, bg=self.colors["nav_btn_bg"], fg=self.colors["nav_btn_fg"], 
                            relief=tk.FLAT, bd=2, font=("Roboto", 12, "bold"),
                            command=lambda x=b_text: self.switch_view(x))
            btn.pack(side=tk.LEFT, padx=5, pady=0, ipady=3, fill=tk.X, expand=True)
            self.nav_buttons[b_text] = btn

    def switch_view(self, view_name):
        self.current_view = view_name
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.config(bg=self.colors["active_tab_bg"], fg="white", relief=tk.RAISED)
            else:
                btn.config(bg=self.colors["nav_btn_bg"], fg=self.colors["nav_btn_fg"], relief=tk.FLAT)

        for widget in self.body_frame.winfo_children(): widget.destroy()

        if view_name == "Appointment": self.show_appointment_ui()
        elif view_name == "Pet Records": self.show_pet_records_ui()
        elif view_name == "Stock Inventory": self.show_inventory_ui()
        elif view_name == "Invoice": self.show_invoice_ui()

    # ================= APPOINTMENT =================
    def show_appointment_ui(self):
        main = tk.Frame(self.body_frame, bg='white')
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        left_panel = tk.Frame(main, bg='white')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))

        # Dashboard
        dash_frame = tk.Frame(left_panel, bg=self.colors["dashboard_bg"], pady=10)
        dash_frame.pack(fill=tk.X, pady=(0,10))
        tk.Label(dash_frame, text="Dashboard", font=("Roboto", 22, "bold"), bg=self.colors["dashboard_bg"]).pack(anchor="w", padx=15)
        self.lbl_upcoming = tk.Label(dash_frame, text="Upcoming Appointment: None", bg=self.colors["upcoming"], height=2, padx=10, anchor="w")
        self.lbl_upcoming.pack(fill=tk.X, padx=20, pady=4)
        self.lbl_lowstock = tk.Label(dash_frame, text="Low Stock Items: 0", bg=self.colors["lowstock"], height=2, padx=10, anchor="w")
        self.lbl_lowstock.pack(fill=tk.X, padx=20, pady=4)
        self.lbl_vaccine = tk.Label(dash_frame, text="Vaccines Due: 0", bg=self.colors["vaccine"], height=2, padx=10, anchor="w")
        self.lbl_vaccine.pack(fill=tk.X, padx=20, pady=4)

        # Appointment Treeview
        tk.Label(left_panel, text="Appointments List", font=("Roboto", 12, "bold"), bg='white').pack(anchor="w")
        search_frame = tk.Frame(left_panel, bg='white', pady=5)
        search_frame.pack(fill=tk.X)
        tk.Label(search_frame, text="Search Term:", bg='white').pack(side=tk.LEFT)
        self.search_term_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_term_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.apply_search_filter)
        tk.Label(search_frame, text="Filter By:", bg='white').pack(side=tk.LEFT, padx=(10,5))
        self.filter_column_var = tk.StringVar(value="All Columns")
        filter_columns = ["All Columns", "Date", "Time", "Pet", "Owner", "Contact", "Service"]
        self.filter_combobox = ttk.Combobox(search_frame, textvariable=self.filter_column_var, values=filter_columns, state="readonly", width=15)
        self.filter_combobox.pack(side=tk.LEFT)
        self.filter_combobox.bind("<<ComboboxSelected>>", self.apply_search_filter)

        cols = ("ID", "Date", "Time", "Pet", "Owner", "Contact", "Service")
        tree_container = tk.Frame(left_panel)
        tree_container.pack(fill=tk.BOTH, expand=True)
        self.tree = ttk.Treeview(tree_container, columns=cols, show="headings", height=15)
        yscroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        for col in cols:
            self.tree.heading(col, text=col)
            width = 60 if col=="ID" else 115
            self.tree.column(col, width=width, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.select_appointment)

        # Form Panel
        form_frame = tk.Frame(main, bg=self.colors["dashboard_bg"], padx=20, pady=10)
        form_frame.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(form_frame, text="Manage Appointment", font=("Roboto", 12, "bold"), bg=self.colors["dashboard_bg"]).pack()
        self.entries = {}
        fields = ["Date", "Time", "Pet", "Owner", "Contact Number", "Service"]
        for f in fields:
            tk.Label(form_frame, text=f, bg=self.colors["dashboard_bg"], font=("Roboto", 10, "bold")).pack(anchor="w", pady=(8,0))
            ent = tk.Entry(form_frame, font=("Roboto", 10))
            ent.pack(fill=tk.X)
            self.entries[f] = ent

        btn_frame = tk.Frame(form_frame, bg=self.colors["dashboard_bg"])
        btn_frame.pack(fill=tk.X, pady=15)
        tk.Button(btn_frame, text="Add", bg=self.colors["upcoming"], command=self.save_appointment).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Update", bg=self.colors["lowstock"], command=self.update_appointment).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Delete", bg=self.colors["vaccine"], command=self.delete_appointment).pack(fill=tk.X, pady=2)
        tk.Button(btn_frame, text="Clear Form", command=self.clear_fields).pack(fill=tk.X, pady=2)

        ttk.Separator(form_frame, orient='horizontal').pack(fill='x', pady=10)
        self.today_count_label = tk.Label(form_frame, text="0 Appointment/s Today", bg=self.colors["dashboard_bg"], fg="#ff4da6", font=("Roboto", 14, "bold"))
        self.today_count_label.pack(anchor="w", padx=10)

        self.load_data()

    def format_and_validate_date(self, date_str):
        formats_to_try = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
        for fmt in formats_to_try:
            try:
                date_obj = datetime.datetime.strptime(date_str, fmt)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue
        messagebox.showwarning("Date Error", "Invalid date format. Use YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY.")
        return None

    def validate_fields(self, values):
        if not all(values):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return False
        contact = self.entries["Contact Number"].get()
        if not contact.isdigit():
            messagebox.showwarning("Validation Error", "Contact Number must contain only digits.")
            return False
        return True

    def save_appointment(self):
        values = [self.entries[f].get() for f in self.entries]
        if not self.validate_fields(values): return
        formatted_date = self.format_and_validate_date(values[0])
        if not formatted_date: return
        values[0] = formatted_date
        time_input = values[1].strip()
        try:
            time_obj = datetime.datetime.strptime(time_input, "%I:%M %p")
        except ValueError:
            try:
                time_obj = datetime.datetime.strptime(time_input, "%H:%M")
            except ValueError:
                messagebox.showwarning("Time Error", "Invalid time format.")
                return
        values[1] = time_obj.strftime("%H:%M")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO appointments (date, time, pet, owner, contact_number, service) VALUES (?,?,?,?,?,?)", values)
        conn.commit()
        conn.close()
        self.clear_fields()
        self.load_data()

    def select_appointment(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, "values")
        if not values:
            return

        self.selected_apt_id = values[0]

        field_order = ["Date", "Time", "Pet", "Owner", "Contact Number", "Service"]
        for i, field in enumerate(field_order):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, values[i+1])

    def update_appointment(self):
        if not self.selected_apt_id: return
        values = [self.entries[f].get() for f in self.entries]
        if not self.validate_fields(values): return
        formatted_date = self.format_and_validate_date(values[0])
        if not formatted_date: return
        values[0] = formatted_date
        time_input = values[1].strip()
        try:
            time_obj = datetime.datetime.strptime(time_input, "%I:%M %p")
        except ValueError:
            try:
                time_obj = datetime.datetime.strptime(time_input, "%H:%M")
            except ValueError:
                messagebox.showwarning("Time Error", "Invalid time format.")
                return
        values[1] = time_obj.strftime("%H:%M")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE appointments SET date=?, time=?, pet=?, owner=?, contact_number=?, service=? WHERE id=?", values + [self.selected_apt_id])
        conn.commit()
        conn.close()
        self.clear_fields()
        self.load_data()

    def delete_appointment(self):
        if not self.selected_apt_id: return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?"):
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("DELETE FROM appointments WHERE id=?", (self.selected_apt_id,))
            conn.commit()
            conn.close()
            self.clear_fields()
            self.load_data()

    def clear_fields(self):
        self.selected_apt_id = None
        for e in self.entries.values(): e.delete(0, tk.END)
        self.search_term_var.set("")
        self.filter_column_var.set("All Columns")
        self.load_data()

    def apply_search_filter(self, event=None):
        search_term = self.search_term_var.get().lower()
        filter_col = self.filter_column_var.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM appointments")
        rows = c.fetchall()
        conn.close()
        for r in rows:
            values = [str(v).lower() for v in r]
            if filter_col == "All Columns":
                if any(search_term in v for v in values[1:]):
                    self.tree.insert("", tk.END, values=r)
            else:
                col_index = ["Date", "Time", "Pet", "Owner", "Contact", "Service"].index(filter_col) + 1
                if search_term in values[col_index]:
                    self.tree.insert("", tk.END, values=r)
        self.apply_zebra_striping()
        self.update_dashboard()

    def apply_zebra_striping(self):
        for i, item in enumerate(self.tree.get_children()):
            if i % 2 == 0:
                self.tree.item(item, tags=("even",))
            else:
                self.tree.item(item, tags=("odd",))
        self.tree.tag_configure("even", background=self.colors["zebra_even"])
        self.tree.tag_configure("odd", background=self.colors["zebra_odd"])

    def load_data(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM appointments ORDER BY date ASC, time ASC")
        rows = c.fetchall()
        conn.close()
        for r in rows:
            self.tree.insert("", tk.END, values=r)
        self.apply_zebra_striping()
        self.update_dashboard()

    def update_dashboard(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        c.execute("SELECT COUNT(*) FROM appointments WHERE date=?", (today,))
        count_today = c.fetchone()[0]
        self.today_count_label.config(text=f"{count_today} Appointment/s Today")

        conn.close()

        children = self.tree.get_children()

        if children:
            first_item = children[0]
            values = self.tree.item(first_item, "values")

            # values = (ID, Date, Time, Pet, Owner, Contact, Service)
            appt_date = values[1]
            appt_time = values[2]
            pet = values[3]
            owner = values[4]
            service = values[6]

            self.lbl_upcoming.config(
                text=f"Upcoming Appointment: {appt_time} - {pet} ({service})"
            )
        else:
            self.lbl_upcoming.config(text="Upcoming Appointment: None")

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM inventory WHERE quantity < 5")
        low_stock_count = c.fetchone()[0]
        self.lbl_lowstock.config(text=f"Low Stock Items: {low_stock_count}")

        self.lbl_vaccine.config(text="Vaccines Due: 0")

        conn.close()


    # ================= PET RECORDS =================
    def show_pet_records_ui(self):
        main = tk.Frame(self.body_frame, bg='white')
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = tk.Frame(main, bg='white')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        tk.Label(left, text="Pet Records Database", font=("Roboto", 16, "bold"), bg='white').pack(anchor="w", pady=10)
        
        search_fr = tk.Frame(left, bg='white')
        search_fr.pack(fill=tk.X, pady=(0,5))
        tk.Label(search_fr, text="Search:", bg='white').pack(side=tk.LEFT)
        s_ent = tk.Entry(search_fr, textvariable=self.pet_search_var)
        s_ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        s_ent.bind("<KeyRelease>", self.load_pets)

        filter_fr = tk.Frame(search_fr, bg="white")
        filter_fr.pack(side=tk.LEFT, padx=10)

        self.pet_species_filter = tk.StringVar(value="All")
        self.pet_gender_filter = tk.StringVar(value="All")

        species_fr = tk.Frame(filter_fr, bg="white")
        species_fr.pack(side=tk.LEFT, padx=5)

        tk.Label(species_fr, text="Species", bg="white", font=("Roboto", 9)).pack(anchor="w")
        ttk.Combobox(
            species_fr,
            textvariable=self.pet_species_filter,
            values=["All", "Dog", "Cat"],
            state="readonly",
            width=10
        ).pack()

        gender_fr = tk.Frame(filter_fr, bg="white")
        gender_fr.pack(side=tk.LEFT, padx=5)

        tk.Label(gender_fr, text="Gender", bg="white", font=("Roboto", 9)).pack(anchor="w")
        ttk.Combobox(
            gender_fr,
            textvariable=self.pet_gender_filter,
            values=["All", "Male", "Female"],
            state="readonly",
            width=10
        ).pack()

        self.pet_species_filter.trace_add(
            "write",
            lambda *args: self.load_pets()
        )
        self.pet_gender_filter.trace_add(
            "write",
            lambda *args: self.load_pets()
        )

        tree_container = tk.Frame(left, bg="white")
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        cols = ("ID", "Microchip", "Name", "Species", "Breed", "Owner", "Age", "Gender", "DOB", "Color", "Image")
        self.pet_tree = ttk.Treeview(
            tree_container,
            columns=cols,
            show="headings",
            height=15,
            selectmode="browse"
        )
        
        for c in cols:
            self.pet_tree.heading(c, text=c)
            width = 40 if c == "ID" else 85
            if c == "ID":
                self.pet_tree.column(c, width=width, anchor="center")
            else:
                self.pet_tree.column(c, width=width, anchor="center")

        self.pet_tree.column("Image", width=0, stretch=False)

        v_scroll = ttk.Scrollbar(
            tree_container,
            orient="vertical",
            command=self.pet_tree.yview
        )
        self.pet_tree.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.pet_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pet_tree.bind("<ButtonRelease-1>", self.select_pet)
        self.pet_tree.bind("<Double-1>", self.on_pet_double_click)

        right = tk.Frame(main, bg=self.colors["dashboard_bg"])
        right.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(
            right,
            bg=self.colors["dashboard_bg"],
            highlightthickness=0,
            width=260
        )
        canvas.pack(side=tk.LEFT, fill=tk.Y)

        form_frame = tk.Frame(canvas, bg=self.colors["dashboard_bg"])
        canvas.create_window((15, 0), window=form_frame, anchor="nw")

        form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        CONTENT_WIDTH = 200

        content = tk.Frame(form_frame, bg=self.colors["dashboard_bg"], width=200, bd=1, relief="solid")
        content.pack(padx=15, pady=5)
        content.pack_propagate(False)

        tk.Label(content, text="Manage Pet Record",
                 font=("Roboto", 12, "bold"),
                 bg=self.colors["dashboard_bg"]).pack(pady=(0,10))

        self.pet_image_path = None

        self.pet_image_label = tk.Label(
            content,
            text="No Image",
            width=20,
            height=10,
            bg="white",
            relief=tk.SOLID
        )
        self.pet_image_label.pack(pady=5)

        tk.Button(
            form_frame,
            text="Upload Pet Image",
            command=self.upload_pet_image
        ).pack(fill=tk.X, pady=(0,10))

        self.pet_entries = {}

        field_list = ["Microchip ID", "Pet Name", "Species", "Breed", "Owner", "Age", "Gender", "Date of Birth", "Color"]
        for f in field_list:
            tk.Label(form_frame, text=f, bg=self.colors["dashboard_bg"], font=("Roboto", 9, "bold")).pack(anchor="w")
            if f == "Gender":
                cb = ttk.Combobox(form_frame, values=["Male", "Female", "Unknown"], state="readonly")
                cb.pack(fill=tk.X, pady=(0,2))
                cb.current(2) 
                self.pet_entries[f] = cb
            else:
                e = tk.Entry(form_frame, font=("Roboto", 10))
                e.pack(fill=tk.X, pady=(0,2))
                self.pet_entries[f] = e

        btn_fr = tk.Frame(form_frame, bg=self.colors["dashboard_bg"])
        btn_fr.pack(fill=tk.X, pady=10)
        tk.Button(btn_fr, text="Add", bg=self.colors["upcoming"], command=self.save_pet).pack(fill=tk.X, pady=2)
        tk.Button(btn_fr, text="Update", bg=self.colors["lowstock"], command=self.update_pet).pack(fill=tk.X, pady=2)
        tk.Button(btn_fr, text="Delete", bg=self.colors["vaccine"], command=self.delete_pet).pack(fill=tk.X, pady=2)
        tk.Button(btn_fr, text="Clear", command=self.clear_pet_form).pack(fill=tk.X, pady=2)

        ensure_pets_table_schema()
        
        self.load_pets()

    def select_pet(self, event):
        row_id = self.pet_tree.identify_row(event.y)
        if not row_id:
            return

        self.pet_tree.selection_set(row_id)
        vals = self.pet_tree.item(row_id, "values")
        if not vals:
            return

        self.selected_pet_id = vals[0]

        self.pet_image_path = vals[10]

        if (
            self.pet_image_path
            and IMAGE_SUPPORT
            and os.path.exists(self.pet_image_path)
        ):
            img = Image.open(self.pet_image_path)
            img = img.resize((150, 150), Image.LANCZOS)
            self.pet_img_preview = ImageTk.PhotoImage(img)
            self.pet_image_label.config(image=self.pet_img_preview, text="")
        else:
            self.pet_image_label.config(image="", text="No Image")

        mapping = [
            "Microchip ID",
            "Pet Name",
            "Species",
            "Breed",
            "Owner",
            "Age",
            "Gender",
            "Date of Birth",
            "Color"
        ]

        for i, key in enumerate(mapping):
            widget = self.pet_entries[key]
            value = vals[i + 1]  # skip ID

            if isinstance(widget, ttk.Combobox):
                
                widget.set(value)
            else:
                widget.delete(0, tk.END)
                widget.insert(0, value)

    def on_pet_double_click(self, event):
        selection = self.pet_tree.selection()
        if not selection:
            return

        sel = selection[0]
        vals = self.pet_tree.item(sel, "values")
        if not vals:
            return

        pet_data = {
            "id": vals[0],
            "microchip": vals[1],
            "name": vals[2],
            "species": vals[3],
            "breed": vals[4],
            "owner": vals[5],
            "age": vals[6],
            "gender": vals[7],
            "dob": vals[8],
            "color": vals[9],
            "image_path": vals[10]
        }

        self.open_pet_card(pet_data)

    def show_pet_card(self, event):
        sel = self.pet_tree.focus()
        vals = self.pet_tree.item(sel, "values")
        if not vals:
            return

        pet_data = {
            "name": vals[2],
            "species": vals[3],
            "breed": vals[4],
            "owner": vals[5],
            "age": vals[6],
            "gender": vals[7],
            "dob": vals[8],
            "color": vals[9],
            "image_path": vals[10]
        }

        self.open_pet_card(pet_data)

    def open_pet_card(self, pet_data):
        card = tk.Toplevel(self.root)
        card.title("Pet ID Card")
        card.geometry("520x320")
        card.resizable(False, False)
        card.configure(bg="#f7d6e0") 

        main = tk.Frame(card, bg="#ffffff", bd=2, relief="ridge")
        main.pack(padx=15, pady=15, fill="both", expand=True)

        left = tk.Frame(main, bg="#ffffff")
        left.pack(side="left", padx=15, pady=15)

        right = tk.Frame(main, bg="#ffffff")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        if pet_data["image_path"] and os.path.exists(pet_data["image_path"]):
            img = Image.open(pet_data["image_path"])
            img = img.resize((170, 190))
            pet_img = ImageTk.PhotoImage(img)
            img_lbl = tk.Label(left, image=pet_img, bg="white", relief="solid", bd=1)
            img_lbl.image = pet_img
            img_lbl.pack()
        else:
            tk.Label(
                left,
                text="NO IMAGE",
                width=18,
                height=10,
                bg="#eeeeee",
                relief="solid"
            ).pack()

        title = tk.Label(
            right,
            text=pet_data["name"].upper(),
            font=("Roboto", 16, "bold"),
            bg="white"
        )
        title.pack(pady=(0, 8))

        fields = [
            ("Species", pet_data["species"]),
            ("Breed", pet_data["breed"]),
            ("Age", pet_data["age"]),
            ("Gender", pet_data["gender"]),
            ("DOB", pet_data["dob"]),
            ("Color", pet_data["color"]),
            ("Owner", pet_data["owner"]),
        ]

        for label, value in fields:
            row = tk.Frame(right, bg="white")
            row.pack(anchor="w", pady=2, fill="x")

            tk.Label(
                row,
                text=f"{label}:",
                font=("Roboto", 12, "bold"),
                bg="white",
                width=10,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                font=("Roboto", 12),
                bg="white",
                anchor="w"
            ).pack(side="left")

        tk.Label(
            card,
            text="PAWSITIVE TREAT CLINIC",
            font=("Roboto", 11, "bold"),
            bg="#f7d6e0"
        ).pack(pady=(0, 5))

    def upload_pet_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Pet Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if not file_path:
            return

        self.pet_image_path = file_path

        if IMAGE_SUPPORT:
            img = Image.open(file_path)
            img = img.resize((50, 50))
            self.pet_img_preview = ImageTk.PhotoImage(img)
            self.pet_image_label.config(image=self.pet_img_preview, text="")
                
    def format_and_validate_date(self, date_str):
        formats_to_try = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
        for fmt in formats_to_try:
            try:
                date_obj = datetime.datetime.strptime(date_str, fmt)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue
        messagebox.showwarning("Date Error", "Invalid date format. Use YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY.")
        return None

    def validate_fields(self, values):
        if not all(values):
            messagebox.showwarning("Validation Error", "All fields are required!")
            return False
        return True

    def save_pet(self):
        vals = [self.pet_entries[f].get().strip() for f in self.pet_entries]
        if not self.validate_fields(vals):
            return
        formatted_dob = self.format_and_validate_date(vals[7])
        if not formatted_dob:
            return
        vals[7] = formatted_dob
        vals.append(self.pet_image_path)
        conn = sqlite3.connect(DB_NAME)
        conn.execute("""
            INSERT INTO pets (
                microchip_id,
                pet_name,
                species,
                breed,
                owner,
                age,
                gender,
                dob,
                color,
                image_path
            )
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, vals)
        conn.commit()
        conn.close()

        self.clear_pet_form()

    def update_pet(self):
        if not self.selected_pet_id:
            return
        vals = [self.pet_entries[f].get().strip() for f in self.pet_entries]
        if not self.validate_fields(vals):
            return
        formatted_dob = self.format_and_validate_date(vals[7])
        if not formatted_dob:
            return
        vals[7] = formatted_dob
        vals.append(self.pet_image_path)
        conn = sqlite3.connect(DB_NAME)
        conn.execute("""
            UPDATE pets SET
                microchip_id=?,
                pet_name=?,
                species=?,
                breed=?,
                owner=?,
                age=?,
                gender=?,
                dob=?,
                color=?,
                image_path=?
            WHERE id=?
        """, vals + [self.selected_pet_id])
        conn.commit()
        conn.close()

        self.clear_pet_form()

    def delete_pet(self):
        if not self.selected_pet_id: return
        conn = sqlite3.connect(DB_NAME)
        conn.execute("DELETE FROM pets WHERE id=?", (self.selected_pet_id,))
        conn.commit()
        conn.close()
        self.clear_pet_form()

    def clear_pet_form(self):
        self.selected_pet_id = None
        for e in self.pet_entries.values(): e.delete(0, tk.END)
        self.load_pets()
        self.pet_image_path = None
        self.pet_image_label.config(image="", text="No Image")

    def load_pets(self, event=None):
        for i in self.pet_tree.get_children():
            self.pet_tree.delete(i)

        search = self.pet_search_var.get().strip()
        species = self.pet_species_filter.get()
        gender = self.pet_gender_filter.get()

        query = "SELECT * FROM pets WHERE 1=1"
        params = []

        if search:
            query += """
                AND (
                    pet_name LIKE ?
                    OR owner LIKE ?
                    OR microchip_id LIKE ?
                    OR species LIKE ?
                    OR breed LIKE ?
                    OR color LIKE ?
                )
            """
            s = f"%{search}%"
            params.extend([s, s, s, s, s, s])

        if species != "All":
            query += " AND LOWER(species) = LOWER (?)"
            params.append(species)

        if gender != "All":
            query += " AND LOWER(gender) = LOWER(?)"
            params.append(gender)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(query, params)

        for row in c.fetchall():
            self.pet_tree.insert("", tk.END, values=row)

        conn.close()
        self.apply_pet_zebra_strip()

    def apply_pet_zebra_strip(self):
        for i, item in enumerate(self.pet_tree.get_children()):
            if i % 2 == 0:
                self.pet_tree.item(item, tags=("even",))
            else:
                self.pet_tree.item(item, tags=("odd",))
        self.pet_tree.tag_configure("even", background=self.colors["zebra_even"])
        self.pet_tree.tag_configure("odd", background=self.colors["zebra_odd"])

    # ================= INVENTORY =================
    def show_inventory_ui(self):
        main = tk.Frame(self.body_frame, bg='white')
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = tk.Frame(main, bg='white')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        tk.Label(left, text="Stock Inventory", font=("Roboto", 16, "bold"), bg='white').pack(anchor="w", pady=10)
        
        search_fr = tk.Frame(left, bg='white')
        search_fr.pack(fill=tk.X, pady=(0,5))
        tk.Label(search_fr, text="Search Item:", bg='white').pack(side=tk.LEFT)
        s_ent = tk.Entry(search_fr, textvariable=self.inv_search_var)
        s_ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        s_ent.bind("<KeyRelease>", self.load_inventory) 

        cols = ("ID", "Item Name", "Category", "Quantity", "UOM", "Status")
        self.inv_tree = ttk.Treeview(left, columns=cols, show="headings", height=15)
        for c in cols:
            self.inv_tree.heading(c, text=c)
            width = 40 if c == "ID" else 100
            self.inv_tree.column(c, width=width, anchor="center")
        self.inv_tree.pack(fill=tk.BOTH, expand=True)
        self.inv_tree.bind("<<TreeviewSelect>>", self.select_item)

        right = tk.Frame(main, bg=self.colors["dashboard_bg"], padx=20, pady=20)
        right.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(right, text="Manage Inventory", font=("Roboto", 12, "bold"), bg=self.colors["dashboard_bg"]).pack(pady=(0,15))
        
        self.inv_entries = {}
        fields = ["Item Name", "Category", "Quantity", "Unit of Measure", "Status"]
        for f in fields:
            tk.Label(right, text=f, bg=self.colors["dashboard_bg"]).pack(anchor="w")
            if f == "Status":
                cb = ttk.Combobox(right, values=["In Stock", "Low Stock", "Out of Stock", "Discontinued"], state="readonly")
                cb.pack(fill=tk.X, pady=(0,5))
                cb.current(0)
                self.inv_entries[f] = cb
            else:
                e = tk.Entry(right)
                e.pack(fill=tk.X, pady=(0,5))
                self.inv_entries[f] = e
        
        btn_fr = tk.Frame(right, bg=self.colors["dashboard_bg"])
        btn_fr.pack(fill=tk.X, pady=10)
        tk.Button(btn_fr, text="Add", bg=self.colors["upcoming"], command=self.save_item).pack(fill=tk.X, pady=2)
        tk.Button(btn_fr, text="Update", bg=self.colors["lowstock"], command=self.update_item).pack(fill=tk.X, pady=2)
        tk.Button(btn_fr, text="Delete", bg=self.colors["vaccine"], command=self.delete_item).pack(fill=tk.X, pady=2)
        tk.Button(btn_fr, text="Clear", command=self.clear_inv_form).pack(fill=tk.X, pady=2)

        self.load_inventory()

    def select_item(self, event):
        sel = self.inv_tree.focus()
        vals = self.inv_tree.item(sel, "values")
        if vals:
            self.selected_inv_id = vals[0]

            mapping = ["Item Name", "Category", "Quantity", "Unit of Measure", "Status"]
            for i, key in enumerate(mapping):
                if key == "Status":
                    self.inv_entries[key].set(vals[i+1])
                else:
                    self.inv_entries[key].delete(0, tk.END)
                    self.inv_entries[key].insert(0, vals[i+1])


    def save_item(self):
        try:
            qty = int(self.inv_entries["Quantity"].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be a number")
            return

        if qty <= 0:
            status = "Out of Stock"
        elif qty < 5:
            status = "Low Stock"
        else:
            status = "In Stock"

        vals = [
            self.inv_entries["Item Name"].get(),
            self.inv_entries["Category"].get(),
            qty,
            self.inv_entries["Unit of Measure"].get(),
            status
        ]

        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "INSERT INTO inventory (item_name, category, quantity, unit_measure, status) VALUES (?,?,?,?,?)",
            vals
        )
        conn.commit()
        conn.close()

        self.clear_inv_form()
        self.update_dashboard_stats()

    def update_item(self):
        if not self.selected_inv_id:
            return

        try:
            qty = int(self.inv_entries["Quantity"].get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be a number")
            return

        if qty <= 0:
            status = "Out of Stock"
        elif qty < 5:
            status = "Low Stock"
        else:
            status = "In Stock"

        vals = [
            self.inv_entries["Item Name"].get(),
            self.inv_entries["Category"].get(),
            qty,
            self.inv_entries["Unit of Measure"].get(),
            status,
            self.selected_inv_id
        ]

        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "UPDATE inventory SET item_name=?, category=?, quantity=?, unit_measure=?, status=? WHERE id=?",
            vals
        )
        conn.commit()
        conn.close()

        self.clear_inv_form()
        self.update_dashboard_stats()

    def delete_item(self):
        if not self.selected_inv_id: return
        conn = sqlite3.connect(DB_NAME)
        conn.execute("DELETE FROM inventory WHERE id=?", (self.selected_inv_id,))
        conn.commit()
        conn.close()
        self.clear_inv_form()
        self.update_dashboard_stats()

    def clear_inv_form(self):
        self.selected_inv_id = None
        for key, e in self.inv_entries.items():
            if key == "Status": e.current(0)
            else: e.delete(0, tk.END)
        self.load_inventory()

    def load_inventory(self, event=None):
        for i in self.inv_tree.get_children(): self.inv_tree.delete(i)
        search = self.inv_search_var.get()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        if search:
            c.execute("SELECT * FROM inventory WHERE item_name LIKE ? OR category LIKE ?", (f"%{search}%", f"%{search}%"))
        else:
            c.execute("SELECT * FROM inventory")
        for row in c.fetchall(): self.inv_tree.insert("", tk.END, values=row)
        conn.close()
        self.apply_inv_zebra_strip()

    def apply_inv_zebra_strip(self):
        for i, item in enumerate(self.inv_tree.get_children()):
            if i % 2 == 0:
                self.inv_tree.item(item, tags=("even",))
            else:
                self.inv_tree.item(item, tags=("odd",))
        self.inv_tree.tag_configure("even", background=self.colors["zebra_even"])
        self.inv_tree.tag_configure("odd", background=self.colors["zebra_odd"])

    # ================= INVOICES =================
    def show_invoice_ui(self):
        main = tk.Frame(self.body_frame, bg='white')
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = tk.Frame(main, bg='white')
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,10))
        tk.Label(left, text="Invoices List", font=("Roboto", 16, "bold"), bg='white').pack(anchor="w", pady=10)
        
        search_fr = tk.Frame(left, bg='white')
        search_fr.pack(fill=tk.X, pady=(0,5))
        tk.Label(search_fr, text="Search Invoice:", bg='white').pack(side=tk.LEFT)
        s_ent = tk.Entry(search_fr, textvariable=self.invc_search_var)
        s_ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        s_ent.bind("<KeyRelease>", self.load_invoices)

        cols = ("ID", "Date", "Client", "Desc", "Amount")
        self.invc_tree = ttk.Treeview(left, columns=cols, show="headings", height=15)
        for c in cols:
            self.invc_tree.heading(c, text=c)
            self.invc_tree.column(c, width=90)
        self.invc_tree.pack(fill=tk.BOTH, expand=True)
        self.invc_tree.bind("<<TreeviewSelect>>", self.display_receipt)

        mid = tk.Frame(main, bg=self.colors["dashboard_bg"], padx=15, pady=20)
        mid.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        tk.Label(mid, text="Create Invoice", font=("Roboto", 12, "bold"), bg=self.colors["dashboard_bg"]).pack(pady=(0,15))
        
        self.invc_entries = {}
        for f in ["Date", "Client Name", "Description", "Amount"]:
            tk.Label(mid, text=f, bg=self.colors["dashboard_bg"]).pack(anchor="w")
            e = tk.Entry(mid, width=20)
            if f == "Date": e.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
            e.pack(fill=tk.X, pady=(0,5))
            self.invc_entries[f] = e
        
        btn_fr = tk.Frame(mid, bg=self.colors["dashboard_bg"])
        btn_fr.pack(fill=tk.X, pady=10)

        tk.Button(
            btn_fr,
            text="Generate",
            bg=self.colors["vaccine"],
            command=self.save_invoice
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            btn_fr,
            text="Delete",
            bg=self.colors["lowstock"],
            command=self.delete_invoice
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            btn_fr,
            text="Print",
            bg=self.colors["upcoming"],
            command=self.print_invoice
        ).pack(fill=tk.X, pady=2)
 
        self.receipt_frame = tk.Frame(main, bg="white", bd=2, relief=tk.RIDGE, width=250)
        self.receipt_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.receipt_frame.pack_propagate(False)

        tk.Label(self.receipt_frame, text="PAWSITIVE TREAT", font=("Courier", 14, "bold"), bg="white").pack(pady=(20, 5))
        tk.Label(self.receipt_frame, text="Official Receipt", font=("Courier", 10), bg="white").pack()
        tk.Label(self.receipt_frame, text="-----------------------", font=("Courier", 10), bg="white").pack()
        
        self.r_date = tk.StringVar(value="Date: YYYY-MM-DD")
        self.r_client = tk.StringVar(value="Client: [Name]")
        self.r_id = tk.StringVar(value="Invoice #: [ID]")
        
        tk.Label(self.receipt_frame, textvariable=self.r_date, font=("Courier", 10), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(self.receipt_frame, textvariable=self.r_id, font=("Courier", 10), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(self.receipt_frame, textvariable=self.r_client, font=("Courier", 10), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(self.receipt_frame, text="-----------------------", font=("Courier", 10), bg="white").pack(pady=5)
        
        self.r_desc = tk.StringVar(value="Item...")
        tk.Label(self.receipt_frame, textvariable=self.r_desc, font=("Courier", 12), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=10)
        tk.Label(self.receipt_frame, text="-----------------------", font=("Courier", 10), bg="white").pack(pady=5)
        
        self.r_total = tk.StringVar(value="Total: ₱0.00")
        tk.Label(self.receipt_frame, textvariable=self.r_total, font=("Courier", 14, "bold"), bg="white", anchor="e").pack(fill=tk.X, padx=10, pady=10)
        tk.Label(self.receipt_frame, text="Thank you!", font=("Courier", 10, "italic"), bg="white").pack(side=tk.BOTTOM, pady=20)

        self.load_invoices()

    def display_receipt(self, event):
        selected = self.invc_tree.focus()
        vals = self.invc_tree.item(selected, "values")
        if vals:
            self.selected_invoice_id = vals[0]
            self.r_id.set(f"Invoice #: {vals[0]}")
            self.r_date.set(f"Date: {vals[1]}")
            self.r_client.set(f"Client: {vals[2]}")
            self.r_desc.set(vals[3])
            self.r_total.set(f"Total: ₱{vals[4]}")

    def delete_invoice(self):
        if not hasattr(self, "selected_invoice_id"):
            messagebox.showwarning("No Selection", "Please select an invoice to delete.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this invoice?"
        )
        if not confirm:
            return

        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "DELETE FROM invoices WHERE id=?",
            (self.selected_invoice_id,)
        )
        conn.commit()
        conn.close()

        self.selected_invoice_id = None
        self.clear_receipt()
        self.load_invoices()

    def clear_receipt(self):
        self.r_id.set("Invoice #: [ID]")
        self.r_date.set("Date: YYYY-MM-DD")
        self.r_client.set("Client: [Name]")
        self.r_desc.set("Item...")
        self.r_total.set("Total: ₱0.00")

    def save_invoice(self):
        vals = [self.invc_entries[f].get() for f in self.invc_entries]

        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "INSERT INTO invoices (date, client_name, description, amount) VALUES (?,?,?,?)",
            vals
        )
        conn.commit()
        conn.close()

        for e in self.invc_entries.values():
            e.delete(0, tk.END)

        self.clear_receipt()
        self.load_invoices()

    def print_invoice(self):
        if not hasattr(self, "selected_invoice_id"):
            messagebox.showwarning("No Selection", "Please select an invoice to print.")
            return

        content = f"""
    PAWSITIVE TREAT
    Official Receipt
    -----------------------
    {self.r_date.get()}
    {self.r_id.get()}
    {self.r_client.get()}
    -----------------------
    {self.r_desc.get()}
    -----------------------
    {self.r_total.get()}

    Thank you!
    """

        filename = f"invoice_{self.selected_invoice_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content.strip())

        messagebox.showinfo(
            "Printed",
            f"Invoice saved as {filename}\nYou can now print it."
        )

    def load_invoices(self, event=None):
        for i in self.invc_tree.get_children(): self.invc_tree.delete(i)
        search = self.invc_search_var.get()
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        if search:
            c.execute("SELECT * FROM invoices WHERE client_name LIKE ? OR description LIKE ? OR id LIKE ?", (f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            c.execute("SELECT * FROM invoices")
        for row in c.fetchall(): self.invc_tree.insert("", tk.END, values=row)
        conn.close()

    

# ================= RUN =================
if __name__ == "__main__":
    init_db()
    ensure_pets_table_schema()  

    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()

