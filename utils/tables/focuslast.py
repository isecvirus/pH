from tkinter import BooleanVar
from tkinter.ttk import Treeview


def FocusLast(var: BooleanVar, table: Treeview):
    if len(table.get_children()) > 0 and not var.get():
        table.see(table.get_children()[-1])
        table.focus(table.get_children()[-1])