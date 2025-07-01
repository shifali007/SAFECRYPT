# 🔐 SafeCrypt

**Secure File Encryption and Management Tool (Desktop GUI Application)**

SafeCrypt is a Windows-based Python desktop application designed to protect your sensitive files and folders. It offers AES encryption/decryption, visibility toggling (hide/unhide), edit locking, and user-based access control — all wrapped in a simple and intuitive interface.

---

## 🚀 Features

- 🔑 **AES-256 Encryption & Decryption**  
  Secure your files using the AES algorithm in CBC mode with custom key support.

- 👤 **User Registration and Login System**  
  Each user has isolated access and tracking of encrypted/decrypted files.

- 📁 **Track and Manage Files/Folders**  
  Add, remove, and monitor the status of files or folders from your personal dashboard.

- 🕶️ **Hide / Unhide Files and Folders**  
  Easily change file/folder visibility using PowerShell scripts.

- 🔒 **Lock / Unlock Editing Access**  
  Prevent modifications to files by changing permissions through PowerShell automation.

- 🧠 **User-Friendly GUI**  
  Built with `tkinter` for a clean and simple user experience.

---

## 🛠️ Technologies Used

- **Python 3.10+**
- **tkinter** (GUI)
- **pycryptodome** (AES encryption)
- **pywin32 & PowerShell** (file visibility and permission control)
- **pickle** (user data storage)

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/safecrypt.git
   cd safecrypt
