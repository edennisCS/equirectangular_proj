import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showerror

from pathlib import Path
from functools import partial

import matplotlib.pyplot as plt

from src.cube import Cube


class App(tk.Tk):
    sides_per_tesselation = {
        "Cube": 6,
        "Tetrahedron": 4,
        "Octahedron": 8,
        "Dodecahedron": 12,
        "Isocahedron": 20
    }

    tesselations = (
        "Cube",
        "Tetrahedron",
        "Octahedron",
        "Dodecahedron",
        "Isocahedron"
    )

    # placeholder use cube for all for poc to be edited with other tesselations when complete
    tesselation_classes_by_name = {
        "Cube": Cube,
        "Tetrahedron": Cube,
        "Octahedron": Cube,
        "Dodecahedron": Cube,
        "Isocahedron": Cube
    }

    def __init__(self):
        super().__init__()

        # create the root window
        self.title('Select a tesselation')
        self.resizable(True, True)
        self.geometry('2000x1000')

        # datatype of selected tesselation
        self.selected_tesselation = tk.StringVar(self)

        # initial selected tesselation
        self.selected_tesselation.set( "Cube" )

        self.create_teselation_select()
        self.create_file_selects()
        self.create_generate_button()

    def create_teselation_select(self):
        self.paddings = {'padx': 5, 'pady': 5}

        # label
        label = ttk.Label(self, text='Select a Tesselation:')
        label.grid(column=0, row=0, sticky=tk.W, **self.paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.selected_tesselation,
            self.tesselations[0],
            *self.tesselations,
            command=self.tesselation_selected)

        option_menu.grid(column=1, row=0, sticky=tk.W, **self.paddings)

        # output label
        self.output_label = ttk.Label(self, foreground='red', text = "Selected tesselation has % s sides" % self.sides_per_tesselation[self.selected_tesselation.get()] )
        self.output_label.grid(column=0, row=1, sticky=tk.W, **self.paddings)

    def create_file_selects(self):
        self.file_selects = []
        self.file_select_labels = []
        self.selected_filenames = {}

        # we create a file select for every individual side in a tesselation 
        for side_number in list(range(0, self.sides_per_tesselation[self.selected_tesselation.get()])) :
            # indivdual file select button
            self.file_selects.append(ttk.Button(
                self,
                text='Select image for side % s' % (side_number + 1),
                command= partial(self.select_file, side_number)
            ))

            # we divide the file selects into rows of 3 starting under existing buttons
            column_number = 2*(side_number % 3)
            row_number = int((side_number / 3) + 2)

            self.file_selects[-1].grid(column=column_number, row=row_number, sticky=tk.W, **self.paddings)

            # a label to show selected file name
            self.file_select_labels.append(ttk.Label(
                self,
                text='No image selected'
            ))

            self.file_select_labels[-1].grid(column=column_number+1, row=row_number, sticky=tk.W, **self.paddings)

    def create_generate_button(self):
        # a button to generate the tesselation  based on the selected images
        self.generate_button = ttk.Button(
            self,
            text='Generate',
            command = self.generateTesselation
        )

        # put the generate button below all the file selects
        row_number = int((len(self.file_selects) / 3) + 3)
        self.generate_button.grid(column=0, row=row_number, sticky=tk.W, **self.paddings)

    def generateTesselation(self):
        # ensure a file is selected for every side
        for side_number in list(range(0, self.sides_per_tesselation[self.selected_tesselation.get()])):
            if(self.selected_filenames.get(side_number) is None):
                return showerror("Missing side", "Select an image for side: % s" % (side_number + 1))

        # find class of selected tesselation
        tesselation_class = self.tesselation_classes_by_name[self.selected_tesselation.get()]

        # render tesselation
        tesselation = tesselation_class(self.selected_filenames.values())
        tesselation.render(plt)

    def destroy_file_selects(self):
        # loop through all file selects and destroy
        for file_select in self.file_selects:
            file_select.destroy()

        # loop through all file select labels and destroy
        for label in self.file_select_labels:
            label.destroy()

        # destroy generate button because it needs to be repositioned
        self.generate_button.destroy()


    def tesselation_selected(self, *args):
        # update teselation selected text for the sides of selected tesselation
        self.output_label['text'] = "Selected tesselation has % s sides" % self.sides_per_tesselation[self.selected_tesselation.get()] 

        # destroy existing file selects as a new number is needed for the newly selected tesselation
        self.destroy_file_selects()

        # recreate a new number of file selects for the number of sides in new tesselation
        self.create_file_selects()
        self.create_generate_button()

    def select_file(self, side_number):
        # only accept png as transparency is used in tesselation
        filetypes = (
            ('image files', '*.png'),
            ('All files', '*.*')
        )

        # file select dialog
        filename = fd.askopenfilename(
            title='Select image',
            initialdir='/',
            filetypes=filetypes)

        # if a file is selected update the selected file for the side
        if(len(filename) != 0):
            self.selected_filenames[side_number] = filename
            self.file_select_labels[side_number]['text'] = "Selected image % s" % Path(filename).name
