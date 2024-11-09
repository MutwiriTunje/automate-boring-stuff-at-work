import customtkinter as ctk
import pyautogui
import time
import threading
import webbrowser

# Initialize customtkinter with a pink color theme
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("green")  # Green color theme

# Global flag to stop typing
stop_event = threading.Event()

# Timer variables
timer_seconds = 10  # Default countdown time
timer_var = None  # Timer variable (to be created after app initialization)

# Function to start typing
def start_typing():
    stop_event.clear()  # Clear the stop event (to make sure typing can proceed)
    text_to_type = text_box.get("1.0", "end-1c")  # Get text from the text box
    typing_speed = 1 / typing_speed_var.get()  # Typing speed: converted to interval (e.g., speed of 5 = fast typing)
    start_delay = delay_var.get()  # Delay before typing starts

    # Start the countdown timer for sleep delay
    start_sleep_timer(start_delay)

    # Start the countdown before typing
    start_sleep_timer_thread(start_delay)

# Function to stop typing
def stop_typing():
    stop_event.set()  # Trigger the stop event to interrupt typing

# Timer function to update the countdown for sleep delay
def start_sleep_timer(delay):
    global timer_seconds  # Use the global timer_seconds directly
    timer_seconds = delay  # Set the timer to the start delay in seconds
    update_timer()

# Function to update the timer display every second
def update_timer():
    global timer_seconds  # Ensure we reference the global variable
    if timer_seconds <= 0:
        return
    minutes, seconds = divmod(timer_seconds, 60)
    timer_var.set(f"{minutes:02}:{seconds:02}")
    timer_seconds -= 1
    if timer_seconds > 0:
        app.after(1000, update_timer)  # Update every second

# Function to start the countdown in a new thread
def start_sleep_timer_thread(delay):
    def countdown():
        for _ in range(delay, 0, -1):
            time.sleep(1)  # Wait for 1 second
            minutes, seconds = divmod(_, 60)
            timer_var.set(f"{minutes:02}:{seconds:02}")  # Update the timer display
            app.update()  # Update the GUI to show the timer change
        type_text()  # Start typing after the timer ends

    # Start the countdown in a separate thread so that the GUI remains responsive
    threading.Thread(target=countdown).start()

# Function to perform typing once countdown is complete
def type_text():
    text_to_type = text_box.get("1.0", "end-1c")  # Get text from the text box
    typing_speed = 1 / typing_speed_var.get()  # Typing speed as interval (e.g., 1 for slow, 5 for fast)

    for char in text_to_type:
        if stop_event.is_set():  # Check if stop event is triggered
            print("Typing stopped.")
            break
        pyautogui.typewrite(char, interval=typing_speed)

# Function to increase or decrease typing speed
def increase_speed():
    current_speed = typing_speed_var.get()
    if current_speed < 10:  # Limit the speed to a maximum of 10
        typing_speed_var.set(current_speed + 1)

def decrease_speed():
    current_speed = typing_speed_var.get()
    if current_speed > 1:  # Limit the speed to a minimum of 1
        typing_speed_var.set(current_speed - 1)

# Function to increase or decrease start delay
def increase_delay():
    current_delay = delay_var.get()
    if current_delay < 10:
        delay_var.set(current_delay + 1)

def decrease_delay():
    current_delay = delay_var.get()
    if current_delay > 0:
        delay_var.set(current_delay - 1)

# Function to open website
def open_website(event):
    webbrowser.open("https://mutwiritunje.github.io/")  # Replace with your actual URL

# Create the main window
app = ctk.CTk()
app.title("Crafted for Marjicc, because she's pure magic! ✨")
app.geometry("600x500")

# Create a grid layout with 1 row and 2 columns (75% for text, 25% for controls)
app.grid_columnconfigure(0, weight=4)  # 75% for text box
app.grid_columnconfigure(1, weight=1)  # 25% for controls
app.grid_rowconfigure(1, weight=1)  # Ensure text box expands

# Label and Text box
text_label = ctk.CTkLabel(app, text="Enter text to type:")
text_label.grid(row=0, column=0, pady=10, sticky="w")  # Align the label to the top-left

# Make the textbox larger (expand and fill the available space)
text_box = ctk.CTkTextbox(app, height=10)
text_box.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")  # Use sticky="nsew" for full expansion

# Left side buttons for speed and delay controls (in the second column)
left_frame = ctk.CTkFrame(app)
left_frame.grid(row=0, column=1, rowspan=2, pady=10, sticky="nsew")

# Speed Controls
speed_label = ctk.CTkLabel(left_frame, text="Typing Speed (1-10):")
speed_label.pack(pady=5)

typing_speed_var = ctk.IntVar(value=3)  # Default speed
typing_speed_display = ctk.CTkLabel(left_frame, textvariable=typing_speed_var)
typing_speed_display.pack(pady=5)

speed_increase_button = ctk.CTkButton(left_frame, text="+", command=increase_speed, fg_color="#FF1493")
speed_increase_button.pack(side="top", pady=5)
speed_decrease_button = ctk.CTkButton(left_frame, text="-", command=decrease_speed, fg_color="#FF1493")
speed_decrease_button.pack(side="top", pady=5)

# Start Delay Controls
delay_label = ctk.CTkLabel(left_frame, text="Start Delay (seconds):")
delay_label.pack(pady=5)

delay_var = ctk.IntVar(value=5)  # Default delay
delay_display = ctk.CTkLabel(left_frame, textvariable=delay_var)
delay_display.pack(pady=5)

delay_increase_button = ctk.CTkButton(left_frame, text="+", command=increase_delay, fg_color="#FF1493")
delay_increase_button.pack(side="top", pady=5)
delay_decrease_button = ctk.CTkButton(left_frame, text="-", command=decrease_delay, fg_color="#FF1493")
delay_decrease_button.pack(side="top", pady=5)

# Timer Display
timer_label = ctk.CTkLabel(app, text="ETA for Sleep Timer:")
timer_label.grid(row=2, column=0, pady=5, sticky="w")

timer_var = ctk.StringVar(value="00:00")  # Initial countdown timer display
timer_display = ctk.CTkLabel(app, textvariable=timer_var, font=("Arial", 20))
timer_display.grid(row=2, column=0, pady=5, sticky="e")

# Start Button
start_button = ctk.CTkButton(app, text="Start Typing", command=start_typing, fg_color="#FF1493")
start_button.grid(row=3, column=0, pady=10)

# Stop Button
stop_button = ctk.CTkButton(app, text="Stop Typing", command=stop_typing, fg_color="#FF1493")
stop_button.grid(row=3, column=1, pady=10)

# Footer Section
footer_frame = ctk.CTkFrame(app)
footer_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Tunje Mutwiri. All rights reserved.", anchor="center")
footer_label.pack(pady=5)

contact_text = "Reach out: www.MutwiriTunje.github.io | +254792397230"
contact_info_label = ctk.CTkLabel(
    footer_frame, 
    text=contact_text,
    anchor="center",
    cursor="hand2"
)
contact_info_label.pack(pady=5)
contact_info_label.bind("<Button-1>", open_website)

# Start the main loop
app.mainloop()
