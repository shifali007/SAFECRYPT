import tkinter as tk
from tkinter import messagebox

class LoginRegisterGUI:
  def __init__(self, master, on_login, on_register):
    """
    master: root or parent widget
    on_login: callback function called with (username, password) on successful login submit
    on_register: callback function called with (username, password, confirm_password) on registration submit
    """
    self.master = master
    self.on_login = on_login
    self.on_register = on_register

    self.master.title("SafeCrypt Login")
    self.master.geometry("400x350")
    self.master.resizable(False, False)

    self.container = tk.Frame(self.master, bg="#f0f0f0")
    self.container.pack(fill="both", expand=True, padx=20, pady=20)

    self.show_main_menu()

  def clear_container(self):
    for widget in self.container.winfo_children():
      widget.destroy()

  def show_main_menu(self):
    self.clear_container()
    tk.Label(self.container, text="Welcome to SafeCrypt", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=(10, 30))

    btn_login = tk.Button(self.container, text="Login", font=("Helvetica", 14), width=20, command=self.show_login_form, bg="#4CAF50", fg="white", activebackground="#45a049")
    btn_login.pack(pady=10)

    btn_register = tk.Button(self.container, text="Register", font=("Helvetica", 14), width=20, command=self.show_register_form, bg="#2196F3", fg="white", activebackground="#1976D2")
    btn_register.pack(pady=10)

  def show_login_form(self):
    self.clear_container()

    tk.Label(self.container, text="Login", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=(10, 20))

    tk.Label(self.container, text="Username:", bg="#f0f0f0").pack(anchor="w")
    self.login_username = tk.Entry(self.container, width=30)
    self.login_username.pack(pady=(0,10))

    tk.Label(self.container, text="Password:", bg="#f0f0f0").pack(anchor="w")
    self.login_password = tk.Entry(self.container, show="*", width=30)
    self.login_password.pack(pady=(0,20))

    btn_submit = tk.Button(self.container, text="Login", width=20, bg="#4CAF50", fg="white", activebackground="#45a049",
                command=self.handle_login)
    btn_submit.pack(pady=(0, 10))

    btn_back = tk.Button(self.container, text="Back", width=20, command=self.show_main_menu)
    btn_back.pack()

  def show_register_form(self):
    self.clear_container()

    tk.Label(self.container, text="Register", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=(10, 20))

    tk.Label(self.container, text="Username:", bg="#f0f0f0").pack(anchor="w")
    self.reg_username = tk.Entry(self.container, width=30)
    self.reg_username.pack(pady=(0,10))

    tk.Label(self.container, text="Password:", bg="#f0f0f0").pack(anchor="w")
    self.reg_password = tk.Entry(self.container, show="*", width=30)
    self.reg_password.pack(pady=(0,10))

    tk.Label(self.container, text="Confirm Password:", bg="#f0f0f0").pack(anchor="w")
    self.reg_confirm = tk.Entry(self.container, show="*", width=30)
    self.reg_confirm.pack(pady=(0,20))

    btn_submit = tk.Button(self.container, text="Register", width=20, bg="#2196F3", fg="white", activebackground="#1976D2",
                command=self.handle_register)
    btn_submit.pack(pady=(0, 10))

    btn_back = tk.Button(self.container, text="Back", width=20, command=self.show_main_menu)
    btn_back.pack()

  def handle_login(self):
    username = self.login_username.get().strip()
    password = self.login_password.get().strip()
    if not username or not password:
      messagebox.showerror("Error", "Please fill in all fields.")
      return
    # Call the provided callback
    success, msg = self.on_login(username, password)
    if success:
      messagebox.showinfo("Login Success", msg)
    else:
      messagebox.showerror("Login Failed", msg)


  def handle_register(self):
    username = self.reg_username.get().strip()
    password = self.reg_password.get().strip()
    confirm = self.reg_confirm.get().strip()
    if not username or not password or not confirm:
      messagebox.showerror("Error", "Please fill in all fields.")
      return
    if password != confirm:
      messagebox.showerror("Error", "Passwords do not match.")
      return
    # Call the provided callback
    success, msg = self.on_register(username, password, confirm)
    if success:
      messagebox.showinfo("Registration Success", msg)
    else:
      messagebox.showerror("Registration Failed", msg)

