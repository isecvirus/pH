import datetime
from tkinter import Entry
from tkinter.ttk import Treeview

from utils.debug import dbg, SUCCESS
from utils.validator import validator


def Add(table:Treeview, source:Entry, destination:Entry, data:dict, start_symbol:str):
    src = source.get()
    dst = destination.get()

    if validator.ip(src.strip()) and validator.ip(dst.strip()):
        for item in data.keys():
            if [src, dst] == data[item]['info']:
                return False
        else:
            dbg("Added '%s > %s'" % (src, dst), SUCCESS)
            index = len(table.get_children()) + 1
            at = datetime.datetime.now().strftime("%I:%M:%S %p")
            child = table.insert(parent='', index='end', values=(index, src, dst, at, "0", start_symbol), tags="stopped")
            data[child] = {"info": [src, dst], "status": False, "count": 0}
            source.delete(0, 'end')
            # destination.delete(0, 'end')
