import tkinter as tk
import pyglet
from pyglet import font
pyglet.options['win32_gdi_font'] = True

import os

# Ensure the font file is in the same directory as your script or provide the full path

# Get the font name as pyglet recognizes it (often the base name of the file without extension)
# You might need to check the actual font name within the TTF file if it differs from the filename.
font.add_directory('MicrosoftAptosFonts')
root = tk.Tk()
root.title("Pyglet Custom Font Example")
label = tk.Label(root, text="Hello, Pyglet Custom Font!", font=('Aptos ExtraBold',40))
label.pack(pady=20)
root.mainloop()