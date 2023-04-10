import datetime
import threading
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Treeview

import netfilterqueue
from netfilterqueue import COPY_PACKET
from scapy.layers.inet import IP, TCP
import pyperclip
from scapy.packet import Raw

from cutter.columns import cut_table_columns
from cutter.tableHeaders import Headers
from utils.tables.moveableCells import Moveable_Treeview_cells
from utils.Randomizer import randomize
from utils.tables.search import Search
from utils.tables.SortTableBy import sortable_ables, Sort_table
from utils.debug import dbg, INFO, SUCCESS, ERROR
from utils.tables.focuslast import FocusLast
from utils.tooltip import ToolTip


cutted = {}
cutter_id_len = 25

def Cutter():
    dbg("Loading cutter..", INFO)

    window = Toplevel()
    window.title("Cutter")

    menubar = Menu(tearoff=False)
    cutter_menu = Menu(tearoff=False)
    menubar.add_cascade(label="Scanner", menu=cutter_menu)

    def Accept_OR_Drop():
        if accept_dropVar.get():
            dbg("Cutter set to '%s'" % "Accept", SUCCESS)
            accept_drop.config(text="ACCEPT", highlightbackground="green", selectcolor="green")
            cutter_menu.entryconfigure(index=1, background="green", label="ACCEPT")
        else:
            dbg("Cutter set to '%s'" % "Drop", SUCCESS)
            accept_drop.config(text="DROP", highlightbackground="red", background="red")
            cutter_menu.entryconfigure(index=1, background="red", label="DROP")

    interactions_frame = Frame(window)
    interactions_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    start = Button(interactions_frame, text="start", cursor='hand2', takefocus=False)
    start.pack(side='right', fill='both')
    ToolTip(start, "Start data interrupting operation!")

    accept_dropVar = BooleanVar(value=True)
    accept_drop = Checkbutton(interactions_frame, text="ACCEPT", takefocus=False, selectcolor="green",
                              indicatoron=False, command=lambda: Accept_OR_Drop(), variable=accept_dropVar)
    accept_drop.pack(side='right', fill='both', expand=True, padx=5)
    ToolTip(accept_drop, "Accept/Drop packets!!")

    clear = Button(interactions_frame, text="clear", cursor='hand2', takefocus=False,
                   command=lambda: cut_table.delete(*cut_table.get_children()))
    clear.pack(side='left')
    ToolTip(clear, "Delete all captured packets !PERMANENTLY!")

    def Export():
        if cutted:
            save_as = asksaveasfilename(title="Save cutter data %s to:" % len(cutted), defaultextension=f".cut",
                                        filetypes=(("(P)acket(S)", f"*.cut"),))
            if save_as:
                clear.config(state="disabled", cursor="")
                data = {}
                for packet_id in cutted:
                    data[packet_id] = cutted[packet_id].fields
                with open(save_as, mode="w", errors="replace") as data2file:
                    data2file.write(str(data))
                data2file.close()
                clear.config(state="normal", cursor="hand2")

    export = Button(interactions_frame, text="export", cursor="hand2", takefocus=False, command=lambda: Export())
    export.pack(side='left', padx=5)
    ToolTip(export, "Export cutter packets to *.cut (plaintext:json) file.")

    browse_resultVar = BooleanVar(value=False)
    browse_result = Checkbutton(interactions_frame, text="browse", takefocus=False, variable=browse_resultVar)
    browse_result.pack(side='left', padx=5)
    ToolTip(browse_result, "Allow browsing packets while running.")

    table_frame = Frame(window)
    table_frame.pack(fill='both', expand=True, padx=5, pady=5)

    search = Entry(table_frame, takefocus=False, cursor="xterm", background="cyan")
    search.pack(side='top', fill='x')
    ToolTip(search, "Search for packet by [ID].")

    search.bind("<Return>", lambda a: Search(query=search.get(), data=cutted))

    cut_result_SBY = Scrollbar(table_frame, orient="vertical")
    cut_result_SBY.pack(side='right', fill='y')

    cut_result_SBX = Scrollbar(table_frame, orient="horizontal")
    cut_result_SBX.pack(side='bottom', fill='x')

    cut_table = Treeview(table_frame, columns=tuple(cut_table_columns.keys()), show="headings", yscrollcommand=cut_result_SBY.set, xscrollcommand=cut_result_SBX.set)
    cut_result_SBY.config(command=cut_table.yview)
    cut_result_SBX.config(command=cut_table.xview)

    Moveable_Treeview_cells(cut_table)

    sortable_ables[cut_table] = {}.fromkeys(tuple([str(c) for c in cut_table_columns.keys()]), "ascending")
    def SortTable(event):
        x = event.x
        y = event.y
        component = cut_table.identify_region(x=x, y=y)
        if component == "heading":
            Sort_table(table=cut_table, columns=cut_table_columns, x=x)
    cut_table.bind("<Button-1>", SortTable)


    def Show_Raw(event):
        x = event.x
        y = event.y
        if cut_table.identify_region(x=x, y=y) == "cell":
            try:
                id = cut_table.item(item=cut_table.identify_row(y=y))['values'][1]
                action = cut_table.item(item=cut_table.identify_row(y=y))['values'][-1]
                if id in cutted.keys():
                    data: IP = cutted[id]
                    window = Toplevel()
                    window.title(id + f" ({action})")
                    text = ScrolledText(window, wrap="word")
                    text.pack(side='top', fill='both', expand=True, padx=1, pady=1)
                    text.insert(1.0, str(data.fields))
                    if data.haslayer(Raw):
                        if data.haslayer(TCP):
                            if data[TCP].dport == 80:
                                text = ScrolledText(window, wrap="word")
                                text.pack(side='top', fill='both', expand=True, padx=1, pady=1)
                                text.insert(1.0, data[Raw].load.decode(errors="replace"))
                    window.mainloop()
            except Exception as e:
                print(e)

    cut_table.bind("<Double-Button-1>", Show_Raw)

    def Copy_row(event):
        x = event.x
        y = event.y
        if cut_table.identify_region(x=x, y=y) == "cell":
            try:
                column_num = cut_table.identify_column(x=x)  # as #0, #1, #2
                column_data = cut_table.column(
                    column=column_num)  # as {'width': 512, 'minwidth': 20, 'stretch': 1, 'anchor': 'center', 'id': 'DATA'}
                column_index = list(cut_table_columns.keys()).index(column_data['id'])
                item_id = cut_table.identify_row(y=y)
                pyperclip.copy(cut_table.item(item=item_id)['values'][column_index])
            except Exception:
                pass

    cut_table.bind("<Button-2>", Copy_row)

    cut_table.pack(fill='both', expand=True)
    cut_table.tag_bind(tagname="accept")
    cut_table.tag_bind(tagname="drop")
    cut_table.tag_configure(tagname="accept", background="green")
    cut_table.tag_configure(tagname="drop", background="red")
    Headers(table=cut_table, headers=cut_table_columns)

    def process_packet(packet: netfilterqueue.Packet):
        # hw = packet.get_hw()
        rand_id = randomize.id(cutter_id_len)
        payload = IP(packet.get_payload())
        # payload_length = packet.get_payload_len()
        # timestamp = packet.get_timestamp()
        # mark = packet.get_mark()
        at = datetime.datetime.now().strftime("%I:%M:%S %p")

        if accept_dropVar.get():
            packet.accept()
            index = str(len(cut_table.get_children()) + 1)
            # cut_table.insert(parent='', index='end', values=(index, str(packet), str(hw), str(payload), str(payload_length), str(timestamp), str(mark),"ACCEPT"), tags="accept")
            cutted[rand_id] = payload
            cut_table.insert(parent='', index='end',
                             values=(index, rand_id, str(packet), at, "ACCEPT"),
                             tags="accept")
            FocusLast(table=cut_table, var=browse_resultVar)
        else:
            packet.drop()
            index = str(len(cut_table.get_children()) + 1)
            # cut_table.insert(parent='', index='end', values=(index, str(packet), str(hw), str(payload), str(payload_length), str(timestamp), str(mark), "DROP"), tags="drop")
            cutted[rand_id] = payload
            cut_table.insert(parent='', index='end',
                             values=(index, rand_id, str(packet), at, "DROP"), tags="drop")
            FocusLast(table=cut_table, var=browse_resultVar)

    queue = netfilterqueue.NetfilterQueue()

    def RUN():
        try:
            dbg("Starting cutter..", INFO)
            queue.bind(queue_num=0, user_callback=process_packet, mode=COPY_PACKET)
            threading.Thread(target=queue.run, daemon=True).start()
            start.config(state='disabled', cursor='')
            cutter_menu.entryconfigure(index=0, state="disabled")
            dbg("Cutter started!", SUCCESS)
        except Exception as error:
            dbg(error, ERROR)

    start.config(command=lambda: RUN())
    cutter_menu.add_command(label="start", command=lambda: RUN())
    cutter_menu.add_checkbutton(label="ACCEPT", background="green", command=lambda: Accept_OR_Drop(),
                                       variable=accept_dropVar, indicatoron=False)
    cutter_menu.add_checkbutton(label="browse", variable=browse_resultVar)
    cutter_menu.add_command(label="export", command=lambda: Export())
    cutter_menu.add_command(label="clear", command=lambda: cut_table.delete(*cut_table.get_children()))

    dbg("Cutter loaded.", SUCCESS)
    window.config(menu=menubar)

    window.mainloop()