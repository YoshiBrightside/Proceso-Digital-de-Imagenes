from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import filters as fl

class UniversalImageFilterApplier:
    def __init__(self):
        '''
        Bunch of init code, basically it creates and sets up our environment.
        
        The Universal Image Filter Applier contains:
        - Window for storing everything.
        - Four frames for the two images, the filters and the options.
        - Two canvas for storing images.
        - Two images.
        - Two image changers, this way we don't need to create more canvas
          (see update_image methods).
        - Some buttons.
        - An uncreative name.
        '''
        # Sets the window itself
        self.window = Tk()
        self.window.geometry('1200x600')
        self.window.title('Universal Image Filter Applier')
        self.window.configure(background="#0f0f0f")
        self.window.resizable(width = True, height = True)
        # Sets the frames
        self.option_frame = Frame(self.window, background="#1c1c1c", bd=1)
        self.filter_frame = Frame(self.window, background="#1c1c1c", bd=1)
        self.left_image_frame = Frame(self.window, background="#1c1c1c", bd=1)
        self.right_image_frame = Frame(self.window, background="#1c1c1c", bd=1)
        # Sets the place in grid for frames
        self.left_image_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=2)
        self.right_image_frame.grid(row=0, column=2, sticky="nsew", padx=3, pady=2)
        self.filter_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=2, pady=2)
        self.option_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=3, pady=2)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=0)
        self.window.grid_rowconfigure(2, weight=0)
        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        # Sets the left_canvas for left and right images
        self.left_canvas = Canvas(self.left_image_frame, width=self.left_image_frame.winfo_screenwidth())
        self.left_canvas.pack(fill="both", expand = True)
        self.right_canvas = Canvas(self.right_image_frame, width=self.right_image_frame.winfo_screenwidth())
        self.right_canvas.pack(fill="both", expand = True)
        self.left_image = Image.open('img/bunny1.jpeg')
        self.right_image = Image.open('img/alpaca1.jpeg')
        # Create a button and place it into the window
        self.apply_filter_btn = Button(self.option_frame, width = '50', height='5',
                        text ='Apply filter',
                        command = self.update_right_image)
        self.apply_filter_btn.pack()
        self.open_image_btn = Button(self.filter_frame, width = '30',
                        text ='Open image',
                        command = self.open_image)
        self.open_image_btn.pack()
        # We add the filters, yay
        self.load_filters()
        self.filter_btns
        
                
        # Tkinter has a trash managemnt bug, we store the images to provent it
        self.anti_trash_system = [ImageTk.PhotoImage(self.left_image.resize((self.left_canvas.winfo_width(),400), Image.ANTIALIAS)),
                                  ImageTk.PhotoImage(self.right_image.resize((self.right_canvas.winfo_width(),400), Image.ANTIALIAS))]
        self.left_image_changer = self.left_canvas.create_image(0, 0, anchor=NW, image=self.anti_trash_system[0])
        self.right_image_changer = self.right_canvas.create_image(0, 0, anchor=NW, image=self.anti_trash_system[1])
        self.window.mainloop()

    def load_filters(self):
        self.filters = fl.get_filters()
        self.filter_btns = [None for _ in range(len(self.filters))]
        for f in range(len(self.filters)):
            self.filter_btns[f] = Button(self.filter_frame, width = '30', height='5',
                        text =self.filters[f].name,
                        command = lambda f=f: fl.apply_filter(self.filters[f].name, self.left_image, self.filters[f].options)) # https://stackoverflow.com/a/10865170
            self.filter_btns[f].pack()

    def update_left_image(self, image):
        '''
        Updates and resizes the new image
        '''
        self.left_image = image
        self.anti_trash_system[0] = ImageTk.PhotoImage(image.resize((self.left_canvas.winfo_width(),self.left_canvas.winfo_height()), Image.ANTIALIAS))
        self.left_canvas.itemconfigure(self.left_image_changer, image = self.anti_trash_system[0])

    def update_right_image(self, filter=None):
        modded_image = self.left_image
        if filter:
            print('Filter')
        self.right_image = modded_image
        self.anti_trash_system[1] = ImageTk.PhotoImage(modded_image.resize((self.right_canvas.winfo_width(),self.left_canvas.winfo_height()), Image.ANTIALIAS))
        self.right_canvas.itemconfigure(self.right_image_changer, image = self.anti_trash_system[1])

    def open_image(self):
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
        img = Image.open(filename)
        self.update_left_image(img)

def main():
    UIFA = UniversalImageFilterApplier()

if __name__ == '__main__':
    main()