"""
File where the main functions to interact with the network are. Also there are
some interesting functions to sort the dictionary of the networks.
"""

from wifi import Cell
import json
from collections import OrderedDict


def scanwifi(interface, order=None):
    """ Main function of the app, searches for the AP near and formats them to
    json in order to transfer it to the client module.

    Args:
        interface (str): interface to use in order to scan
        order (str): main attribute of the cell to order the resulting
        dictionary, if so.
    Returns:
        bytes: all the networks around the sensor and all its data in json
        format.
    """
    cells = list(Cell.all(interface))
    data = {}

    # Add all the elements into the dict
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
    """
    Sorts the dictionary of networks given by the key-word given. Only 2
    keywords implemented, address or signal.
    Args:
        dic (dictionary): dictionary of the networks to sort.
        key (str): keyword of the parameter of the network to priorize in
        position of the list.

    Returns:
        collections.OrderedDict: dictionary sorted with the specifications
        given.
    Raises:
        NotImplementedError if the keyword is not recognised.
    """
    if key == "address":
        return sort_by_idx(dic, 0)
    elif key == "signal":
        return sort_by_idx(dic, 1)
    else:
        raise NotImplementedError("That function is not implemented yet")


def sort_by_idx(dic, idx, bigger=True):
    """
    Assuming the format of the dictionary key:[i,i+1..] sorts the dictionary
    by the value index given. In ascendant or descendant order depending of the
    bigger argument value. Descendant by default.

    Args:
        dic (dictionary): dictionary of the networks to sort.

    Returns:
        collections.OrderedDict: dictionary sorted with the specifications
        given.
    """
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
