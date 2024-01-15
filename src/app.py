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
    # Definition of available tessellations
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

    window_size = '2000x1000'
    paddings = {'padx': 5, 'pady': 5}

    def __init__(self):
        super().__init__()

        # create the root window
        self.title('Select a tessellation')
        self.resizable(True, True)
        self.geometry(self.window_size)

        # datatype of selected tessellation
        self.selected_tessellation = tk.StringVar(self)

        # initial selected tessellation
        self.selected_tessellation.set("Cube")
        self.update_color_vars()

        # Create selects and buttons
        self.create_tessellation_select()
        self.create_color_selects()
        self.create_generate_button()

    def choose_color(self, color_var):
        color_code = colorchooser.askcolor(title="Choose a color")
        if color_code[1] is not None:
            color_var.set(color_code[1])
            return color_code[1]

    def update_color_vars(self):
        number_of_sides = self.selected_tessellation_side_count()
        self.color_vars = [tk.StringVar() for _ in range(number_of_sides)]

    def create_tessellation_select(self):
        # label for tessellation dropdown
        label = ttk.Label(self, text='Select a Tessellation:')
        label.grid(column=0, row=0, sticky=tk.W, **self.paddings)
        # option menu to select tessellation
        option_menu = ttk.OptionMenu(
            self,
            self.selected_tessellation,
            self.tessellation_names()[0],
            *self.tessellation_names(),
            command=self.tessellation_selected)

        option_menu.grid(column=1, row=0, sticky=tk.W, **self.paddings)

        # output label showing the number of sides for the selected tessellation
        self.output_label = ttk.Label(self, foreground='red',
                                      text=f"Selected tessellation has {self.selected_tessellation_side_count()} sides")
        self.output_label.grid(column=0, row=1, sticky=tk.W, **self.paddings)

    def create_generate_button(self):
        # a button to generate the tessellation  based on the selected images
        self.generate_button = ttk.Button(
            self,
            text='Generate',
            command=self.generate_tessellation
        )

        # put the generate button below all the color selects
        row_number = len(self.color_selects) + 3
        self.generate_button.grid(column=0, row=row_number, sticky=tk.W, **self.paddings)

    def create_color_selects(self):
        self.color_selects = []
        self.color_select_labels = []
        self.color_vars = []

        # available_colors = ("Red", "Green", "Blue", "Purple", "Yellow", "Pink")
        for side_number in range(self.selected_tessellation_side_count()):
            label = ttk.Label(self, text=f'Color for side {side_number + 1}:')
            label.grid(column=0, row=side_number + 2, sticky=tk.W, **self.paddings)
            self.color_select_labels.append(label)

            color_var = tk.StringVar(self)
            self.color_vars.append(color_var)

            color_button = tk.Button(self, text='Choose color', command=lambda var=color_var: self.choose_color(var))
            color_button.grid(column=1, row=side_number + 2, sticky=tk.W)
            self.color_selects.append(color_button)

    def generate_tessellation(self):
        try:
            print("Generating tessellation...")
            for color_var in self.color_vars:
                if color_var.get() in ("None", ""):
                    tk.messagebox.showerror("Error", "Please select a color for each side.")
                    return

            colors = [color_var.get() for color_var in self.color_vars]
            print(colors)
            tessellation_instance = self.selected_tessellation_class()(colours=colors)
            plot_panels(tessellation_instance.panels, tessellation_instance.face_geometry)
            messagebox.showinfo("Success", "The tessellation was generated successfully.")
            print("Tessellation generated successfully.")

        except Exception as e:
            traceback.print_exc()
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def tessellation_selected(self, *args):
        # update tessellation selected text for the sides of selected tessellation
        self.output_label['text'] = f"Selected tessellation has {self.selected_tessellation_side_count()} sides"


        # Destroy all selects specific to tessellation
        self.destroy_tessellation_selects()

        # recreate a new number of file selects for the number of sides in new tessellation
        self.create_color_selects()
        self.create_generate_button()

    def destroy_tessellation_selects(self):
        # Destroy generate button so it can be re-rendered in correct position
        self.generate_button.destroy()

        # Destroy colour selects with their labels
        for label in self.color_select_labels:
            label.destroy()
        for color_select in self.color_selects:
            color_select.destroy()

    def selected_tessellation_class(self):
        return self.tessellations[self.selected_tessellation.get()]["klass"]

    def tessellation_names(self):
        return list(self.tessellations.keys())

    def selected_tessellation_side_count(self):
        return self.tessellations[self.selected_tessellation.get()]["sides"]
