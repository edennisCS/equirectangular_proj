import tkinter as tk
import traceback
from functools import partial
from tkinter import ttk, messagebox
from tkinter.messagebox import showerror
from tkinter import colorchooser
import math

import matplotlib.pyplot as plt

from distortion import plot_panels
from src.cube import Cube
from src.octohedron import Octohedron


class App(tk.Tk):
    # sides_per_tesselation = {
    #     "Cube": 6,
    # }

    tessellations = {
        "Cube": {
            "sides": 6,
            "klass": Cube
        },
        "Octahedron": {
            "sides": 8,
            "klass": Octohedron
        },
    }

    # # placeholder use cube for all for poc to be edited with other tessellations when complete
    # tesselation_classes_by_name = {
    #     "Cube": Cube,
    # }

    window_size = '2000x1000'
    file_select_column_number = 3
    paddings = {'padx': 5, 'pady': 5}

    def __init__(self):
        super().__init__()

        # create the root window
        self.title('Select a tesselation')
        self.resizable(True, True)
        self.geometry(self.window_size)

        # datatype of selected tesselation
        self.selected_tesselation = tk.StringVar(self)

        # initial selected tesselation
        self.selected_tesselation.set("Cube")
        self.update_color_vars()
        print(f'init: {self.selected_tesselation.get()}')

        self.create_tesselation_select()
        self.create_color_selects()
        self.create_generate_button()

    def choose_color(self, color_var):
        color_code = colorchooser.askcolor(title="Choose a color")
        if color_code[1] is not None:
            color_var.set(color_code[1])
            print(f"Color: {color_code[1]}")
            return color_code[1]

    def update_color_vars(self):
        tesselation_type = self.selected_tesselation.get()
        number_of_sides = self.tessellations[tesselation_type]["sides"]
        self.color_vars = [tk.StringVar() for _ in range(number_of_sides)]

    def create_tesselation_select(self):
        print(f'Tesselation Select: {self.selected_tesselation.get()}')
        # label
        label = ttk.Label(self, text='Select a Tesselation:')
        label.grid(column=0, row=0, sticky=tk.W, **self.paddings)
        print(f"Th: {list(self.tessellations.keys())}")
        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.selected_tesselation,
            list(self.tessellations.keys())[0],
            *list(self.tessellations.keys()),
            command=self.tesselation_selected)

        option_menu.grid(column=1, row=0, sticky=tk.W, **self.paddings)

        # output label showing the number of sides for the selected tesselation
        self.output_label = ttk.Label(self, foreground='red',
                                      text=f"Selected tesselation has {self.tesselation_side_count()} sides")
        self.output_label.grid(column=0, row=1, sticky=tk.W, **self.paddings)
        print(f'Tesselation 1: {self.selected_tesselation.get()}')

    def create_generate_button(self):
        # a button to generate the tesselation  based on the selected images
        print(f'Generate: {self.selected_tesselation.get()}')
        self.generate_button = ttk.Button(
            self,
            text='Generate',
            command=self.generate_tesselation
        )

        # put the generate button below all the color selects
        row_number = math.ceil((len(self.color_selects) / self.file_select_column_number) + 8)
        self.generate_button.grid(column=0, row=row_number, sticky=tk.W, **self.paddings)

    def create_color_selects(self):
        print(f'Colour: {self.selected_tesselation.get()}')
        self.color_selects = []
        self.color_select_labels = []
        self.color_vars = []

        # available_colors = ("Red", "Green", "Blue", "Purple", "Yellow", "Pink")
        for side_number in range(self.tessellations[self.selected_tesselation.get()]["sides"]):
            label = ttk.Label(self, text=f'Color for side {side_number + 1}:')
            label.grid(column=0, row=side_number + 2, sticky=tk.W, **self.paddings)
            self.color_select_labels.append(label)

            color_var = tk.StringVar(self)
            self.color_vars.append(color_var)

            color_button = tk.Button(self, text='Choose color', command=lambda var=color_var: self.choose_color(var))
            color_button.grid(column=1, row=side_number + 2, sticky=tk.W)
            self.color_selects.append(color_button)

    def generate_tesselation(self):
        try:
            print("Generating tesselation...")
            for color_var in self.color_vars:
                if color_var.get() in ("None", ""):
                    tk.messagebox.showerror("Error", "Please select a color for each side.")
                    return

            colors = [color_var.get() for color_var in self.color_vars]
            print(colors)
            tesselation_instance = self.tessellations[self.selected_tesselation.get()]["klass"](colours=colors)
            plot_panels(tesselation_instance.panels, tesselation_instance.face_geometry)
            messagebox.showinfo("Success", "The tesselation was generated successfully.")
            print("Tesselation generated successfully.")

        except Exception as e:
            traceback.print_exc()
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def tesselation_selected(self, *args):
        # update tesselation selected text for the sides of selected tesselation
        self.output_label['text'] = f"Selected tesselation has {self.tesselation_side_count()} sides"
        self.generate_button.destroy()

        for label in self.color_select_labels:
            label.destroy()
        for color_select in self.color_selects:
            color_select.destroy()
        # recreate a new number of file selects for the number of sides in new tesselation

        self.create_color_selects()

        self.create_generate_button()

    def tesselation_side_count(self):
        print(f'tesselation: {self.selected_tesselation.get()}')
        return self.tessellations[self.selected_tesselation.get()]["sides"]


if __name__ == "__main__":
    app = App()
    app.mainloop()
