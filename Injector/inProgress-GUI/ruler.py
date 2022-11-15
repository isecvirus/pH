import re
from tkinter import Listbox, TclError, StringVar, Toplevel, LabelFrame, Frame, Button, BooleanVar, Checkbutton
from tkinter.scrolledtext import ScrolledText

from Injector.insert import Insert_FromFile, Insert_FromWebsite
from utils.lorem_ipsum import lorem_ipsum
from Injector.capture import rules

def Add_rule(
        rules_list: Listbox,
        rule: str,
        edit: bool = False,
        first_example: str = lorem_ipsum,
        rule_key: ScrolledText = None,
        rule_value: ScrolledText = None,
        Regex: bool = False
) -> None:
    """
    :param Regex:
    :param rules_list:
    -:: a list of all added rules.
    :param rule:
    -:: modification id for the html code rule.
    :param edit:
    -:: is this function request for editing a rule?
    :param first_example:
    -:: what text will appear as the example in the first run of this function.
    :param rule_key:
    -:: the html code that will be modified.
    :param rule_value:
    -:: what modifications will the html code get?
    :return:
    """
    last_inserted_example = StringVar(value=first_example)
    if (not rule in rules and len(rule.replace(" ", "")) > 0 or edit):
        window = Toplevel()
        window.attributes('-topmost', True)
        window.title(rule)
        window.resizable(False, False)

        example_frame = LabelFrame(window, text="Example", labelanchor='n')
        example_frame.pack(side='top', fill='both', padx=5, pady=5)

        example_loaders_frame = Frame(example_frame)
        example_loaders_frame.pack(side='bottom', fill='x')

        example_load_file = Button(example_loaders_frame, text="file",
                                   command=lambda: Insert_FromFile(rule_name=rule, example_field=example,
                                                                   last_inserted=last_inserted_example))
        example_load_file.pack(side='right', fill='x', expand=True)

        example_load_website = Button(example_loaders_frame, text="website",
                                      command=lambda: Insert_FromWebsite(rule_name=rule, example_field=example,
                                                                         last_inserted=last_inserted_example))
        example_load_website.pack(side='left', fill='x', expand=True)

        example = ScrolledText(example_frame, wrap="word", height=10, cursor="")
        example.insert(1.0, lorem_ipsum)
        example.config(state="disabled")
        example.pack(side='top')

        ############
        rule_key_frame = LabelFrame(window, text="Key")
        rule_key_frame.pack(side='top', fill='both', padx=5, pady=5)

        rule_value_frame = LabelFrame(window, text="Value")
        rule_value_frame.pack(side='top', fill='both', padx=5, pady=5)

        ############

        ############

        confirm_rule = Button(rule_value_frame, text="confirm")
        rule_key_field = ScrolledText(rule_key_frame, maxundo=-1, undo=True, height=10, wrap="word")
        rule_value_field = ScrolledText(rule_value_frame, maxundo=-1, undo=True, height=10, wrap="word")
        regex_rule_keyVar = BooleanVar(value=Regex)

        def UpdateExample():
            rk = rule_key_field.get(1.0, 'end').strip()
            rv = rule_value_field.get(1.0, 'end').strip()
            example.config(state="normal")
            modified_example = last_inserted_example.get().replace(rk, rv)
            if regex_rule_keyVar.get():
                try:
                    modified_example = re.sub(pattern=rk, repl=rv, string=last_inserted_example.get())
                    confirm_rule.config(state="normal")
                except re.error:
                    confirm_rule.config(state="disabled")
            else:
                confirm_rule.config(state="normal")
            example.config(state="normal")
            example.delete(1.0, 'end')
            example.insert(1.0, modified_example)
            example.config(state="disabled")

        ############
        if isinstance(rule_key, ScrolledText):
            rule_key_field.insert(1.0, rule_key.get(1.0, 'end'))
        elif isinstance(rule_key, str):
            rule_key_field.insert(1.0, rule_key)
        rule_key_field.pack(fill='both', expand=True)

        if isinstance(rule_value, ScrolledText):
            rule_value_field.insert(1.0, rule_value.get(1.0, 'end'))
        elif isinstance(rule_value, str):
            rule_value_field.insert(1.0, rule_value)
        rule_value_field.pack(fill='both', expand=True)

        ############

        ############

        def Confirm():
            rk = rule_key_field.get(1.0, 'end').strip()
            rv = rule_value_field.get(1.0, 'end').strip()
            reg = regex_rule_keyVar.get()
            if rk:
                if not rule in rules:
                    rules_list.insert('end', rule)
                rules[rule] = {"repl": rk, 'to': rv, 'regex': reg}
                window.destroy()

        ############

        ############
        rule_key_field.bind("<KeyPress>", lambda _: UpdateExample())
        rule_key_field.bind("<KeyRelease>", lambda _: UpdateExample())

        rule_value_field.bind("<KeyPress>", lambda _: UpdateExample())
        rule_value_field.bind("<KeyRelease>", lambda _: UpdateExample())
        ############

        ############
        regex_rule_key = Checkbutton(rule_key_frame, text="Regex", variable=regex_rule_keyVar)
        regex_rule_key.pack(side='bottom', anchor="w")
        regex_rule_key.bind("<ButtonPress>", lambda A: UpdateExample())
        regex_rule_key.bind("<ButtonRelease>", lambda A: UpdateExample())

        ############

        confirm_rule.config(command=lambda: Confirm())
        confirm_rule.pack(side='bottom', fill='x')


def Delete_rule(List: Listbox):
    try:
        index = list(List.get(0, 'end')).index(List.selection_get())
        rule = List.get(first=index, last=index)[0]
        List.delete(first=index, last=index)
        if rule in rules:
            del rules[rule]
    except TclError:
        pass
