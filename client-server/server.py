
#Names: Leen Abhari, Simrah Shabandri
import socket
import xml.etree.ElementTree as ET
import csv

# first we get the directory.csv data
data = []

with open('directory.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)


# create a server socket and listen for client connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 65432))
server_socket.listen()
print("Hello! Server is running... Waiting for client to connect...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected with {addr}, YAY!")

    try:
        query_xml = conn.recv(4096).decode()

        query = ET.fromstring(query_xml)
        conditions = query.findall('condition')

        filtered_data = data
        column_exists = False 
        for condition in conditions:
            column = condition.find('column').text.strip() 
            value = condition.find('value').text.strip()   
            print(f"Filtering by: {column} = {value}")  

            if any(column in row for row in data):
                column_exists = True
                filtered_data = [row for row in filtered_data if row.get(column) and row[column].strip() == value]


        # create the response XML
        response = ET.Element('result')
        if column_exists:
            ET.SubElement(response, 'status').text = 'Success'
            if filtered_data:
                data_elem = ET.SubElement(response, 'data')
                for row in filtered_data:
                    row_elem = ET.SubElement(data_elem, 'row')
                    for key, value in row.items():
                        ET.SubElement(row_elem, key.lower()).text = value
            else:
                ET.SubElement(response, 'message').text = 'No data found :('
        else:
            ET.SubElement(response, 'status').text = 'failure'
            ET.SubElement(response, 'message').text = 'column not found :('
            
        response_xml = ET.tostring(response, encoding='utf-8')
        conn.send(response_xml)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()