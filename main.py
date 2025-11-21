import os   
import shutil 
import tkinter as tk 
from tkinter import filedialog


root = tk.Tk() 
root.title("File Organizer") 
root.geometry("400x250") 


# we will use a folder selection dialog so the user doesn't have to type the path

def choose_folder():
    folder = filedialog.askdirectory(title="Select Folder to Organize")
    folder_label.config(text=folder)
    return folder

select_button = tk.Button(root, text="Choose Folder", command=choose_folder)
select_button.pack(pady=10) # adding some spacing

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

tk.Label(root, text="Folder name for Images:").pack()
image_entry = tk.Entry(root)
image_entry.pack()

tk.Label(root, text="Folder name for Documents:").pack()
docs_entry = tk.Entry(root)
docs_entry.pack()


# now here we are writing logic to move files based on their extensions

def organize_files():
    folder_path = folder_label.cget("text")
    if folder_path == "No folder selected":
        print("Please select a folder first !")
        return 
    
    # geting folder names from user
    images_folder = os.path.join(folder_path, image_entry.get())
    docs_folder = os.path.join(folder_path, docs_entry.get())

    # creating folders if they don't exist
    for folder in [images_folder, docs_folder]:
        if not os.path.exists(folder):
            os.mkdir(folder)
    
    mapping = {
        ".jpg": images_folder,
        ".png": images_folder,
        ".jpeg": images_folder,
        ".pdf": docs_folder,
        ".txt": docs_folder,
        ".docx": docs_folder
    }

    # move files
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower() # getting its extension
            if ext in mapping:
                shutil.move(file_path, os.path.join(mapping[ext], file))

start_button = tk.Button(root, text="Start Organizing", command=organize_files)
start_button.pack(pady=10)

root.mainloop()