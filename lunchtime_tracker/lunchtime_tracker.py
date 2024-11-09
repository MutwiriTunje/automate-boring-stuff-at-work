import pdfplumber  
import csv
import pandas as pd
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
import webbrowser

# Step 1: Define PDF to CSV Conversion Function
def pdf_to_csv(pdf_path, csv_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            writer.writerow(row)
# Step 2: Define Shift Analysis Program
def analyze_shifts(csv_path, is_weekend):
    df = pd.read_csv(csv_path, skiprows=1)
    df['Person ID'] = df['Person ID'].astype(str).str.strip("'").str.strip()

    if is_weekend:
        shift_times = {
            "shift_1": (datetime.strptime("12:00:00", "%H:%M:%S").time(), datetime.strptime("12:25:59", "%H:%M:%S").time()),
            "shift_2": (datetime.strptime("12:25:00", "%H:%M:%S").time(), datetime.strptime("12:50:59", "%H:%M:%S").time()),
            "shift_3": (datetime.strptime("12:50:00", "%H:%M:%S").time(), datetime.strptime("13:15:59", "%H:%M:%S").time()),
            "shift_4": (datetime.strptime("13:15:00", "%H:%M:%S").time(), datetime.strptime("13:40:59", "%H:%M:%S").time()),
        }
        time_limit = ("12:00", "14:00")
    else:
        shift_times = {
            "shift_1": (datetime.strptime("12:00:00", "%H:%M:%S").time(), datetime.strptime("12:45:59", "%H:%M:%S").time()),
            "shift_2": (datetime.strptime("12:45:00", "%H:%M:%S").time(), datetime.strptime("13:30:59", "%H:%M:%S").time()),
            "shift_3": (datetime.strptime("13:30:00", "%H:%M:%S").time(), datetime.strptime("14:15:59", "%H:%M:%S").time()),
            "shift_4": (datetime.strptime("14:15:00", "%H:%M:%S").time(), datetime.strptime("15:00:59", "%H:%M:%S").time()),
        }
        time_limit = ("12:00", "16:00")

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df = df.dropna(subset=['Time'])
    df = df[(df['Time'].dt.time >= datetime.strptime(time_limit[0], "%H:%M").time()) & 
            (df['Time'].dt.time <= datetime.strptime(time_limit[1], "%H:%M").time())]

    employee_shifts = {
        '34': "shift_1", '83': "shift_1", '102': "shift_1", '43': "shift_1", '94': "shift_1", '110': "shift_1",
        '107': "shift_1", '16': "shift_2", '31': "shift_2", '18': "shift_2", '82': "shift_2", '105': "shift_2",
        '57': "shift_2", '108': "shift_2", '13': "shift_2", '24': "shift_3", '12': "shift_3", '33': "shift_3",
        '7': "shift_3", '96': "shift_3", '109': "shift_3", '103': "shift_3", '32': "shift_3", '97': "shift_4",
        '35': "shift_4", '5': "shift_4", '90': "shift_4", '37': "shift_4", '10': "shift_4", '85': "shift_4",
        '87': "shift_4", '54': "shift_4",
    }

    results = []
    for person_id, group in df.groupby('Person ID'):
        if person_id not in employee_shifts:
            continue

        shift_name = employee_shifts[person_id]
        shift_start, shift_end = shift_times[shift_name]
        group = group.sort_values('Time')
        earliest_check = group['Time'].iloc[0].time()
        latest_check = group['Time'].iloc[-1].time()

        out_of_shift_time = 0
        if earliest_check < shift_start or latest_check > shift_end:
            out_of_shift_time = (datetime.combine(datetime.today(), latest_check) - 
                                 datetime.combine(datetime.today(), earliest_check)).total_seconds() / 60

            results.append({
                "Name": group['Name'].iloc[0],
                "Person ID": person_id,
                "Assigned Shift": shift_name,
                "Minutes Outside Shift": out_of_shift_time,
                "keyed out at": earliest_check,
                "keyed in at": latest_check
            })

    return pd.DataFrame(results)



# Step 3: Create CustomTkinter GUI
def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filename:
        entry_pdf_path.delete(0, ctk.END)
        entry_pdf_path.insert(0, filename)

def convert_and_analyze():
    pdf_path = entry_pdf_path.get()
    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file.")
        return

    csv_path = pdf_path.rsplit(".", 1)[0] + ".csv"
    pdf_to_csv(pdf_path, csv_path)
    
    # Get the selected toggle state (True for weekend, False for weekday)
    is_weekend = weekend_toggle.get()

    results_df = analyze_shifts(csv_path, is_weekend)

    for row in treeview.get_children():
        treeview.delete(row)

    if results_df.empty:
        messagebox.showinfo("Results", "No entries found outside assigned shifts.")
    else:
        for _, row in results_df.iterrows():
            treeview.insert("", "end", values=(row["Name"], row["Person ID"], row["Assigned Shift"],
                                               row["Minutes Outside Shift"], row["keyed out at"], row["keyed in at"]))

# function to change appearance mode
def change_appearance_mode(new_mode):
    ctk.set_appearance_mode(new_mode)

# Set up CustomTkinter window
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("Lunch Time Lateness Tracker")

# Load and Display Company Logo
logo_path = "assets/images/logo.png"  # Replace with the actual path to your logo file
logo_image = ctk.CTkImage(Image.open(logo_path), size=(100, 70))

logo_label = ctk.CTkLabel(root, image=logo_image, text="")
logo_label.pack(pady=10)

# Main Frame for Input and Buttons
frame = ctk.CTkFrame(root)
frame.pack(padx=10, pady=10, fill="both", expand=True)

label_pdf_path = ctk.CTkLabel(frame, text="Select PDF File:")
label_pdf_path.grid(row=0, column=0, padx=5, pady=5)

entry_pdf_path = ctk.CTkEntry(frame, width=400)
entry_pdf_path.grid(row=0, column=1, padx=5, pady=5)

button_browse = ctk.CTkButton(frame, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2, padx=5, pady=5)

button_convert = ctk.CTkButton(frame, text="Convert and Analyze", command=convert_and_analyze)
button_convert.grid(row=1, column=0, columnspan=3, pady=10)

# Weekday/Weekend Toggle
weekend_toggle_label = ctk.CTkLabel(frame, text="Toggle for Weekend Shifts:")
weekend_toggle_label.grid(row=2, column=0, padx=5, pady=5)

weekend_toggle = ctk.CTkSwitch(frame, text="Weekend", onvalue=True, offvalue=False)
weekend_toggle.grid(row=2, column=1, padx=5, pady=5)

# Appearance mode selection
appearance_frame = ctk.CTkFrame(root)
appearance_frame.pack(fill="x", padx=10, pady=5)

label_appearance = ctk.CTkLabel(appearance_frame, text="Appearance Mode:")
label_appearance.grid(row=0, column=0, padx=5)

appearance_mode_options = ["Light", "Dark"]
appearance_mode_dropdown = ctk.CTkOptionMenu(appearance_frame, values=appearance_mode_options, command=change_appearance_mode)
appearance_mode_dropdown.grid(row=0, column=1, padx=5)

# Treeview for displaying results
treeview = ttk.Treeview(root, columns=("Name", "Person ID", "Assigned Shift", "Minutes Outside Shift", "Keyed Out At", "Keyed In At"), show="headings")
treeview.heading("Name", text="Name")
treeview.heading("Person ID", text="Person ID")
treeview.heading("Assigned Shift", text="Assigned Shift")
treeview.heading("Minutes Outside Shift", text="Minutes Outside Shift")
treeview.heading("Keyed Out At", text="Keyed Out At")
treeview.heading("Keyed In At", text="Keyed In At")
treeview.pack(padx=10, pady=10, fill="both", expand=True)

# Footer
footer_frame = ctk.CTkFrame(root)
footer_frame.pack(fill="x")

footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Tunje Mutwiri. All rights reserved.", anchor="center")
footer_label.pack(pady=5)

# Define function to open website
def open_website(event):
    webbrowser.open("https://mutwiritunje.github.io/")  # Replace with your actual URL
# Combined label text with only the website part clickable
contact_text = "Reach out: www.MutwiriTunje.github.io | +254792397230"  

# Display centered contact information
contact_info_label = ctk.CTkLabel(
    footer_frame, 
    text=contact_text,
    anchor="center",
    cursor="hand2"  # Sets cursor as hand when hovering over the label
)
contact_info_label.pack(pady=5)

# Bind the click event to only the website portion
contact_info_label.bind("<Button-1>", open_website)

# Center frame and start the main loop
footer_frame.pack(anchor="center")


root.mainloop()
