import threading
from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Treeview, Combobox
import scapy.all as scapy
import scapy.layers.http
import netifaces
from scapy.layers.dns import DNSQR
import pyperclip
from scapy.layers.inet import TCP
from scapy.packet import Raw
from scapy.sendrecv import sniff
from sniffer.columns import sniff_table_columns
from sniffer.keywords import default_keywords, Delete_keyword, LoadFromFile, Add_keyword
from sniffer.get_url import get_url
from sniffer.login_info import get_login_info
from utils.tables.moveableCells import Moveable_Treeview_cells
from sniffer.tableHeaders import Headers
from utils.Randomizer import randomize
from utils.tables.search import Search
from utils.tables.SortTableBy import sortable_ables, Sort_table
from utils.debug import dbg, INFO, SUCCESS, WARNING
from utils.tables.focuslast import FocusLast
from utils.tooltip import ToolTip

sniffed = {}
sniffer_id_len = 25


def Sniffer(add_module_to, sniffer_action_menu: Menu):
    dbg("Loading sniffer..", INFO)
    sniff_frame = LabelFrame(text="SNIFFER")
    sniff_frame.pack(side='right', expand=True, fill='both', padx=5, pady=5)
    add_module_to.add(sniff_frame)

    interactions_frame = Frame(sniff_frame)
    interactions_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    start_sniff = Button(interactions_frame, text="sniff", cursor="hand2", takefocus=False)
    start_sniff.pack(side='left', padx=5)
    ToolTip(start_sniff, "Start sniffing packets.")

    keywords_frame = LabelFrame(sniff_frame, text="keywords")
    keywords_frame.pack(side='right', fill='both')
    keywords_actions_frame = Frame(keywords_frame)
    keywords_actions_frame.pack(side='bottom', fill='x', padx=5, pady=5)

    keyword_input = Entry(keywords_frame, background="cyan")
    keyword_input.pack(side='top', fill='x')
    ToolTip(keyword_input, "Keywords to hunt [CREDENTIALS]")

    inner_keywords_frame = Frame(keywords_frame)
    inner_keywords_frame.pack(fill='both', expand=True)

    keywords_SBY = Scrollbar(inner_keywords_frame, orient="vertical")
    keywords_SBX = Scrollbar(inner_keywords_frame, orient="horizontal")
    keywords_SBY.pack(side='right', fill='y')

    keywords_SBX.pack(side='bottom', fill='x')

    keywords = Listbox(inner_keywords_frame, takefocus=False, justify="center", selectmode="single",
                       yscrollcommand=keywords_SBY.set, xscrollcommand=keywords_SBX.set)
    keywords.pack(fill='both', expand=True)

    keywords_SBY.config(command=keywords.yview)
    keywords_SBX.config(command=keywords.xview)

    keywords.bind("<BackSpace>", lambda a: Delete_keyword(List=keywords))
    keywords.bind("<Delete>", lambda a: Delete_keyword(List=keywords))

    for dk in default_keywords:
        dbg("Added '%s' as a keywords for sniffer." % dk, SUCCESS)
        keywords.insert('end', dk)

    load_fromFile = Button(keywords_actions_frame, text="load", command=lambda: LoadFromFile(List=keywords),
                           cursor="hand2",
                           takefocus=False)
    load_fromFile.pack(side='left', fill='x', expand=True)
    ToolTip(load_fromFile, "Load keywords from a file.")

    clear_all = Button(keywords_actions_frame, text="clear", command=lambda: keywords.delete(0, 'end'), cursor="hand2",
                       takefocus=False)
    clear_all.pack(side='right', fill='x', expand=True)
    ToolTip(clear_all, "Removes all keywords !PERMANENTLY!")

    keyword_input.bind("<Return>", lambda a: Add_keyword(List=keywords, kw_entry=keyword_input))

    table_frame = Frame(sniff_frame)
    table_frame.pack(fill='both', padx=5, pady=5, expand=True)

    inputs_frame = Frame(table_frame)
    inputs_frame.pack(side='top', fill='x')

    search = Entry(inputs_frame, takefocus=False, cursor="xterm", background="cyan")
    search.pack(side='left', fill='x', expand=True)
    ToolTip(search, "Search for packet by [ID].")

    data_filter = Entry(inputs_frame, background="red", foreground="white")
    data_filter.pack(side='right', fill='x', expand=True)
    ToolTip(data_filter, "Only packets contains [THIS], !(LEAVE EMPTY FOR ALL)!")

    search.bind("<Return>", lambda a: Search(query=search.get(), data=sniffed))

    sniff_result_SBY = Scrollbar(table_frame, orient="vertical")
    sniff_result_SBY.pack(side='right', fill='y')

    sniff_result_SBX = Scrollbar(table_frame, orient="horizontal")
    sniff_result_SBX.pack(side='bottom', fill='x')

    sniff_table = Treeview(table_frame, columns=tuple(sniff_table_columns.keys()), show="headings", yscrollcommand=sniff_result_SBY.set, xscrollcommand=sniff_result_SBX.set)
    sniff_table.pack(side='left', fill='both', expand=True)
    sniff_result_SBY.config(command=sniff_table.yview)
    sniff_result_SBX.config(command=sniff_table.xview)
    sniff_table.tag_bind(tagname="creds")
    sniff_table.tag_configure(tagname="creds", background="red", foreground="white")
    sniff_table.tag_bind(tagname="dns")
    sniff_table.tag_configure(tagname="dns", background="yellow", foreground="black")
    Headers(table=sniff_table, headers=sniff_table_columns)

    Moveable_Treeview_cells(sniff_table)

    sortable_ables[sniff_table] = {}.fromkeys(tuple([str(c) for c in sniff_table_columns.keys()]), "ascending")

    def SortTable(event):
        x = event.x
        y = event.y
        component = sniff_table.identify_region(x=x, y=y)
        if component == "heading":
            Sort_table(table=sniff_table, columns=sniff_table_columns, x=x)

    sniff_table.bind("<Button-1>", SortTable)

    def Show_Raw(event):
        x = event.x
        y = event.y
        if sniff_table.identify_region(x=x, y=y) == "cell":
            try:
                id = sniff_table.item(item=sniff_table.identify_row(y=y))['values'][1]
                if id in sniffed.keys():
                    data: scapy.layers.http.HTTPRequest = sniffed[id].fields
                    window = Toplevel()
                    window.title(id)
                    text = ScrolledText(window, wrap="word")
                    text.pack(side='top', fill='both', expand=True, padx=1, pady=1)
                    text.insert(1.0, str(data))
                    if data.haslayer(Raw):
                        if data.haslayer(TCP):
                            if data[TCP].dport == 80:
                                text = ScrolledText(window, wrap="word")
                                text.pack(side='top', fill='both', expand=True, padx=1, pady=1)
                                text.insert(1.0, data[Raw].load.decode(errors="replace"))
                    window.mainloop()
            except Exception:
                pass

    sniff_table.bind("<Double-Button-1>", Show_Raw)

    def Copy_row(event):
        x = event.x
        y = event.y
        if sniff_table.identify_region(x=x, y=y) == "cell":
            try:
                column_num = sniff_table.identify_column(x=x)  # as #0, #1, #2
                column_data = sniff_table.column(
                    column=column_num)  # as {'width': 512, 'minwidth': 20, 'stretch': 1, 'anchor': 'center', 'id': 'DATA'}
                column_index = list(sniff_table_columns.keys()).index(column_data['id'])
                item_id = sniff_table.identify_row(y=y)
                pyperclip.copy(sniff_table.item(item=item_id)['values'][column_index])
            except Exception:
                pass

    sniff_table.bind("<Button-2>", Copy_row)

    clear = Button(interactions_frame, text="clear", cursor="hand2", takefocus=False,
                   command=lambda: sniff_table.delete(*sniff_table.get_children()))
    clear.pack(side='right', padx=2)
    ToolTip(clear, "Delete all sniffed packets !PERMANENTLY!")

    def Export():
        if sniffed:
            save_as = asksaveasfilename(title="Save %s sniffer data to:" % len(sniffed),
                                        defaultextension=f".sniff", filetypes=(("(P)acket(S)", f"*.sniff"),))
            if save_as:
                clear.config(state="disabled", cursor="")
                data = {}
                for packet_id in sniffed:
                    data[packet_id] = sniffed[packet_id].fields
                with open(save_as, mode="w", errors="replace") as data2file:
                    data2file.write(str(data))
                data2file.close()
                clear.config(state="normal", cursor="hand2")

    export = Button(interactions_frame, text="export", cursor="hand2", takefocus=False, command=lambda: Export())
    export.pack(side='right', padx=5)
    ToolTip(export, "Export sniffer packets to a *.sniff (plaintext:json) file")

    browse_resultVar = BooleanVar(value=False)
    browse_result = Checkbutton(interactions_frame, text="browse", takefocus=False, variable=browse_resultVar)
    browse_result.pack(side='right')
    ToolTip(browse_result, "Allow browsing packets while running.")

    interfaces = sorted(netifaces.interfaces())
    interfaceVar = StringVar()
    if len(interfaces) > 0:
        interfaceVar.set(interfaces[0])
    interface = Combobox(interactions_frame, takefocus=False, exportselection=True, values=interfaces, state="readonly",
                         textvariable=interfaceVar)
    interface.pack(side='right', fill='x', expand=True)
    ToolTip(interface, "Pick an interface to sniff data from.")

    def Update_interfaces():
        # dbg("Updating interfaces..", INFO)
        interface.config(values=netifaces.interfaces())

    interface.bind("<Button-1>", lambda a: Update_interfaces())
    interface.bind("<Enter>", lambda a: Update_interfaces())
    interface.bind("<Leave>", lambda a: Update_interfaces())

    def start_sniffer():
        dbg("Sniffer started using interface '%s'" % interfaceVar.get(), SUCCESS)
        sniff(iface=interfaceVar.get(), store=False, prn=process_sniffed_packet)
        start_sniff.config(state="disabled")

    def process_sniffed_packet(packet):
        """
        [<Ether  dst=e4:54:e8:d4:d6:6c src=00:c0:ca:ae:54:98 type=IPv4 |<IP  version=4 ihl=5 tos=0x0 len=478 id=57701 flags=DF frag=0 ttl=64 proto=tcp chksum=0xc6d src=192.168.100.183 dst=44.228.249.3 |<TCP  sport=54128 dport=http seq=2956432290 ack=1471430401 dataofs=8 reserved=0 flags=PA window=497 chksum=0x6273 urgptr=0 options=[('NOP', None), ('NOP', None), ('Timestamp', (4184639756, 1972643878))] |<HTTP  |<HTTPRequest  Method='GET' Path='/login.php' Http_Version='HTTP/1.1' Accept='text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' Accept_Encoding='gzip, deflate' Accept_Language='en-US,en;q=0.5' Connection='keep-alive' Cookie='login=test%2Ftest' Host='testphp.vulnweb.com' Referer='http://testphp.vulnweb.com/login.php' Upgrade_Insecure_Requests='1' User_Agent='Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0' |>>>>>]
        """
        f = data_filter.get()
        if packet.haslayer(scapy.layers.http.HTTPRequest):
            url = get_url(packet)
            rand = randomize.id(sniffer_id_len)
            index = str(len(sniff_table.get_children()) + 1)
            url = url.decode(errors="replace")
            if f in str(url):
                sniff_table.insert(parent='', index='end', values=(index, rand, "URL", url))

                sniffed[rand] = packet[scapy.layers.http.HTTPRequest]  # rp=raw packet

            credentials = get_login_info(packet, List=keywords)
            if credentials and f in str(credentials):
                rand = randomize.id(sniffer_id_len)
                sniffed[rand] = packet[scapy.layers.http.HTTPRequest]  # rp=raw packet
                sniff_table.insert(parent='', index='end', values=(index, rand, "CREDS", credentials), tags="creds")

            FocusLast(table=sniff_table, var=browse_resultVar)
        elif packet.haslayer(DNSQR):
            url = str(packet[DNSQR].qname.decode(errors='replace'))[:-1]
            index = str(len(sniff_table.get_children()) + 1)
            rand = randomize.id(sniffer_id_len)
            if f in url:
                sniff_table.insert(parent='', index='end', values=(index, rand, "DNS", url), tags="dns")
                sniffed[rand] = packet[DNSQR]

            FocusLast(table=sniff_table, var=browse_resultVar)

    def RUN():
        dbg("Running sniffer on interface '%s'" % interfaceVar.get(), WARNING)
        threading.Thread(target=start_sniffer).start()
        start_sniff.config(state='disabled', cursor="")
        interface.config(state='disabled')
        sniffer_packets_menu.entryconfigure(index=0, state="disabled")

    start_sniff.config(command=lambda: RUN())

    sniffer_packets_menu = Menu(tearoff=False)
    sniffer_action_menu.add_cascade(label="Packets", menu=sniffer_packets_menu)
    sniffer_packets_menu.add_command(label="sniff", command=lambda: RUN())
    sniffer_packets_menu.add_checkbutton(label="browse", variable=browse_resultVar)
    sniffer_packets_menu.add_command(label="export", command=lambda: Export())
    sniffer_packets_menu.add_command(label="clear", command=lambda: sniff_table.delete(*sniff_table.get_children()))

    sniffer_keywords_menu = Menu(tearoff=False)
    sniffer_action_menu.add_cascade(label="Keywords", menu=sniffer_keywords_menu)
    sniffer_keywords_menu.add_command(label="add", command=lambda: Add_keyword(List=keywords, kw_entry=keyword_input))
    sniffer_keywords_menu.add_command(label="load", command=lambda: LoadFromFile(List=keywords))
    sniffer_keywords_menu.add_command(label="clear", command=lambda: keywords.delete(0, 'end'))

    dbg("Sniffer loaded.", SUCCESS)
