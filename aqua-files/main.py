import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkm
from tkinter import simpledialog as sd

window = tk.Tk()

tree = ttk.Treeview(window, columns=("Name", "Type"), selectmode="browse")
tree.heading("Name", text="Name")
tree.heading("Type", text="Type")
tree['show'] = 'headings'

def refreshTree():
    directory = os.getcwd()
    tree.delete(*tree.get_children())
    for i in os.listdir(directory):
        if os.path.isdir(i):
            tree.insert(parent="", index="end", values=(i, "Folder"), text="folder")
        else:
            tree.insert(parent="", index="end", values=(i, "File"), text="file")

    tree.insert(parent="", index=0, values="Go\ to\ parent\ directory", text="parentdir")

tree.pack(side=tk.LEFT, padx=5)

def openCallback(event = None):
    selected = tree.item(tree.focus())
    if selected["text"] == "file":
        os.startfile('"' + selected["values"][0] + '"')
    elif selected["text"] == "folder":
        try:
            os.chdir(selected["values"][0])
            refreshTree()
        except PermissionError:
            tkm.showerror(title="Error", message="Access denied.")
            os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
            refreshTree()
    elif selected["text"] == "parentdir":
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        refreshTree()

def deleteCallback():
    selected = tree.item(tree.focus())
    if selected["text"] == "file":
        if tkm.askyesno(title="Confirm", message="Are you sure you want to delete this file?"):
            os.remove(selected["values"][0])
            refreshTree()
    elif selected["text"] == "folder":
        if tkm.askyesno(title="Confirm", message="Are you sure you want to delete this file?"):
            os.rmdir(selected["values"][0])
            refreshTree()

def makeFolderCallback():
    try:
        foldername = sd.askstring(title="AquaFiles", prompt="Folder Name:")
        os.mkdir(foldername)
    except FileExistsError:
        tkm.showerror(title="Error", message="Folder already exists!")
    except OSError:
        tkm.showerror(title="Error", message="Invalid folder name!")
    except TypeError:
        pass
    refreshTree()

def makeFileCallback():
    try:
        filename = sd.askstring(title="AquaFiles", prompt="File Name:")
        os.open(filename, os.O_CREAT)
    except FileExistsError:
        tkm.showerror(title="Error", message="File already exists!")
    except OSError:
        tkm.showerror(title="Error", message="Invalid file name!")
    except TypeError:
        pass
    refreshTree()

def renameFileCallback():
    selected = tree.item(tree.focus())
    try:
        newname = sd.askstring(title="AquaFiles", prompt="New Name (include extension):")
        os.rename(selected["values"][0], newname)
    except FileExistsError:
        tkm.showerror(title="Error", message="File already exists!")
    except PermissionError:
        tkm.showerror(title="Error", message="Access denied.")
    except TypeError:
        pass

button_open = tk.Button(window, text="Open", width=125, command=openCallback)
button_delete = tk.Button(window, text="Delete", width=125, command=deleteCallback)
button_new_folder = tk.Button(window, text="New Folder", width=125, command=makeFolderCallback)
button_new_file = tk.Button(window, text="New File", width=125, command=makeFileCallback)
button_rename = tk.Button(window, text="Rename", width=125, command=renameFileCallback)
button_refresh = tk.Button(window, text="Refresh", width=125, command=refreshTree)

button_open.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
button_delete.pack(side=tk.TOP, anchor="ne", padx=10)
button_new_folder.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
button_new_file.pack(side=tk.TOP, anchor="ne", padx=10)
button_rename.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)
button_refresh.pack(side=tk.TOP, anchor="ne", padx=10)
tree.bind("<Double-Button-1>", openCallback)

refreshTree()
window.title("AquaFiles")
window.geometry("600x250")
window.resizable(False, False)
window.iconbitmap("icon.ico")
window.mainloop()
