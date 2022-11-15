from tkinter.ttk import Treeview

def Moveable_Treeview_cells(tv: Treeview):
    # tv = Treeview
    def Down(event):
        tv = event.widget
        if tv.identify_row(event.y) not in tv.selection():
            tv.selection_set(tv.identify_row(event.y))

    def Up(event):
        tv = event.widget
        if tv.identify_row(event.y) in tv.selection():
            tv.selection_set(tv.identify_row(event.y))
    def Move(event):
        tv = event.widget
        moveto = tv.index(tv.identify_row(event.y))
        for s in tv.selection():
            tv.move(s, '', moveto)

    tv.bind("<ButtonPress-1>", Down, True)
    tv.bind("<ButtonRelease-1>", Up, True)
    tv.bind("<B1-Motion>", Move, True)