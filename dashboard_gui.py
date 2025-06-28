import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from aes_enc_desc import encrypt_file, decrypt_file
import os
import json
import subprocess

class DashboardGUI(tk.Frame):
  def __init__(self, parent, encryptor, username, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    self.encryptor = encryptor
    self.username = username

    self.tracked_items = []
    self.selected_item = None
    self.trackfile_path = "trackdata.dat"

    self.create_widgets()
    self.load_tracked_items()

  def create_widgets(self):
    title = tk.Label(self, text="SafeCrypt Dashboard", font=("Helvetica", 16, "bold"))
    title.pack(pady=10)

    columns = ("Name", "Location", "Status", "Visibility", "Key Used")
    self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
    for col in columns:
      self.tree.heading(col, text=col)
      self.tree.column(col, anchor="w", width=150)
    self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    btn_frame = tk.Frame(self)
    btn_frame.pack(pady=5)

    self.btn_add = tk.Button(btn_frame, text="Add File/Folder", width=15, command=self.add_item)
    self.btn_remove = tk.Button(btn_frame, text="Remove Selected", width=15, command=self.remove_item, state=tk.DISABLED)
    self.btn_open_details = tk.Button(btn_frame, text="Open Details", width=15, command=self.open_details_panel, state=tk.DISABLED)

    self.btn_add.grid(row=0, column=0, padx=5)
    self.btn_remove.grid(row=0, column=1, padx=5)
    self.btn_open_details.grid(row=0, column=2, padx=5)

    self.details_panel = None

  def on_tree_select(self, event):
    selected = self.tree.selection()
    if selected:
      self.selected_item = selected[0]
      self.btn_remove.config(state=tk.NORMAL)
      self.btn_open_details.config(state=tk.NORMAL)
    else:
      self.selected_item = None
      self.btn_remove.config(state=tk.DISABLED)
      self.btn_open_details.config(state=tk.DISABLED)

  def add_item(self):
    choice = messagebox.askquestion("Add", "Add a file? (No = add folder)")

    if choice == 'yes':
      path = filedialog.askopenfilename()
    else:
      path = filedialog.askdirectory()

    if not path:
      return

    name = os.path.basename(path)
    location = path
    status = "Decrypted"
    visibility = "Visible"
    key_used = "-"

    item_data = {
      "name": name,
      "location": location,
      "status": status,
      "visibility": visibility,
      "key_used": key_used,
      "path": path,
      "is_folder": choice != 'yes',
      "encrypted": False,
      "hidden": False,
      "key": None,
      "editable": True,
    }
    self.tracked_items.append(item_data)
    self.tree.insert("", "end", values=(name, location, status, visibility, key_used))
    self.save_tracked_items()

  def remove_item(self):
    if not self.selected_item:
      return
    index = self.tree.index(self.selected_item)
    self.tree.delete(self.selected_item)
    del self.tracked_items[index]
    self.selected_item = None
    self.btn_remove.config(state=tk.DISABLED)
    self.btn_open_details.config(state=tk.DISABLED)
    if self.details_panel:
      self.details_panel.destroy()
      self.details_panel = None
    self.save_tracked_items()

  def open_details_panel(self):
    if not self.selected_item:
      return
    if self.details_panel:
      self.details_panel.destroy()

    index = self.tree.index(self.selected_item)
    item = self.tracked_items[index]

    self.details_panel = tk.Frame(self, relief=tk.RIDGE, borderwidth=2)
    self.details_panel.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(self.details_panel, text=f"Name: {item['name']}", font=("Helvetica", 12, "bold")).pack(anchor="w")
    tk.Label(self.details_panel, text=f"Location: {item['location']}", wraplength=600).pack(anchor="w")
    tk.Label(self.details_panel, text=f"Type: {'Folder' if item['is_folder'] else 'File'}").pack(anchor="w")
    tk.Label(self.details_panel, text=f"Status: {'Encrypted' if item['encrypted'] else 'Decrypted'}").pack(anchor="w")
    tk.Label(self.details_panel, text=f"Visibility: {'Hidden' if item['hidden'] else 'Visible'}").pack(anchor="w")
    tk.Label(self.details_panel, text=f"Key Used: {item['key'] if item['key'] else '-'}").pack(anchor="w")

    action_frame = tk.Frame(self.details_panel)
    action_frame.pack(pady=10)

    btn_encrypt = tk.Button(
      action_frame, text="Encrypt", width=12,
      command=lambda: self.encrypt_item(index),
      state=tk.DISABLED if item['encrypted'] else tk.NORMAL
    )
    btn_decrypt = tk.Button(
      action_frame, text="Decrypt", width=12,
      command=lambda: self.decrypt_item(index),
      state=tk.DISABLED if not item['encrypted'] else tk.NORMAL
    )
    btn_toggle_vis = tk.Button(action_frame, text="Hide" if not item['hidden'] else "Unhide", width=12, command=lambda: self.toggle_visibility(index))
    btn_toggle_edit = tk.Button(
      action_frame,
      text="Lock Editing" if item['editable'] else "Unlock Editing",
      width=15,
      command=lambda: self.toggle_editability(index)
    )

    btn_encrypt.grid(row=0, column=0, padx=5)
    btn_decrypt.grid(row=0, column=1, padx=5)
    btn_toggle_vis.grid(row=0, column=2, padx=5)
    btn_toggle_edit.grid(row=0, column=3, padx=5)

  def encrypt_item(self, index):
    item = self.tracked_items[index]
    key = self.ask_key()
    if not key:
      return

    success = encrypt_file(item['path'], key)
    if success:
      item['encrypted'] = True
      item['key'] = key
      self.update_treeview_item(index)
      self.save_tracked_items()
      self.open_details_panel()
      messagebox.showinfo("Encrypted", f"Encrypted {item['name']} with key '{key}'.")
      self.open_details_panel()
    else:
      messagebox.showerror("Error", f"Failed to encrypt {item['name']}.")

  def decrypt_item(self, index):
    item = self.tracked_items[index]
    key = item['key']
    if not key:
      messagebox.showerror("Error", "No key stored for decryption.")
      return

    success = decrypt_file(item['path'], key)
    if success:
      item['encrypted'] = False
      item['key'] = None
      self.update_treeview_item(index)
      self.save_tracked_items()
      self.open_details_panel()
      messagebox.showinfo("Decrypted", f"Decrypted {item['name']}.")
      self.open_details_panel()
    else:
      messagebox.showerror("Error", f"Failed to decrypt {item['name']}.")

  def toggle_visibility(self, index):
    item = self.tracked_items[index]
    new_state = not item['hidden']
    self.set_visibility(item['path'], hide=new_state)
    item['hidden'] = new_state
    self.update_treeview_item(index)
    self.save_tracked_items()
    self.open_details_panel()

  def ask_key(self):
    key = simpledialog.askstring("Key Selection", "Enter encryption key name:")
    return key

  def update_treeview_item(self, index):
    item = self.tracked_items[index]
    values = (
      item['name'],
      item['location'],
      "Encrypted" if item['encrypted'] else "Decrypted",
      "Hidden" if item['hidden'] else "Visible",
      item['key'] if item['key'] else "-"
    )
    tree_id = self.tree.get_children()[index]
    self.tree.item(tree_id, values=values)

  def save_tracked_items(self):
    try:
      if os.path.exists(self.trackfile_path):
        with open(self.trackfile_path, "r") as f:
          all_data = json.load(f)
      else:
        all_data = {}

      all_data[self.username] = self.tracked_items

      with open(self.trackfile_path, "w") as f:
        json.dump(all_data, f, indent=2)
    except Exception as e:
      messagebox.showerror("Error", f"Failed to save tracked items: {str(e)}")

  def load_tracked_items(self):
    if not os.path.exists(self.trackfile_path):
      return
    try:
      with open(self.trackfile_path, "r") as f:
        all_data = json.load(f)
      self.tracked_items = all_data.get(self.username, [])
      for item in self.tracked_items:
        values = (
          item['name'],
          item['location'],
          "Encrypted" if item['encrypted'] else "Decrypted",
          "Hidden" if item['hidden'] else "Visible",
          item['key'] if item['key'] else "-"
        )
        self.tree.insert("", "end", values=values)
    except Exception as e:
      messagebox.showerror("Error", f"Failed to load tracked items: {str(e)}")
  
  def set_visibility(self, path, hide=True):
    script_path = os.path.abspath("visibility_utils.ps1")
    action = "hide" if hide else "unhide"
    try:
      result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path, "-Path", path, "-Action", action],
          capture_output=True,
          text=True
        )
      if result.returncode != 0:
        messagebox.showerror("Error", f"Visibility toggle failed:\n{result.stdout}")
    except Exception as e:
      messagebox.showerror("Error", f"Exception occurred:\n{str(e)}")
  
  def toggle_editability(self, index):
    item = self.tracked_items[index]
    path = item['path']
    item['editable'] = not item.get('editable', True)

    try:
      action = "lock" if not item['editable'] else "unlock"
      subprocess.run([
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", "file_lock.ps1",
        path,
        action
      ], check=True)
    except Exception as e:
      messagebox.showerror("Error", f"Failed to toggle editability: {e}")
      item['editable'] = not item['editable']  # Revert on failure

    self.save_tracked_items()
    self.open_details_panel()