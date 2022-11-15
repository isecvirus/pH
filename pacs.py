#!/usr/bin/env python3

from tkinter import *
from tkinter.messagebox import askquestion

from controller.reroute import Route_Locally, Route_Remotely, Flush
from utils.debug import dbg, INFO, SUCCESS, IGNORE, WARNING, ERROR

from scanner.scan import Scanner
from spoofer.spoof import Spoofer
from cutter.cut import Cutter
from sniffer.sniff import Sniffer


def run():
    try:
        dbg("Starting PacS..", INFO)

        ps = Tk()
        ps.title("PacS | v1.0.0 (Beta)")

        menu = Menu(ps)
        packets_menu = Menu(tearoff=False)
        menu.add_cascade(label="Packets", menu=packets_menu)
        route_menu = Menu(tearoff=False)
        packets_menu.add_cascade(label="Route", menu=route_menu)
        route_menu.add_command(label="locally", command=lambda: Route_Locally())
        route_menu.add_command(label="remotely", command=lambda: Route_Remotely())
        packets_menu.add_command(label="flush", command=lambda: Flush())

        action_menu = Menu(tearoff=False)
        menu.add_cascade(label="Action", menu=action_menu)
        scanner_menu = Menu(tearoff=False)
        action_menu.add_cascade(label="Scanner", menu=scanner_menu)
        spoofer_menu = Menu(tearoff=False)
        action_menu.add_cascade(label="Spoofer", menu=spoofer_menu)
        cutter_menu = Menu(tearoff=False)
        action_menu.add_cascade(label="Cutter", menu=cutter_menu)
        sniffer_menu = Menu(tearoff=False)
        action_menu.add_cascade(label="Sniffer", menu=sniffer_menu)

        def exit_():
            a = askquestion(title="Exit?!", message="Are you sure?", default="no")
            if a == "yes":
                ps.quit()

        menu.add_command(label="Exit", command=lambda: exit_())

        main_frame = PanedWindow(ps, orient='vertical')
        main_frame.pack(fill='both', expand=True)

        upper_frame = PanedWindow()
        upper_frame.pack(side='top', fill='both', expand=True, pady=3, padx=3)
        main_frame.add(upper_frame)

        lower_frame = PanedWindow()
        lower_frame.pack(side='bottom', fill='both', expand=True, pady=3, padx=3)
        main_frame.add(lower_frame)

        main_frame.paneconfigure(tagOrId=upper_frame, height=0)
        main_frame.paneconfigure(tagOrId=lower_frame, height=0)

        Scanner(add_module_to=upper_frame, scanner_action_menu=scanner_menu)
        Spoofer(add_module_to=upper_frame, spoofer_action_menu=spoofer_menu)
        Cutter(add_module_to=lower_frame, cutter_action_menu=cutter_menu)
        Sniffer(add_module_to=lower_frame, sniffer_action_menu=sniffer_menu)

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
