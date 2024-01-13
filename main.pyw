import os
import shutil
import sys
from tkinter import Tk, Label, Listbox, filedialog, Frame, CENTER, font, ttk, messagebox, Toplevel

import customtkinter

def setup_version_selection(master):
    version_frame = Frame(master, bg="#1e1e1e", padx=20, pady=5)
    version_frame.pack(pady=20)

    label_font = font.Font(family="Helvetica", size=24, weight="bold")
    label = Label(version_frame, text="Select Fabric Version:", bg="#1e1e1e", fg="white", font=label_font)
    label.pack()

    listbox_font = font.Font(family="Helvetica", size=13, weight="bold")

    lunar_path = os.path.join(os.path.expanduser("~"), ".lunarclient", "offline", "multiver", "mods")
    fabric_versions = [d for d in os.listdir(lunar_path) if os.path.isdir(os.path.join(lunar_path, d))]

    style = ttk.Style()
    style.configure("RoundedListbox.TListbox", borderwidth=0, relief="flat", background="#333333", foreground="white", font=listbox_font)

    version_listbox = Listbox(version_frame, selectmode="single", height=len(fabric_versions), width=20, justify=CENTER, selectbackground="green", bg="#333333", fg="white", font=listbox_font, bd=0, relief="flat")
    for version in fabric_versions:
        version_listbox.insert("end", version)
    version_listbox.pack()

    return version_frame, version_listbox

def setup_mod_import(master, version_frame, version_listbox):
    mod_frame = Frame(master, bg="#1e1e1e", padx=10)
    mod_frame.pack(pady=0)

    button_font = customtkinter.CTkFont(family="Helvetica", size=30, weight="bold")
    import_button = customtkinter.CTkButton(mod_frame, text="Load Mod", command=lambda: import_mod(version_listbox), font=button_font, fg_color='#333333', hover_color='green')
    import_button.pack()

    create_page_button = customtkinter.CTkButton(mod_frame, text="Unload Mod", command=lambda: create_new_window(master, version_listbox), font=button_font, fg_color='#333333', hover_color='green')
    create_page_button.pack()

def import_mod(version_listbox):
    selected_version = get_selected_version(version_listbox)

    if not selected_version:
        messagebox.showwarning("Warning", "Please select a Fabric version before importing a mod.")
        return

    lunar_path = os.path.join(os.path.expanduser("~"), ".lunarclient", "offline", "multiver", "mods")
    version_path = os.path.join(lunar_path, selected_version)

    if os.path.exists(version_path):
        mod_path = get_mod_path()

        if mod_path:
            shutil.copy(mod_path, version_path)
            message = f"Mod '{os.path.basename(mod_path)}' imported to '{selected_version}' successfully."
            print(message)
            messagebox.showinfo("Success", message)
    else:
        error_message = f"Error: Lunar Client version '{selected_version}' not found."
        print(error_message)
        messagebox.showerror("Error", error_message)

def get_selected_version(version_listbox):
    selected_indices = version_listbox.curselection()
    return version_listbox.get(selected_indices[0]) if selected_indices else ""

def get_mod_path():
    try:
        mod_path = filedialog.askopenfilename(title="Select Mod to Import", filetypes=[("Jar Files", "*.jar")])
    except Exception as e:
        print(f"Warning: File dialog not available. Please enter the mod path manually.")
        mod_path = input("Enter the full path to the mod file (including filename): ")

    return mod_path

def create_new_window(master, version_listbox):
    selected_version = get_selected_version(version_listbox)

    if not selected_version:
        messagebox.showwarning("Warning", "Please select a Fabric version before unloading a mod.")
        return

    new_window = Toplevel(master)
    new_window.title("Unload Mods")
    new_window.geometry("500x400")
    new_window.resizable(False, False)
    new_window.configure(bg="#1e1e1e")

    version_frame = Frame(new_window, bg="#1e1e1e", padx=20, pady=5)
    version_frame.pack(pady=20)

    label_font = font.Font(family="Helvetica", size=24, weight="bold")
    label = Label(version_frame, text="Select Mod To Unload:", bg="#1e1e1e", fg="white", font=label_font)
    label.pack()

    listbox_font = font.Font(family="Helvetica", size=13, weight="bold")

    lunar_path = os.path.join(os.path.expanduser("~"), ".lunarclient", "offline", "multiver", "mods")
    mods_path = os.path.join(lunar_path, selected_version)
        
    fabric_versions = [d for d in os.listdir(mods_path) if os.path.isdir(mods_path) and d.endswith('.jar')]
    if len(fabric_versions) == 0:
        nlabel = Label(version_frame, text="No Mods Found", bg="#1e1e1e", fg="white", font=label_font)
        nlabel.pack()
        return
    
    style = ttk.Style()
    style.configure("RoundedListbox.TListbox", borderwidth=0, relief="flat", background="#333333", foreground="white", font=listbox_font)

    max_mod_length = max(len(mod) for mod in fabric_versions)
    listbox_width = max_mod_length * 2 

    version_listbox2 = Listbox(version_frame, selectmode="single", height=len(fabric_versions), width=listbox_width, justify=CENTER, selectbackground="green", bg="#333333", fg="white", font=listbox_font, bd=0, relief="flat")
    for version in fabric_versions:
        version_listbox2.insert("end", version)
    version_listbox2.pack(pady=10)

    button_font = customtkinter.CTkFont(family="Helvetica", size=30, weight="bold")
    unload_button = customtkinter.CTkButton(version_frame, text="Unload Mod", command=lambda: unload_mod(mods_path, selected_version, version_listbox2), font=button_font, fg_color='#333333', hover_color='green')
    unload_button.pack()

    return version_frame, version_listbox2

def unload_mod(mods_paths, selected_version, version_listbox2):
    selected_mod_index = version_listbox2.curselection()

    if not selected_mod_index:
        messagebox.showwarning("Warning", "Please select a mod to unload.")
        return

    selected_mod = version_listbox2.get(selected_mod_index)
    lunar_path = os.path.join(os.path.expanduser("~"), ".lunarclient", "offline", "multiver", "mods")
    mods_path2 = os.path.join(mods_paths, selected_mod)

    print(mods_paths)

    try:
        os.remove(mods_path2)
        message = f"Mod '{selected_mod}' unloaded from '{selected_version}' successfully."
        print(message)
        messagebox.showinfo("Success", message)
        # Refresh the listbox after unloading
        version_listbox2.delete(0, "end")
        fabric_versions = [d for d in os.listdir(mods_paths) if os.path.isdir(mods_paths) and d.endswith('.jar')]
        for version in fabric_versions:
            version_listbox2.insert("end", version)
        visible_items = min(len(fabric_versions), 10)  # Set a maximum of 10 visible items
        version_listbox2.configure(height=visible_items)
    except Exception as e:
        error_message = f"Error unloading mod '{selected_mod}' from '{selected_version}': {str(e)}"
        print(error_message)
        messagebox.showerror("Error", error_message)

if __name__ == "__main__":
    root = Tk()
    root.title("Mod Loader")
    root.geometry("500x400")
    root.resizable(False, False)
    root.configure(bg="#1e1e1e")

    version_frame, version_listbox = setup_version_selection(root)
    setup_mod_import(root, version_frame, version_listbox)

    root.mainloop()
