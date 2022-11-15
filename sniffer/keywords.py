import os
from tkinter import Listbox, TclError, Entry
from tkinter.filedialog import askopenfilename

default_keywords = sorted(["username", "user", "login", "password", "pass"])


def Add_keyword(List:Listbox, kw_entry:Entry):
    kw = kw_entry.get()
    if kw not in List.get(0, 'end') and len(kw.replace(' ', '')) > 0:
        List.insert('end', kw)
        kw_entry.delete(0, 'end')

def LoadFromFile(List:Listbox):
    file = askopenfilename(title="Load keywords from:", defaultextension=".txt")
    if file:
        if os.path.exists(file) and os.path.isfile(file):
            with open(file, "r", errors="replace") as data_file:
                for line in data_file.readlines():
                    kw = line.strip('\n')
                    if kw not in List.get(0, 'end'):
                        List.insert('end', kw)
            data_file.close()

def Delete_keyword(List:Listbox):
    try:
        index = list(List.get(0, 'end')).index(List.selection_get())
        List.delete(first=index, last=index)
    except TclError:
        pass