from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

BLOCK_SIZE = 16 # AES block size

def pad(data):
  pad_len = BLOCK_SIZE - len(data) % BLOCK_SIZE
  return data + bytes([pad_len]) * pad_len

def unpad(data):
  pad_len = data[-1]
  return data[:-pad_len]

def encrypt_file(filepath, key_name):
  try:
    key = key_name.encode("utf-8").ljust(32, b'\0')[:32] # Pad/truncate to 32 bytes
    with open(filepath, 'rb') as f:
      data = f.read()

    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = iv + cipher.encrypt(pad(data))

    with open(filepath, 'wb') as f:
      f.write(encrypted_data)

    return True
  except Exception as e:
    print(f"[Encryption Error] {e}")
    return False

def decrypt_file(filepath, key_name):
  try:
    key = key_name.encode("utf-8").ljust(32, b'\0')[:32] # Pad/truncate to 32 bytes
    with open(filepath, 'rb') as f:
      encrypted_data = f.read()

    iv = encrypted_data[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(encrypted_data[BLOCK_SIZE:])
    original = unpad(data)

    with open(filepath, 'wb') as f:
      f.write(original)

    return True
  except Exception as e:
    print(f"[Decryption Error] {e}")
    return False