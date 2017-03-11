from wifi import Cell, Scheme
import json

def scanwifi(interface):

	cells = list(Cell.all(interface))
	data = {}

	for cell in cells:
		data[cell.ssid] = [cell.address, cell.signal]
	
	#	print("SSID: ", cell.ssid, cell.signal)
	#	print("Signal: ", cell.signal)
	#	print("Address: ", cell.address)

	# Once the data is read, parse it in json
	res = json.dumps(data)


	# To bytes
	return bytes( res, "ascii")
