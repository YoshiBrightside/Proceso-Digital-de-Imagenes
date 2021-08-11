import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from time import sleep

def openfilename():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(title ='"pen')
    return filename

def update_img():
    # Select the Imagename  from a folder 
    global image_name
    image_name = openfilename()
    # opens the image
    img = Image.open(image_name)
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((500, 300))
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
    # create a label
    panel = tk.Label(root, image = img)
    # set the image as img 
    panel.image = img
    panel.grid(row=1, column=1, sticky="nsew", padx=3, pady=2)

def apply_filter(filter = None):
    # Select the Imagename  from a folder 
    global image_name
    image_name = openfilename()
    # opens the image
    img = Image.open(image_name)
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((500, 300))
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(img)
    # create a label
    panel = tk.Label(root, image = img)
    # set the image as img 
    panel.image = img
    panel.grid(row=1, column=1, sticky="nsew", padx=3, pady=2)

root = tk.Tk()
root.geometry("1200x600")
root.configure(background="#0f0f0f")

# Allow Window to be resizable
root.resizable(width = True, height = True)

image1_frame = tk.Frame(root, background="#1c1c1c", bd=1)
image2_frame = tk.Frame(root, background="#1c1c1c", bd=1)
option_frame = tk.Frame(root, background="#1c1c1c", bd=1)
filter_frame = tk.Frame(root, background="#1c1c1c", bd=1)
before_text_frame = tk.Frame(root, background="#1c1c1c", bd=1)
after_text_frame = tk.Frame(root, background="#1c1c1c", bd=1)

filter_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=2, pady=2)
before_text_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
after_text_frame.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
image1_frame.grid(row=1, column=1, sticky="nsew", padx=3, pady=2)
image2_frame.grid(row=1, column=2, sticky="nsew", padx=3, pady=2)
option_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=3, pady=2)

image1 = ImageTk.PhotoImage(Image.open("img/bunny1.jpeg").resize((500, 300)))
tk.Label(image1_frame, image=image1).pack()

image2 = ImageTk.PhotoImage(Image.open("img/alpaca1.jpeg").resize((500, 300)))
tk.Label(image2_frame, image=image2).pack()

root.grid_rowconfigure(0, weight=10)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=100)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)

# Create a button and place it into the window using grid layout
btn = tk.Button(option_frame, text ='open image', command = update_img).grid(
                                        row = 1, columnspan = 4)

root.mainloop()