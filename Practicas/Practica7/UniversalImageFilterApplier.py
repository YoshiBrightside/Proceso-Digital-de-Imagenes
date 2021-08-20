from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import filters as fl 
import copy

class UniversalImageFilterApplier:
    def __init__(self):
        '''
        Bunch of init code, basically it creates and sets up our environment.
        
        The Universal Image Filter Applier contains:
        - Window for storing everything.
        - Five frames for the two images, the filters and the options.
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
        self.menu_frame = Frame(self.window, background="#1c1c1c", bd=1)
        # Sets the place in grid for frames
        self.left_image_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=2)
        self.right_image_frame.grid(row=0, column=2, sticky="nsew", padx=3, pady=2)
        self.filter_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=2, pady=2)
        self.option_frame.grid(row=2, column=1, sticky="nsew", padx=3, pady=2)
        self.menu_frame.grid(row=2, column=2, sticky="nsew", padx=3, pady=2)
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
        # Create buttons
        self.apply_filter_btn = Button(self.option_frame,
                                       width = '50', height = '2',
                                       text = 'Apply filter',
                                       command = self.update_right_image)
        self.apply_filter_btn.pack()
        self.reset_image_btn = Button(self.menu_frame, width = '50',
                                  height = '2', text ='Reset Image',
                                  command = self.reset_image)
        self.reset_image_btn.pack()
        self.open_image_btn = Button(self.menu_frame, width = '50',
                                     height = '2', text ='Open image',
                                     command = self.open_image)
        self.open_image_btn.pack()
        self.save_btn = Button(self.menu_frame, width = '50', height='2',
                                     text ='Save Image As',
                                     command = self.save_as)
        self.save_btn.pack()
        self.save_btn.pack()
        # We load the filters, yay
        self.load_filters()
        self.selected_filter = None
        self.filter_options = {}
        self.selected_options = {}
        # Tkinter has a trash managemnt bug, we store the images to prevent it
        self.anti_trash_system = [ImageTk.PhotoImage(self.left_image.resize((self.left_canvas.winfo_width(),400), Image.ANTIALIAS)),
                                  ImageTk.PhotoImage(self.right_image.resize((self.right_canvas.winfo_width(),400), Image.ANTIALIAS))]
        self.left_image_changer = self.left_canvas.create_image(0, 0, anchor=NW, image=self.anti_trash_system[0])
        self.right_image_changer = self.right_canvas.create_image(0, 0, anchor=NW, image=self.anti_trash_system[1])
        self.window.mainloop()

    def set_selected_filter(self, new_filter):
        self.clear_filter_options()
        self.selected_filter = new_filter
        self.display_filter_options()

    def clear_filter_options(self):
        for v in self.filter_options.values():
            if v: # No estoy seguro de que sea necesario aun el if
                v.destroy()
        self.selected_options.clear()
        self.filter_options.clear()

    def get_filter_option_inputs(self):
        '''
        Obtiene los valores que se le han dado a las opciones del filtro
        seleccionado y las desenvuelve de StringVar. Usado en vez de bind.
        '''
        for k, v in (self.filter_options.items()):
            if str(v.__class__())[2:10] == 'combobox':
                self.selected_options[k] = v.get()
            if str(v.__class__())[2:6] == 'text':
                self.selected_options[k] = self.filter_options[k].get("1.0",END)[:-1]
            
        

    def display_filter_options(self):
        for o in (self.selected_filter.options.keys()):
            self.selected_options[o] = StringVar()
            if self.selected_filter.options[o]['style'] == 'dropdown':
                self.filter_options[o] = ttk.Combobox(self.option_frame)
                self.filter_options[o]['values'] = self.selected_filter.options[o]['values']
            if self.selected_filter.options[o]['style'] == 'text_box':
                self.filter_options[o] = Text(self.option_frame, height='2', width='20')
                self.filter_options[o].insert('end', o)
            if self.selected_filter.options[o]['style'] == 'spinbox':
                self.filter_options[o] = Spinbox(self.option_frame, from_=0, to=255)    
            self.filter_options[o].pack()

    def load_filters(self):
        self.filters = fl.get_filters()
        self.filter_btns = [None for _ in range(len(self.filters))]
        for f in range(len(self.filters)):
            self.filter_btns[f] = Button(self.filter_frame, width = '30', height='2',
                        text =self.filters[f].name,
                        command = lambda f=f: self.set_selected_filter(self.filters[f])) # Reason for f=f https://stackoverflow.com/a/10865170
            self.filter_btns[f].pack()

    def update_left_image(self, image):
        '''
        Updates and resizes the new image
        '''
        self.left_image = image
        self.anti_trash_system[0] = ImageTk.PhotoImage(image.resize((self.left_canvas.winfo_width(),self.left_canvas.winfo_height()), Image.ANTIALIAS))
        self.left_canvas.itemconfigure(self.left_image_changer, image = self.anti_trash_system[0])
        self.left_image.save('.temp.jpeg', quality=100)

    def reset_image(self):
        self.open_image(self.left_image.filename)

    def update_right_image(self, reset = False):
        self.get_filter_option_inputs()
        if self.selected_filter != None and not reset:
            modded_image = self.selected_filter.apply_filter(self.selected_filter.name, self.right_image, self.selected_options)
        try:
            self.right_image = Image.open('.temp.jpeg')
        except Exception:
            self.right_image = modded_image
        self.anti_trash_system[1] = ImageTk.PhotoImage(self.right_image.resize((self.right_canvas.winfo_width(),self.left_canvas.winfo_height()), Image.ANTIALIAS))
        self.right_canvas.itemconfigure(self.right_image_changer, image = self.anti_trash_system[1])

    def open_image(self, filename=None):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        if not filename:
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
        self.update_right_image(reset=True)

    
    def save_as(self):
        name = filedialog.asksaveasfile(
            mode='w',
            defaultextension=".jpeg"
        )
        self.right_image.save(name, quality=100)

def main():
    UIFA = UniversalImageFilterApplier()

if __name__ == '__main__':
    main()