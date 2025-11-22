import os
import shutil
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


#   ------- EVENT HANDLER CLASS -----------

class MyHandler(FileSystemEventHandler):
    def __init__(self, parentFolder, imgFolder, docsFolder):
        self.parentFolder = parentFolder
        self.imgFolder = imgFolder
        self.docsFolder = docsFolder

        # Mapping of file extensions → target folders
        self.mapping = {
            ".jpg": self.imgFolder,
            ".jpeg": self.imgFolder,
            ".png": self.imgFolder,
            ".pdf": self.docsFolder,
            ".txt": self.docsFolder,
            ".docx": self.docsFolder
        }

    def organize_file(self, file_path):
        if not os.path.isfile(file_path):
            return

        ext = os.path.splitext(file_path)[1].lower()

        if ext in self.mapping:
            target_folder = self.mapping[ext]
            filename = os.path.basename(file_path)
            target_path = os.path.join(target_folder, filename)

            try:
                shutil.move(file_path, target_path)
                print(f"Moved: {filename} → {target_folder}")
            except Exception as e:
                print("Error moving file:", e)

    def on_created(self, event):
        print(f"New file created: {event.src_path}")
        self.organize_file(event.src_path)


#  -------------- ORGANIZE EXISTING FILES -----------

def organize_existing_files(root_folder, handler):
    for file in os.listdir(root_folder):
        full_path = os.path.join(root_folder, file)

        if os.path.isfile(full_path):
            handler.organize_file(full_path)


#  ----------- TKINTER UI --------------

root = tk.Tk()
root.title("File Organizer")
root.geometry("400x280")

selected_folder = None
image_folder_name = None
docs_folder_name = None


def choose_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory(title="Select Folder to Organize")
    folder_label.config(text=selected_folder)


tk.Button(root, text="Choose Folder", command=choose_folder).pack(pady=10)

folder_label = tk.Label(root, text="No folder selected")
folder_label.pack()

tk.Label(root, text="Folder name for Images:").pack()
image_entry = tk.Entry(root)
image_entry.pack()

tk.Label(root, text="Folder name for Documents:").pack()
docs_entry = tk.Entry(root)
docs_entry.pack()


# ------------------------------
#   START WATCHDOG
# ------------------------------

def initializeBot():
    global selected_folder, image_folder_name, docs_folder_name

    image_folder_name = image_entry.get().strip()
    docs_folder_name = docs_entry.get().strip()

    root.destroy()
    startWatchDog()


def startWatchDog():
    global selected_folder, image_folder_name, docs_folder_name

    if not selected_folder:
        print("Select a folder first!")
        return

    # create subfolders inside selected folder
    images_folder = os.path.join(selected_folder, image_folder_name)
    docs_folder = os.path.join(selected_folder, docs_folder_name)

    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(docs_folder, exist_ok=True)

    handler = MyHandler(selected_folder, images_folder, docs_folder)

    # Organize existing files before starting watchdog
    organize_existing_files(selected_folder, handler)

    observer = Observer()
    observer.schedule(handler, path=selected_folder, recursive=False)
    observer.start()

    print("Watching for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


tk.Button(root, text="Start Organizing", command=initializeBot).pack(pady=15)

root.mainloop()
