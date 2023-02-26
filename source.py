import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import *
import customtkinter as ck
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from io import BytesIO
import  os


def data2binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]
    return p

def hidedata(img, data):
    data += "$$"
    d_index = 0
    b_data = data2binary(data)
    len_data = len(b_data)

    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            if d_index < len_data:
                pix[0] = int(r[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[1] = int(g[:-1] + b_data[d_index])
                d_index += 1
            if d_index < len_data:
                pix[2] = int(b[:-1] + b_data[d_index])
                d_index += 1
            if d_index >= len_data:
                break
    return img

def encode():
    filename = filedialog.askopenfilename()
    image = cv2.imread(filename)
    img = Image.open(filename, 'r')
    w, h = img.size
    data = entry_encode.get()
    if len(data) == 0:
        raise ValueError("Empty data")
    enc_img = filedialog.asksaveasfilename()
    enc_data = hidedata(image, data)
    cv2.imwrite(enc_img, enc_data)
    show_image(enc_data, title="Encoded Image")
    img1 = Image.open(enc_img, 'r')
    img1 = img1.resize((w, h),Image.ANTIALIAS)
    if w != h:
        img1.save(enc_img, optimize=True, quality=65)
    else:
        img1.save(enc_img)

def find_data(img):
    bin_data = ""
    for value in img:
        for pix in value:
            r, g, b = data2binary(pix)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]

    all_bytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]

    readable_data = ""
    for x in all_bytes:
        readable_data += chr(int(x, 2))
        if readable_data[-2:] == "$$":
            break
    return readable_data[:-2]

def decode():
    filename = filedialog.askopenfilename()
    image = cv2.imread(filename)
    msg = find_data(image)
    if len(msg) == 0:
        messagebox.showerror("Error", "No hidden message found")
    else:
        entry_decode.delete(0, tk.END)
        entry_decode.insert(tk.END, msg)


def show_image(image, title="Image"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#GUI Configuration
ck.set_appearance_mode("#ffffff")
ck.set_default_color_theme("blue")

root = ck.CTk()
root.title('Steganography Project - WE')
root.geometry("750x600")
root.resizable(width =False, height=False)
root.grid_rowconfigure(0, weight = 2)
root.grid_columnconfigure(0, weight = 2)
root.grid()


frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label = ck.CTkLabel(root, text = "Image Steganography Tool", font = ck.CTkFont("Modern", 20), width = 750, height = 30, fg_color = ("#ffffff", "#00c4cc"))
label.pack(pady=(0,0))

label_encode = ck.CTkLabel(root, text="Enter your message to encode",font=ck.CTkFont("Modern", 30), width=250,height=55,fg_color=("#ffffff", "#00c4cc"),corner_radius=8)
label_encode.place(relx=10, rely=100, anchor=tk.CENTER)
label_encode.pack(pady=(40,5))

entry_encode  = tk.Entry(root, width=200, highlightthickness=5)
entry_encode .config(bg='#ffffff', width=25, highlightbackground="#00c4cc", highlightcolor="#00c4cc")
entry_encode .pack(padx=20, pady=5)

button_encode  = ck.CTkButton(root, text = "Encode", command=encode,font = ck.CTkFont('Modern',25), fg_color=("#ffffff", "#00c4cc"),corner_radius=10)
button_encode .pack(pady=5)

label_decode = ck.CTkLabel(root, text="Decoded Message",font=ck.CTkFont("Modern", 30), width=250,height=55,fg_color=("#ffffff", "#00c4cc"),corner_radius=8)
label_decode.place(relx=10, rely=100, anchor=tk.CENTER)
label_decode.pack(pady=(80,5))

entry_decode = tk.Entry(root, width=200, highlightthickness=5)
entry_decode.config(bg='#ffffff', width=25, highlightbackground="#00c4cc", highlightcolor="#00c4cc")
entry_decode.pack(padx=20, pady=5)

button_decode = ck.CTkButton(root, text = "Click to Decode", command=decode,font = ck.CTkFont('Modern',20), fg_color=("#ffffff", "#00c4cc"),corner_radius=10)
button_decode.pack(pady=5)

root.mainloop()
