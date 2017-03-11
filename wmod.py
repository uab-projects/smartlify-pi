from wifi import Cell
import json
from collections import OrderedDict


def scanwifi(interface, order=None):

    cells = list(Cell.all(interface))
    data = {}

    for cell in cells:
        data[cell.ssid] = [cell.address, cell.signal, cell.encrypted]

    # Sort data if necessary
    if order is not None:
        data = sort_by_key(data, order)
    # Once the data is read and ordered if so, parse it in json
    res = json.dumps(data)
    # To bytes
    return bytes(res, "ascii")


def sort_by_key(dic, key):
    if key == "address":
        return sort_by_idx(dic, 0)
    elif key == "signal":
        return sort_by_idx(dic, 1)
    else:
        return 1


def sort_by_idx(dic, idx, bigger=True):
    lst = []
    dc = OrderedDict()

    for k, v in dic.items():
        lst.append((k, v[idx]))
        print((k, v))

    lst_sorted = sorted(lst, key=lambda tup: tup[1])

    if bigger:
        lst_sorted.reverse()

    for tup in lst_sorted:
        dc[tup[0]] = dic[tup[0]]

    return dc
