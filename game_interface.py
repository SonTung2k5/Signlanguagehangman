import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import PIL for handling jpg images
import subprocess
import sys
import os
import pygame  # Import pygame for playing sound
import pandas as pd

# Initialize pygame mixer
pygame.mixer.init()

def start_game():
    # Open level selection window
    level_window = tk.Toplevel(root)
    level_window.title("Select Level")
    level_window.geometry("400x300")

    def start_level(level):
        # Play the sound
        pygame.mixer.music.load('genshin.mp3')  # Ensure you have a start_sound.mp3 file in the same directory
        pygame.mixer.music.play()
        
        # Run the hangman game script with the selected level
        try:
            subprocess.Popen([sys.executable, 'hangman_game.py', level])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start the game: {e}")
        level_window.destroy()

    # Create buttons for level selection
    easy_button = tk.Button(level_window, text="FOOD", command=lambda: start_level('easy'), **button_style)
    easy_button.pack(pady=20)
    easy_button.bind("<Enter>", on_enter)
    easy_button.bind("<Leave>", on_leave)

    medium_button = tk.Button(level_window, text="Clothes", command=lambda: start_level('medium'), **button_style)
    medium_button.pack(pady=20)
    medium_button.bind("<Enter>", on_enter)
    medium_button.bind("<Leave>", on_leave)

    hard_button = tk.Button(level_window, text="Animals", command=lambda: start_level('hard'), **button_style)
    hard_button.pack(pady=20)
    hard_button.bind("<Enter>", on_enter)
    hard_button.bind("<Leave>", on_leave)

def save_name():
    # Save the user's name
    name = name_entry.get()
    if name:
        with open('user_name.txt', 'w') as f:
            f.write(name)
        messagebox.showinfo("Info", "Name saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter your name.")

def exit_game():
    # Exit the application
    root.destroy()

def open_guide():
    guide_image_path = "signlanguage.jpg"  # Replace with the actual path to your image
    try:
        guide_image = Image.open(guide_image_path)
        guide_image.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open guide image: {e}")

def on_enter(e):
    e.widget['background'] = '#A0522D'  # Darker brown when hovered

def on_leave(e):
    e.widget['background'] = '#8B4513'  # Original brown color

# Create the main window
root = tk.Tk()
root.title("Hangman Game Interface")
root.geometry("800x600")  # Increase the window size

# Load the background image
try:
    background_image = Image.open("newbg.jpg")  # Ensure you have a hangman background.jpg file in the same directory
    background_image = background_image.resize((800, 600), Image.LANCZOS)  # Resize the image to fit the window
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tk.Label(root, image=background_photo)
    background_label.place(relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load background image: {e}")

# Load the Play icon image
try:
    play_icon = Image.open("play_icon.png")  # Ensure you have a play_icon.png file in the same directory
    play_icon = play_icon.resize((50, 50), Image.LANCZOS)  # Resize the icon as needed
    play_icon_photo = ImageTk.PhotoImage(play_icon)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load play icon: {e}")

# Load the Exit icon image
try:
    exit_icon = Image.open("exit_icon.png")  # Ensure you have an exit_icon.png file in the same directory
    exit_icon = exit_icon.resize((50, 50), Image.LANCZOS)  # Resize the icon as needed
    exit_icon_photo = ImageTk.PhotoImage(exit_icon)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load exit icon: {e}")

# Load the Guide icon image
try:
    guide_icon = Image.open("guide_icon.png")  # Ensure you have a guide_icon.png file in the same directory
    guide_icon = guide_icon.resize((50, 50), Image.LANCZOS)  # Resize the icon as needed
    guide_icon_photo = ImageTk.PhotoImage(guide_icon)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load guide icon: {e}")

# Customize button appearance for a hangman game look
button_style = {
    "bg": "#8B4513",  # Brown background
    "fg": "#FFFFFF",  # White text
    "font": ("Courier", 20, "bold"),  # Increase font size
    "bd": 5,  # Border width
    "relief": "ridge",  # Border style
    "highlightthickness": 0,  # Remove highlight border
    "highlightbackground": "#8B4513",  # Same as button background
    "highlightcolor": "#8B4513",  # Same as button background
    "activebackground": "#A0522D",  # Darker brown when pressed
    "cursor": "hand2",  # Change cursor to hand when hovering
    "takefocus": 0  # Remove focus highlight
}

# Create a frame to hold the name entry and save button
name_frame = tk.Frame(root, bg='#80c1ff', bd=5)
name_frame.place(relx=0.5, rely=0.15, anchor='center')  # Adjust rely to position the frame

# Create the name entry
name_label = tk.Label(name_frame, text="Enter your name:", bg='#80c1ff', font=("Helvetica", 16))
name_label.pack(pady=10)
name_entry = tk.Entry(name_frame, font=("Helvetica", 16), width=20)
name_entry.pack(pady=10)

# Create the Save button
save_button = tk.Button(name_frame, text="Save Name", command=save_name, **button_style)
save_button.pack(pady=20)  # Increase padding
save_button.bind("<Enter>", on_enter)
save_button.bind("<Leave>", on_leave)

# Create a frame to hold the Start button
start_frame = tk.Frame(root, bg='#80c1ff', bd=1)
start_frame.place(relx=0.5, rely=0.7, anchor='center')  # Position in the middle down of the screen

# Create the Start button with Play icon
start_button = tk.Button(start_frame, image=play_icon_photo, command=start_game, **button_style)
start_button.pack(pady=20)  # Increase padding
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# Create a frame to hold the Guide button
guide_frame = tk.Frame(root, bg='#80c1ff', bd=1)
guide_frame.place(relx=0.05, rely=0.05, anchor='nw')  # Position at the top-left corner

# Create the Guide button with Guide icon
guide_button = tk.Button(guide_frame, image=guide_icon_photo, command=open_guide, **button_style)
guide_button.pack(pady=20)  # Increase padding
guide_button.bind("<Enter>", on_enter)
guide_button.bind("<Leave>", on_leave)

# Create a frame to hold the Exit button
exit_frame = tk.Frame(root, bg='#80c1ff', bd=1)
exit_frame.place(relx=0.95, rely=0.05, anchor='ne')  # Position at the top-right corner

# Create the Exit button with Exit icon
exit_button = tk.Button(exit_frame, image=exit_icon_photo, command=exit_game, **button_style)
exit_button.pack(pady=20)  # Increase padding
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

# Run the main loop
root.mainloop()