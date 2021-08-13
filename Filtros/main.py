from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

def openPath():
    # open file dialog box to select image
    # The dialogue box has a title "Open"
    filename = filedialog.askopenfilename(
        initialdir="~/",
        filetypes=(
            ('Archivos JPG', '*.jpg'),
            ('Archivos PNG', '*.png'),
            ('Archivos JPEG', '*.jpeg')
        ),
        title='Selecciona una imagen'
    )
    return filename

def update_img(image_container, canvas, x = 500, y = 300):
    # PhotoImage class is used to add image to widgets, icons etc
    img = ImageTk.PhotoImage(file=openPath())
    canvas.imageList.append(img)
    canvas.itemconfig(image_container, image=img)


def apply_filter(filter = None):
    # Select the Imagename  from a folder 
    global image_name
    image_name = filedialog.openfilename()
    # opens the image
    img = Image.open(image_name)
    # resize the image and apply a high-quality down sampling filter
    img = img.resize((500, 300))
    # PhotoImage class is used to add image to widgets, icons etc
    img = PhotoImage(img)
    # create a label
    panel = Label(root, image = img)
    # set the image as img 
    panel.image = img
    panel.grid(row=1, column=1, sticky="nsew", padx=3, pady=2)

def start_main_window():
    root = Tk()
    root.geometry('1200x600')
    root.title('Universal Image Filter Applier')
    root.configure(background="#0f0f0f")
    # Allow Window to be resizable
    root.resizable(width = True, height = True)
    image1_frame = Frame(root, background="#1c1c1c", bd=1)
    image2_frame = Frame(root, background="#1c1c1c", bd=1)
    option_frame = Frame(root, background="#1c1c1c", bd=1)
    filter_frame = Frame(root, background="#1c1c1c", bd=1)
    before_text_frame = Frame(root, background="#1c1c1c", bd=1)
    after_text_frame = Frame(root, background="#1c1c1c", bd=1)
    filter_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=2, pady=2)
    before_text_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
    after_text_frame.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
    image1_frame.grid(row=1, column=1, sticky="nsew", padx=3, pady=2)
    image2_frame.grid(row=1, column=2, sticky="nsew", padx=3, pady=2)
    option_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=3, pady=2)
    canvas = Canvas(image1_frame, width= 500, height= 300)
    canvas.imageList = []
    canvas.pack(expand = NO)
    canvas2 = Canvas(image2_frame, width= 500, height= 300)
    canvas2.imageList = []
    canvas2.pack(expand = NO)
    image1 = ImageTk.PhotoImage(file='img/bunny1.jpeg')
    image2 = ImageTk.PhotoImage(file='img/alpaca1.jpeg')
    root.grid_rowconfigure(0, weight=10)
    root.grid_rowconfigure(1, weight=0)
    root.grid_rowconfigure(2, weight=100)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=0)
    root.grid_columnconfigure(2, weight=0)
    # Create a button and place it into the window using grid layout
    btn = Button(option_frame, width = '50',
                    text ='open image',
                    command = lambda:update_img(left_img, canvas))
    btn.pack()
    left_img = canvas.create_image(0, 0, anchor=NW, image=image1)
    right_img = canvas2.create_image(0, 0, anchor=NW, image=image2)
    canvas.imageList.append(image1)
    root.mainloop()

def main():
    start_main_window()

if __name__ == '__main__':
    main()