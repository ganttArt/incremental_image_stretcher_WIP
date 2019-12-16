import random
import time
import logging
from tkinter import ttk, filedialog, messagebox, StringVar, PhotoImage, Tk
from PIL import Image, ImageTk
from stretching_functions import create_np_array, create_index_list, build_new_image

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

class Gui:
    def __init__(self, master):

        self.image_frame = ttk.Frame(master)
        self.image_frame.pack(side='left', anchor='nw', padx=8, pady=8)

        self.art = PhotoImage(file='intro_image.gif')
        self.art_label = ttk.Label(self.image_frame, image=self.art)
        self.art_label.grid(row=0, column=0)

        self.horizontal_slider = ttk.Scale(self.image_frame, orient='horizontal',
                                           from_=1, to=int(self.art.width()),
                                           length=int(self.art.width()))
        self.horizontal_slider.grid(row=1, column=0)

        self.vertical_slider = ttk.Scale(self.image_frame, orient='vertical',
                                         from_=1, to=int(self.art.height()),
                                         length=int(self.art.height()))
        self.vertical_slider.grid(row=0, column=1)

        self.widget_frame = ttk.Frame(master)
        self.widget_frame.pack(anchor='nw', padx=8, pady=8)

        self.open_button = ttk.Button(self.widget_frame, text="Open", command=self.open_image)
        self.open_button.grid(row=0, column=1)

        self.save_button = ttk.Button(self.widget_frame, text="Save", command=self.save_image)
        self.save_button.grid(row=0, column=2, pady=4)

        ttk.Label(self.widget_frame, text='      Intensity').grid(row=1, column=1)
        self.intensity_value = StringVar()
        self.intensity_value.set("13")
        self.intensity_spinbox = ttk.Spinbox(self.widget_frame, from_=1, to=13, width=5,
                                             textvariable=self.intensity_value)
        self.intensity_spinbox.grid(row=1, column=2, pady=0)


        self.orientation = StringVar()
        self.up_rb = ttk.Radiobutton(self.widget_frame, variable=self.orientation,
                                     value="up", text='Up    ', command=self.upward_stretch)
        self.up_rb.grid(row=2, column=1, sticky='e')
        
        self.down_rb = ttk.Radiobutton(self.widget_frame, variable=self.orientation,
                                       value="down", text='Down', command=self.downward_stretch)
        self.down_rb.grid(row=3, column=1, sticky='e')
        
        self.left_rb = ttk.Radiobutton(self.widget_frame, variable=self.orientation,
                                       value="left", text='Left', command=self.left_stretch)
        self.left_rb.grid(row=2, column=2, sticky='w')
        
        self.right_rb = ttk.Radiobutton(self.widget_frame, variable=self.orientation,
                                        value="right", text='Right', command=self.right_stretch)
        self.right_rb.grid(row=3, column=2, sticky='w')
        self.orientation.set('down')


        self.random_button = ttk.Button(self.widget_frame, text='Random',
                                        command=self.random_stretch)
        self.random_button.grid(row=4, column=1, columnspan=2)


        self.animate_button = ttk.Button(self.widget_frame, text="Animate",
                                         command=self.left_stretch
                                         )
        self.animate_button.grid(row=5, column=1, columnspan=2)


        self.unprocessed_jpg = None
        self.processed_image = None

    def display_image(self):
        self.art = ImageTk.PhotoImage(self.processed_image)
        self.art_label = ttk.Label(self.image_frame, image=self.art)
        self.art_label.grid(row=0, column=0)

    def downward_stretch(self):
        img_array = create_np_array(self.unprocessed_jpg)
        index_list = create_index_list(img_array, int(self.intensity_value.get()))
        self.processed_image = build_new_image(index_list, img_array, self.vertical_slider.get())
        self.display_image()

    def upward_stretch(self):
        self.unprocessed_jpg = self.unprocessed_jpg.rotate(180)
        img_array = create_np_array(self.unprocessed_jpg)
        index_list = create_index_list(img_array, int(self.intensity_value.get()))
        starting_pixel = self.vertical_index_list[int(self.vertical_slider.get())* -1]
        self.processed_image = build_new_image(index_list, img_array, starting_pixel)
        self.processed_image = self.processed_image.rotate(180)
        self.display_image()
        self.unprocessed_jpg = self.unprocessed_jpg.rotate(180)

    def right_stretch(self):
        self.unprocessed_jpg = self.unprocessed_jpg.rotate(270, expand=True)
        img_array = create_np_array(self.unprocessed_jpg)
        index_list = create_index_list(img_array, int(self.intensity_value.get()))
        self.processed_image = build_new_image(index_list, img_array, self.horizontal_slider.get())
        self.processed_image = self.processed_image.rotate(90, expand=True)
        self.display_image()
        self.unprocessed_jpg = self.unprocessed_jpg.rotate(90, expand=True)

    def left_stretch(self):
        self.unprocessed_jpg = self.unprocessed_jpg.rotate(90, expand=True)
        # self.unprocessed_jpg.show()
        img_array = create_np_array(self.unprocessed_jpg)
        index_list = create_index_list(img_array, int(self.intensity_value.get()))
        starting_pixel = self.horizontal_index_list[int(self.horizontal_slider.get()) * -1]
        self.processed_image = build_new_image(index_list, img_array, starting_pixel)
        self.processed_image = self.processed_image.rotate(270, expand=True)
        self.display_image()
        self.unprocessed_jpg = self.unprocessed_jpg.rotate(270, expand=True)        

    def open_image(self):
        filename = filedialog.askopenfilename()

        try: #checking for non-jpg files
            jpg_image = Image.open(filename)
            if jpg_image.format != 'JPEG':
                jpg_image = jpg_image.convert('RGB')
        except Exception as ex:
            print(ex)
            messagebox.showerror("Error", "Image files only please!")

        self.unprocessed_jpg = jpg_image

        self.vertical_slider = ttk.Scale(self.image_frame, orient='vertical',
                                               from_=1, to=self.unprocessed_jpg.size[1],
                                               length=self.unprocessed_jpg.size[1])
        self.vertical_slider.grid(row=0, column=1)
        self.vertical_slider.set(100)

        self.horizontal_slider = ttk.Scale(self.image_frame, orient='horizontal',
                                           from_=1, to=self.unprocessed_jpg.size[0],
                                           length=self.unprocessed_jpg.size[0])
        self.horizontal_slider.grid(row=1, column=0)
        self.horizontal_slider.set(100)

        self.downward_stretch()

        self.vertical_index_list = list(range(0, self.unprocessed_jpg.size[1]))
        self.horizontal_index_list = list(range(0, self.unprocessed_jpg.size[0]))

    def save_image(self):
        save_filename = filedialog.asksaveasfilename(defaultextension='*.jpg')
        self.processed_image.save(save_filename)

    def random_stretch(self):
        self.vertical_slider.set(random.randint(1, self.unprocessed_jpg.size[1]))
        self.intensity_value.set(random.randint(1,13))
        print('random not working right now')
        # self.display_image()


def main():
    root = Tk()
    Gui(root)
    root.mainloop()


if __name__ == '__main__':
    main()