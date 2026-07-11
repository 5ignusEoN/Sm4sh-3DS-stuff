import glob
import os
from Tkinter import Tk

command = "py -2.7 ply2csv.py"

for i in glob.glob('.\\*.ply'):
    command += ' '+os.path.basename(os.path.abspath(i))

os.system(command)

