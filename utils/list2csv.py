import csv

def pylist2csv(data: list, output_filename: str, columns:dict):
    """
    :param data: must be lists in a list:
    [
         [<data>, <data>, <data>],
         [<data>, <data>, <data>],
         etc..
    ]

    :param output_filename: Any
    :return:
    """

    # the below two lines is only checking if the
    # default tables headers are added correctly it..
    # will process, otherwise it will be added in..
    # the first index 0.

    headers = [str(header) for header in columns.keys()]
    if not data[0] == headers: data.insert(0, headers)

    for row_index, list in enumerate(data): # 1
        for column_index, string in enumerate(list): # 2
            data[row_index][column_index] = data[row_index][column_index].replace('\n', '') # 3

    with open(output_filename, 'w', newline='', errors="ignore") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    f.close()
