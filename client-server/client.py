

#Names: Leen Abhari, Simrah Shabandri
import socket
import xml.etree.ElementTree as ET
import sys


if len(sys.argv) != 3:
    print("Usage: python client.py <query_file> <output_file>")
    sys.exit(1)

query_file = sys.argv[1]
output_file = sys.argv[2]


with open(query_file, 'r') as file:
    query_xml = file.read()

# create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 65432))

client_socket.send(query_xml.encode())

response_xml = client_socket.recv(4096).decode()

response_tree = ET.ElementTree(ET.fromstring(response_xml))
root = response_tree.getroot()

# Print the status of the response
status = root.find('status').text
print(f"Status: {status}")

# Save the response XML to the specified output file
with open(output_file, 'w') as file:
    file.write(response_xml)

# Close the socket connection
client_socket.close()
