import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    img_label.config(text="Selected: " + file_path.split("/")[-1])
    img_label.image_path = file_path

def encrypt_image():
    if not hasattr(img_label, 'image_path'):
        messagebox.showerror("Error", "Please select an image first!")
        return

    message = msg_entry.get()
    password = pass_entry.get()
    
    if not message or not password:
        messagebox.showerror("Error", "Message and password cannot be empty!")
        return

    img = cv2.imread(img_label.image_path)
    msg_bytes = [ord(char) for char in message] + [0]  
    
    height, width, channels = img.shape
    max_capacity = height * width * 3  

    if len(msg_bytes) > max_capacity:
        messagebox.showerror("Error", "Message is too long for this image!")
        return

    idx = 0
    for row in range(height):
        for col in range(width):
            for ch in range(3):  
                if idx < len(msg_bytes):
                    img[row, col, ch] = msg_bytes[idx]
                    idx += 1
                else:
                    break
            if idx >= len(msg_bytes):
                break
        if idx >= len(msg_bytes):
            break

    encrypted_image_path = img_label.image_path.split('.')[0] + "_encrypted.png"
    cv2.imwrite(encrypted_image_path, img)
    messagebox.showinfo("Success", f"Message encrypted! Saved as {encrypted_image_path}")

def decrypt_image():
    if not hasattr(img_label, 'image_path'):
        messagebox.showerror("Error", "Please select an encrypted image first!")
        return
    password = pass_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter the password!")
        return

    img = cv2.imread(img_label.image_path)
    
    decrypted_msg = []
    height, width, channels = img.shape

    for row in range(height):
        for col in range(width):
            for ch in range(3):
                val = img[row, col, ch]
                if val == 0:  
                    messagebox.showinfo("Decryption Complete", f"Decrypted Message:\n{''.join(decrypted_msg)}")
                    return
                decrypted_msg.append(chr(val))

    messagebox.showinfo("Decryption Complete", f"Decrypted Message:\n{''.join(decrypted_msg)}")
root = tk.Tk()
root.title("Image Steganography")
root.geometry("500x400")
root.resizable(False, False)
btn_select = tk.Button(root, text="Select Image", command=select_image, font=("Arial", 12))
btn_select.pack(pady=10)

img_label = tk.Label(root, text="No Image Selected", font=("Arial", 10))
img_label.pack()

tk.Label(root, text="Secret Message:", font=("Arial", 12)).pack()
msg_entry = tk.Entry(root, width=40)
msg_entry.pack(pady=5)
tk.Label(root, text="Passcode:", font=("Arial", 12)).pack()
pass_entry = tk.Entry(root, width=40, show="*")
pass_entry.pack(pady=5)
btn_encrypt = tk.Button(root, text="Encrypt Message", command=encrypt_image, font=("Arial", 12), bg="lightblue")
btn_encrypt.pack(pady=10)
btn_decrypt = tk.Button(root, text="Decrypt Message", command=decrypt_image, font=("Arial", 12), bg="lightgreen")
btn_decrypt.pack(pady=10)

root.mainloop()
