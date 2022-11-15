from tkinter import Toplevel, Text

from scapy.layers import http


def Search(query, data:dict):
    if query in data:
        data: http.HTTPRequest = data[query].fields

        window = Toplevel()
        window.title(query)
        text = Text(window, wrap="word")
        text.pack(fill='both', expand=True, padx=1, pady=1)
        text.insert(1.0, str(data))
        window.mainloop()
