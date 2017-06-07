# -*- coding: utf-8 -*-
# Author:
# vk.com/euthanazik

import tkinter as tk
from tkinter.colorchooser import *


class ColorConverter:
    def __init__(self):
        self.rgb = []

    def set_colors(self, r=None, g=None, b=None, colorlist=None, K=1):
        self.rgb = []
        if r and g and b:
            colorlist = [r, g, b]

        if colorlist:
            for color in colorlist:
                self.rgb.append((color / K) / 255)
        else:
            for x in range(3):
                self.rgb.append(1)

    def __str__(self):
        string = "%f, %f, %f, %d" % (self.rgb[0], self.rgb[1], self.rgb[2], 1)
        return string


class Controller:
    def __init__(self, tkroot):
        self.view = MainView(tkroot, self)
        self.converter = ColorConverter()

    @staticmethod
    def _to_hexstr(colorlist=None):
        return '#%02x%02x%02x' % colorlist

    def pick_color(self):
        colors = self.view.get_color()
        hexstring = self._to_hexstr(colorlist=colors)
        self.view.set_canvas_bgcolor(hexstring)
        self.converter.set_colors(colorlist=colors, K=1.3)
        self.view.color_string.set(self.converter)


class MainView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.parent.minsize(width=40, height=20)
        self.controller = controller
        self.color_string = tk.StringVar()
        self._draw_view()

    def _draw_view(self):
        self.parent.grid()

        #####################
        # Context menu
        #####################
        self.rmb_menu = tk.Menu(self.parent, tearoff=0)
        self.rmb_menu.add_command(label=u'Вырезать',
                                  accelerator='Ctrl+X',
                                  command=lambda: self.parent.focus_get().event_generate('<<Cut>>'))
        self.rmb_menu.add_command(label=u'Копировать',
                                  accelerator='Ctrl+C',
                                  command=lambda: self.parent.focus_get().event_generate('<<Copy>>'))
        self.rmb_menu.add_command(label=u'Вставить',
                                  accelerator='Ctrl+V',
                                  command=lambda: self.parent.focus_get().event_generate('<<Paste>>'))
        self.parent.bind("<Button-3>", self.popup)

        pick_button = tk.Button(self.parent, text="Подобрать цвет", command=self.controller.pick_color)
        pick_button.grid(
            column=0, row=0,
            padx=1, pady=1,
            sticky='EW'
        )
        self.canvas = tk.Canvas(self.parent, background='white')
        self.canvas.grid(
            column=0, row=1,
            padx=1, pady=1,
            sticky='NSEW'
        )
        color_output = tk.Entry(self.parent, textvariable=self.color_string)
        color_output.grid(
            column=0, row=2,
            padx=1, pady=1,
            sticky='EW'
        )
        self.parent.resizable(False, False)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.update()

    def set_canvas_bgcolor(self, hexstring="#000000"):
        self.canvas["background"] = hexstring

    def popup(self, event):
        self.rmb_menu.post(event.x_root, event.y_root)

    @staticmethod
    def get_color():
        color = askcolor()
        if not color[0]:
            return (255, 255, 255)
        color = [int(x) for x in color[0]]
        return tuple(color)

if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.title('Пипетка MSC')
    root.mainloop()
