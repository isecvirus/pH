from tkinter.ttk import Treeview

sortable_ables = {}

def Sort_table(table:Treeview, x:int, columns:dict):
    """
    This func will sort the tables based on last click.
    if [HEADER] clicked once will be sorted ascending(a-z0-9),
    twice will be sorted descending(z-a9-0), etc..
    """

    column_name = table.column(column=table.identify_column(x=x))['id']  # it's titled (Ex: Column)
    index = list(columns).index(column_name)
    all_data = [table.item(item=id)['values'] for id in table.get_children()]
    tbl = sortable_ables[table]
    sort_by = tbl[column_name]  # ascending(a-z0-9), descending(z-a9-0)

    if sort_by == "ascending":
        reverse = False
        tbl[column_name] = "descending"
    else:  # sort_by == "descending"
        reverse = True
        tbl[column_name] = "ascending"

    all_data = sorted(all_data, key=lambda x: x[index], reverse=reverse)
    table.delete(*table.get_children())
    for d in all_data:
        table.insert(parent='', values=d, index='end')
    # Rearrange(tables)


