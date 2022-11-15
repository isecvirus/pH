import datetime
import json
import threading
import time
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.ttk import Treeview

import netifaces
import pyperclip

from controller.getMac import get_mac
from scanner.columns import scan_table_columns
from scanner.tableHeaders import Headers
from utils.tables.moveableCells import Moveable_Treeview_cells
from utils.tables.SortTableBy import Sort_table, sortable_ables
from utils.debug import dbg, INFO, WARNING, SUCCESS, IMPORTANT
from utils.tables.focuslast import FocusLast
from utils.tooltip import ToolTip

default_scan_timeout = 1
min_scan_range = 0
max_scan_range = 255


def Scanner(add_module_to, scanner_action_menu: Menu):
    dbg("Loading scanner..", INFO)

    scan_found = Label(text="SCANNER")

    scan_frame = LabelFrame(text="SCANNER", labelwidget=scan_found)
    scan_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
    add_module_to.add(scan_frame)

    interactions_frame = Frame(scan_frame)
    interactions_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    scan_btn = Button(interactions_frame, text="scan", takefocus=False, cursor='hand2')
    scan_btn.pack(side='right', fill='x', expand=True)
    ToolTip(scan_btn, "Start network scan operation!")

    packet_timeoutVar = IntVar(value=default_scan_timeout)
    packet_timeout = Spinbox(interactions_frame, from_=1, to=1440, takefocus=False, foreground="red",
                             textvariable=packet_timeoutVar, width=5, state="readonly", justify="center")
    packet_timeout.pack(side='right', fill='both', padx=5)
    ToolTip(packet_timeout, "Timeout till client response.")

    scan_toVar = IntVar(value=max_scan_range)
    scan_to = Spinbox(interactions_frame, from_=min_scan_range, to=max_scan_range, takefocus=False,
                      foreground="green", textvariable=scan_toVar, width=4, state="readonly", justify="center")
    scan_to.pack(side='right', fill='both', padx=5)
    ToolTip(scan_to, "Scan range [TO].")

    scan_fromVar = IntVar(value=min_scan_range)
    scan_from = Spinbox(interactions_frame, from_=min_scan_range, to=max_scan_range, takefocus=False,
                        foreground="green", textvariable=scan_fromVar, width=4, state="readonly", justify="center")
    scan_from.pack(side='right', fill='both', padx=5)
    ToolTip(scan_from, "Scan range [FROM].")

    def Export():
        if scan_table.get_children():
            save_as = asksaveasfilename(title="Save %s connected clients to:" % len(scan_table.get_children()),
                                        defaultextension=f".clients", filetypes=(("(P)acket(S)", f"*.clients"),))
            if save_as:
                data = {}
                for item in scan_table.get_children():
                    infos = scan_table.item(item=item)['values']
                    data[infos[0]] = infos[1:]
                with open(save_as, mode="w", errors="replace") as data2file:
                    data2file.write(json.dumps(data, indent=4))
                data2file.close()


    scan_BrowseVar = BooleanVar(value=False)
    browse_result = Checkbutton(interactions_frame, text="browse", takefocus=False, variable=scan_BrowseVar)
    browse_result.pack(side='right', fill='x')
    ToolTip(browse_result, "Allow browsing found clients while running.")

    export = Button(interactions_frame, text="export", cursor="hand2", takefocus=False, command=lambda: Export())
    export.pack(side='right', fill='x')
    ToolTip(export, "Export scanner clients to *.pacs (plaintext:json) file.")

    clear_btn = Button(interactions_frame, text="clear", takefocus=False, cursor='hand2',
                       command=lambda: scan_table.delete(*scan_table.get_children()))
    clear_btn.pack(side='left', fill='x')
    ToolTip(clear_btn, "Delete all found clients !PERMANENTLY!")

    table_frame = Frame(scan_frame)
    table_frame.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)

    scan_result_SBY = Scrollbar(table_frame, orient="vertical")
    scan_result_SBY.pack(side='right', fill='y')

    scan_result_SBX = Scrollbar(table_frame, orient="horizontal")
    scan_result_SBX.pack(side='bottom', fill='x')

    scan_table = Treeview(table_frame, columns=tuple(scan_table_columns.keys()), show="headings", yscrollcommand=scan_result_SBY.set, xscrollcommand=scan_result_SBX.set)

    def Copy_row(event):
        x = event.x
        y = event.y
        if scan_table.identify_region(x=x, y=y) == "cell":
            try:
                column_num = scan_table.identify_column(x=x)  # as #0, #1, #2
                column_data = scan_table.column(
                    column=column_num)  # as {'width': 512, 'minwidth': 20, 'stretch': 1, 'anchor': 'center', 'id': 'DATA'}
                column_index = list(scan_table_columns.keys()).index(column_data['id'])
                item_id = scan_table.identify_row(y=y)
                pyperclip.copy(scan_table.item(item=item_id)['values'][column_index])
            except Exception:
                pass

    scan_table.bind("<Button-2>", Copy_row)

    Moveable_Treeview_cells(scan_table)

    sortable_ables[scan_table] = {}.fromkeys(tuple([str(c) for c in scan_table_columns.keys()]), "ascending")
    def SortTable(event):
        x = event.x
        y = event.y
        component = scan_table.identify_region(x=x, y=y)
        if component == "heading":
            Sort_table(table=scan_table, columns=scan_table_columns, x=x)
    scan_table.bind("<Button-1>", SortTable)

    scan_table.pack(fill='both', expand=True)
    scan_result_SBY.config(command=scan_table.yview)
    scan_result_SBX.config(command=scan_table.xview)
    Headers(table=scan_table, headers=scan_table_columns)
    
    def Start_Scan():
        if scan_toVar.get() > scan_fromVar.get():
            class clients:
                found = 0

            scan_from.config(state="disabled")
            scan_to.config(state="disabled")

            dbg(f"Start scan operation <{scan_fromVar.get()}-{scan_toVar.get()}:{packet_timeoutVar.get()}>..", WARNING)
            scan_btn.config(state="disabled", cursor="", text="Scanning..")
            scanner_action_menu.entryconfigure(index=0, state="disabled", label="Scanning..")

            scan_table.delete(*scan_table.get_children())

            defaults = netifaces.gateways()['default']
            gateway = defaults[list(defaults.keys())[0]][0]

            def get_client(ip):
                try:
                    start = time.time()
                    mac = get_mac(ip=ip, timeout=packet_timeoutVar.get()).upper()
                    end = "{:.3f}".format(time.time() - start)
                    at = datetime.datetime.now().strftime("%I:%M:%S %p")
                    scan_table.insert('', index='end', values=(ip, mac, end, at))
                    clients.found += 1
                    scan_found.config(text=f"SCANNER (found: {str(clients.found)})")
                    dbg("'%s' is online (responded estimated '%s')." % (ip, end), IMPORTANT)
                    FocusLast(var=scan_BrowseVar, table=scan_table)
                except IndexError:
                    pass


            for octet in range(scan_fromVar.get(), scan_toVar.get() + 1):
                ip = '.'.join(str(gateway).split('.')[0:-1]) + ".%s" % octet
                threading.Thread(target=get_client, args=(ip,)).start()

            scan_btn.config(state="normal", cursor="hand2", text="scan")
            scanner_action_menu.entryconfigure(index=0, state="normal", label="scan")
            scan_from.config(state="normal")
            scan_to.config(state="normal")

    scan_btn.config(command=lambda: threading.Thread(target=Start_Scan).start())

    scanner_action_menu.add_command(label="scan", command=lambda: threading.Thread(target=Start_Scan).start())
    scanner_action_menu.add_command(label="export", command=lambda: Export())
    scanner_action_menu.add_command(label="clear", command=lambda: scan_table.delete(*scan_table.get_children()))
    scanner_action_menu.add_checkbutton(label="browse", variable=scan_BrowseVar)
    dbg("Scanner loaded.", SUCCESS)
