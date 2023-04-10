#!/usr/bin/env python3
from tkinter import Tk, Menu
from tkinter.ttk import *
from tkinter.messagebox import askquestion

from controller.reroute import Route_Locally, Route_Remotely, Flush
from utils.debug import dbg, INFO, SUCCESS, IGNORE, WARNING, ERROR

from scanner.scan import Scanner
from spoofer.spoof import Spoofer
from cutter.cut import Cutter
from sniffer.sniff import Sniffer

# ('clam', 'alt', 'default', 'classic')
def run():
    try:
        dbg("Starting PacS..", INFO)


        ps = Tk()
        ps.title("PacS | v1.0.0 (Beta)")

        Style().theme_use("clam")

        menu = Menu(ps)
        packets_menu = Menu(tearoff=False)
        menu.add_cascade(label="Packets", menu=packets_menu)
        route_menu = Menu(tearoff=False)
        packets_menu.add_cascade(label="Route", menu=route_menu)
        route_menu.add_command(label="locally", command=lambda: Route_Locally())
        route_menu.add_command(label="remotely", command=lambda: Route_Remotely())
        packets_menu.add_command(label="flush", command=lambda: Flush())

        tools_menu = Menu(tearoff=False)
        menu.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Scanner", command=lambda :Scanner())
        tools_menu.add_command(label="Spoofer", command=lambda :Spoofer())
        tools_menu.add_command(label="Cutter", command=lambda :Cutter())
        sniffer_menu = Menu(tearoff=False)
        tools_menu.add_cascade(label="Sniffer", menu=sniffer_menu)

        def exit_():
            a = askquestion(title="Exit?!", message="Are you sure?", default="no")
            if a == "yes":
                ps.quit()

        menu.add_command(label="Exit", command=lambda: exit_())

        main_frame = PanedWindow(ps, orient='vertical')
        main_frame.pack(fill='both', expand=True)


        # main_frame.add(lower_frame)

        # main_frame.paneconfigure(tagOrId=upper_frame, height=0)
        # main_frame.paneconfigure(tagOrId=lower_frame, height=0)

        Sniffer(add_module_to=main_frame, sniffer_action_menu=sniffer_menu)

        ps.config(menu=menu)
        dbg("PacS is running.", SUCCESS)
        ps.mainloop()
        dbg("Exiting..", IGNORE)
    except KeyboardInterrupt:
        dbg("Next time don't use Ctrl+C to avoid tool crashing.", WARNING)
    except Exception as error:
        dbg(error, ERROR)
    Flush()
    dbg("Bye!", INFO)


run()
