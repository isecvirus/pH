from tkinter.ttk import Treeview
from utils.debug import dbg, INFO


def Headers(table: Treeview, headers: dict):
    for item in headers:
        dbg("Setting '%s' sniffer header." % item, INFO)
        width = headers[item]['width']
        align = headers[item]['align']
        stretch = headers[item]['stretch']
        table.column(column=item, width=width, stretch=stretch, anchor=align)
        table.heading(text=item, column=item)
