# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
# from ttkbootstrap import utility
from tkinter import Toplevel, Label


class ToolTip:
    def __init__(
        self,
        widget,
        text="widget info",
        bootstyle=None,
        wraplength=None,
        fg=None,
        bg="#f2e9ce",
        **kwargs,
    ):
        """
        Parameters:

            widget (Widget):
                The tooltip window will position over this widget when
                hovering.

            text (str):
                The text to display in the tooltip window.

            wraplength (int):
                The width of the tooltip window in screenunits before the
                text is wrapped to the next line. By default, this will be
                a scaled factor of 300.

            **kwargs (Dict):
                Other keyword arguments passed to the `Toplevel` window.
        """
        self.widget = widget
        self.text = text
        self.bootstyle = bootstyle
        self.wraplength = wraplength
        self.toplevel = None
        self.bg = bg
        self.fg = fg

        # set keyword arguments
        # kwargs["overrideredirect"] = True
        # kwargs["master"] = self.widget
        self.toplevel_kwargs = kwargs

        # event binding
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<Motion>", self.move_tip)
        self.widget.bind("<ButtonPress>", self.hide_tip)

    def show_tip(self, *_):
        """Create a show the tooltip window"""
        if self.toplevel:
            return

        self.toplevel = Toplevel(**self.toplevel_kwargs)
        self.toplevel.overrideredirect(True)
        self.toplevel.attributes('-alpha', 0.95)
        lbl = Label(
            master=self.toplevel,
            text=self.text,
            justify='left',
            wraplength=self.wraplength,
            background=self.bg,
            foreground=self.fg
        )
        lbl.pack(fill='both', expand=True)

    def move_tip(self, *_):
        """Move the tooltip window to the current mouse position within the
        widget.
        """
        if self.toplevel:
            x = self.widget.winfo_pointerx() + -85
            y = self.widget.winfo_pointery() + -35
            self.toplevel.geometry(f"+{x}+{y}")

    def hide_tip(self, *_):
        """Destroy the tooltip window."""
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None