from tkinter import ttk, messagebox, filedialog
from threading import Thread
from urllib.parse import urlparse


import uuid
import tkinter as tk
import os
import time
import requests
import queue

control_queue = queue.Queue()

DOWNLOAD_FROMFILE = 1
DOWNLOAD_FROMURL = 2
UPLOAD = 3


import pdxwave.Backsys as Backsys


def main():
    
    def file_select(file_type):
        """
        Opens a file dialog for selecting a file of the given type.
        Returns the file path or an empty string if no file is selected.
        """
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = filedialog.askopenfilename(filetypes=[("", file_type)], initialdir=iDir)
        return file_name


    def download(file_name):
        """
        Handles the file download operation using Backsys.
        """
        if Backsys is None:
            messagebox.showerror("Error", "Backsys module is not available.")
            return

        if not file_name:
            messagebox.showerror("Error", "No file selected.")
            return

        try:
            Backsys.download_file(file_name)
            messagebox.showinfo("Done", "Download completed.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")


    def is_valid_url(url):
        """
        Validates the URL format.
        """
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])


    def download_url():
        """
        Downloads a .pdxwave file from a URL and optionally deletes it afterward.
        """
        if Backsys is None:
            messagebox.showerror("Error", "Backsys module is not available.")
            return

        url = entry_pwf_url.get().strip()
        if not url:
            messagebox.showerror("Error", "URL cannot be empty.")
            return

        if not is_valid_url(url):
            messagebox.showerror("Error", "Invalid URL format.")
            return

        file_name = str(uuid.uuid4()) + ".tmp.pdxwave"
        try:
            # Download the file and save it locally
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses

            with open(file_name, "wb") as file:
                file.write(response.content)

            # Process the downloaded file
            Backsys.download_file(file_name)

            # Optionally delete the file after processing
            if check_pwf_url_checked.get() and os.path.exists(file_name):
                os.remove(file_name)

            messagebox.showinfo("Done", "Download completed.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Network error: {e}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Downloaded file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
        finally:
            # Ensure the file is deleted in case of any failure, if the option is checked
            if check_pwf_url_checked.get() and os.path.exists(file_name):
                os.remove(file_name)


    def upload(file_name):
        """
        Handles the file upload operation using Backsys.
        """
        if Backsys is None:
            messagebox.showerror("Error", "Backsys module is not available.")
            return

        if not file_name:
            messagebox.showerror("Error", "No file selected.")
            return

        try:
            Backsys.upload_file(file_name)
            messagebox.showinfo("Done", "Upload completed.")
        except FileNotFoundError:
            messagebox.showerror("Error", "File does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")


    def add_queue(type_: int):
        """
        adding controls to "Control Queue"
        """
        if type_ == DOWNLOAD_FROMURL:
            control_queue.put([f"Download(from URL)", download_url])
        elif type_ == DOWNLOAD_FROMFILE:
            file_name = file_select("*.pdxwave")
            control_queue.put([f"Download {file_name}", lambda: download(file_name)])
        elif type_ == UPLOAD:
            file_name = file_select("*")
            control_queue.put([f"Upload {file_name}", lambda: upload(file_name)])


    #######################


    def queue_run_loop():
        while True:
            if control_queue.empty():
                log, func = control_queue.get()
                func()
                queue_list.insert(tk.END, log)
            time.sleep(0.1)


    #######################

    # daemon start

    Thread(target=queue_run_loop, daemon=True).start()

    #######################

    # UI Setup

    root = tk.Tk()
    root.title("PDX Wave v0.0.5")
    root.geometry("800x600")

    # Menubar
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    # File menu commands
    file_menu.add_command(label="Download", command=lambda: add_queue(DOWNLOAD_FROMFILE))
    file_menu.add_command(label="Upload", command=lambda: add_queue(UPLOAD))

    # Edit menu commands


    # URL download components
    label_pwf_url = tk.Label(root, text=".pdxwave File URL:")
    entry_pwf_url = tk.Entry(root)
    button_pwf_url = tk.Button(
        root, text="Download", command=lambda: add_queue(DOWNLOAD_FROMURL)
    )
    check_pwf_url_checked = tk.BooleanVar()
    check_pwf_url = tk.Checkbutton(
        root, variable=check_pwf_url_checked, text="Delete .pdxwave after download"
    )

    ttk.Separator(root, orient="horizontal").grid(
        row=1, column=0, columnspan=4, pady=10, sticky="ew"
    )

    queue_list = tk.Listbox(root, width=30)
    queue_label = tk.Label(root, text="Queue List")

    # Grid layout for URL download components
    label_pwf_url.grid(column=0, row=0, sticky="news")
    entry_pwf_url.grid(column=1, row=0, sticky="news")
    button_pwf_url.grid(column=2, row=0, sticky="news")
    check_pwf_url.grid(column=3, row=0, sticky="news")

    queue_label.grid(column=0, row=2)
    queue_list.grid(column=0, row=3)

    # Set the menubar
    root.config(menu=menubar)
    root.mainloop()
