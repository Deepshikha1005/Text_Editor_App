# Import tkinter module for creating GUI applications
import tkinter as tk

# Import submodule filedialog for open/save dialogs and submodule messagebox for popups
from tkinter import filedialog, messagebox,simpledialog,colorchooser
from tkinter import font


# -------------------- MAIN WINDOW --------------------

# Create main application window
root = tk.Tk()

# Set window title
root.title("Simple Text Editor")

# Set window size
root.geometry("800x600")


# -------------------- TEXT EDITOR AREA --------------------

# Create text editor area
text = tk.Text(
    root,                    # Parent window
    wrap=tk.WORD,            # Wrap text by words (not characters)
    font=("Helvetica", 12),  # Font style and size
    undo=True
)

# Make text area fill the entire window
text.pack(expand=True, fill=tk.BOTH)


# -------------------- FILE FUNCTIONS --------------------

# Function to create a new file (clear all text)
def new_file():
    # Delete all text from the text box (from start to end)
    text.delete(1.0, tk.END)


# Function to open an existing text file
def open_file():
    # Open file dialog to select a text file
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",            # Default file extension
        filetypes=[("Text Files", "*.txt")] # Allow only .txt files
    )

    # Check if a file is selected
    if file_path:
        # Open the selected file in read mode
        with open(file_path, "r") as file:
            # Clear old text from editor
            text.delete(1.0, tk.END)
            # Insert file content into the text editor
            text.insert(tk.END, file.read())


# Function to save the current text to a file
def save_file():
    # Open save file dialog
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",            # Default file extension
        filetypes=[("Text Files", "*.txt")] # Allow only .txt files
    )
    
def find_text():
    # User se search word lo
    search_word = simpledialog.askstring(
        "Find",
        "Enter text to search:"
    )

    if search_word:
        # Purane highlights remove karo
        text.tag_remove("highlight", "1.0", tk.END)

        start_pos = "1.0"

        while True:
            start_pos = text.search(
                search_word,
                start_pos,
                stopindex=tk.END
            )

            if not start_pos:
                break

            end_pos = f"{start_pos}+{len(search_word)}c"

            text.tag_add(
                "highlight",
                start_pos,
                end_pos
            )

            start_pos = end_pos

        # Highlight color
        text.tag_config(
            "highlight",
            background="yellow"
        )

    # Check if file path is selected
    if file_path:
        # Open file in write mode
        with open(file_path, "w") as file:
            # Write text editor content into file
            file.write(text.get(1.0, tk.END))

        # Show success message after saving file
        messagebox.showinfo("Info", "File saved successfully!")
        

def change_text_color():
    color = colorchooser.askcolor()[1]

    if color:
        text.config(fg=color)

def dark_mode():
    text.config(
        bg="black",
        fg="white",
        insertbackground="white"
    )


def light_mode():
    text.config(
        bg="white",
        fg="black",
        insertbackground="black"
    )


def make_bold():
    text.tag_add("bold", "sel.first", "sel.last")
    text.tag_config("bold", font=("Helvetica", 12, "bold"))

def make_italic():
    text.tag_add("italic", "sel.first", "sel.last")
    text.tag_config("italic", font=("Helvetica", 12, "italic"))

def make_underline():
    text.tag_add("underline", "sel.first", "sel.last")
    text.tag_config("underline", font=("Helvetica", 12, "underline"))
    

def on_closing():
    answer = messagebox.askyesnocancel(
        "Exit",
        "Do you want to save changes?"
    )

    if answer:  # Yes
        save_file()
        root.destroy()

    elif answer is False:  # No
        root.destroy()

    # Cancel par kuch nahi hoga
# -------------------- MENU BAR --------------------

# Create menu bar
menu = tk.Menu(root)

# Attach menu bar to the window
root.config(menu=menu)

# Create File menu
# Dropdown under File which has options like New, Open, Save, Exit
file_menu = tk.Menu(menu)

# Add File menu to menu bar
menu.add_cascade(label="File", menu=file_menu)

# Add New option to File menu
file_menu.add_command(label="New", command=new_file)

# Add Open option to File menu
file_menu.add_command(label="Open", command=open_file)

# Add Save option to File menu
file_menu.add_command(label="Save", command=save_file)

# Add a separator line in menu
file_menu.add_separator()

# Add Exit option to close the application
file_menu.add_command(label="Exit", command=root.quit)

# Create Edit Menu
edit_menu = tk.Menu(menu, tearoff=0)

# Add Edit menu to menu bar
menu.add_cascade(label="Edit", menu=edit_menu)

# Undo
edit_menu.add_command(
    label="Undo",
    command=lambda: text.event_generate("<<Undo>>")
)

# Redo
edit_menu.add_command(
    label="Redo",
    command=lambda: text.event_generate("<<Redo>>")
)

edit_menu.add_separator()

# Cut
edit_menu.add_command(
    label="Cut",
    command=lambda: text.event_generate("<<Cut>>")
)

# Copy
edit_menu.add_command(
    label="Copy",
    command=lambda: text.event_generate("<<Copy>>")
)

# Paste
edit_menu.add_command(
    label="Paste",
    command=lambda: text.event_generate("<<Paste>>")
)

edit_menu.add_separator()

edit_menu.add_command(
    label="Find",
    command=find_text
)

format_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Format", menu=format_menu)

format_menu.add_command(
    label="Text Color",
    command=change_text_color
)


view_menu = tk.Menu(menu, tearoff=0)

menu.add_cascade(
    label="View",
    menu=view_menu
)

view_menu.add_command(
    label="Dark Mode",
    command=dark_mode
)

view_menu.add_command(
    label="Light Mode",
    command=light_mode
)


format_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Format", menu=format_menu)

format_menu.add_command(label="Text Color", command=change_text_color)
format_menu.add_separator()
format_menu.add_command(label="Bold", command=make_bold)
format_menu.add_command(label="Italic", command=make_italic)
format_menu.add_command(label="Underline", command=make_underline)
# -------------------- RUN APPLICATION --------------------

# Keyboard Shortcuts
root.bind("<Control-z>",
          lambda event: text.event_generate("<<Undo>>"))

root.bind("<Control-y>",
          lambda event: text.event_generate("<<Redo>>"))

root.bind("<Control-x>",
          lambda event: text.event_generate("<<Cut>>"))

root.bind("<Control-c>",
          lambda event: text.event_generate("<<Copy>>"))

root.bind("<Control-v>",
          lambda event: text.event_generate("<<Paste>>"))

root.bind(
    "<Control-f>",
    lambda event: find_text()
)

# Run the application continuously
# Starts and keeps the window open
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()