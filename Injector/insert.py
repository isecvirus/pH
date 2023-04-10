import os
from http.client import HTTPResponse
from tkinter import StringVar
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.simpledialog import askstring
import urllib.request

def Insert_FromWebsite(rule_name:str, example_field:ScrolledText, last_inserted:StringVar):
    url = askstring(prompt="URL:", title=f"Insert html from website for rule({rule_name})")
    if url:
        try:
            response: HTTPResponse = urllib.request.urlopen(url=url)
            html = response.read().decode(errors="replace")
            last_inserted.set(value=html)
            example_field.config(state="normal")
            example_field.delete(1.0, 'end')
            example_field.insert(1.0, html)
            example_field.config(state="disabled")
        except Exception:
            pass

def Insert_FromFile(rule_name:str, example_field:ScrolledText, last_inserted:StringVar):
    file = askopenfilename(title=f"Insert html from file for rule({rule_name})")
    if file:
        if os.path.exists(file) and os.path.isfile(file):
            with open(file=file, mode="r", errors="replace") as file_data:
                html = file_data.read()
                last_inserted.set(value=html)

                example_field.config(state="normal")
                example_field.delete(1.0, 'end')
                example_field.insert(1.0, html)
                example_field.config(state="disabled")
            file_data.close()
