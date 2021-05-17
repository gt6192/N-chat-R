import socket
from tkinter import *
import threading as td

# All required server and client info variables
HOST = ''  # host ip
PORT = ''  # host port
NAME = ''  # user defined host name
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket
clientsocket = []  # clients
address = []  # clients address
client_name = []


def insert_starting_widgets():
    heading_side.grid(row=1, column=0, columnspan="2")
    entry_host_label.grid(row=2, column=0, padx=10)
    entry_host.grid(row=2, column=1, pady=10, padx=10)
    entry_port_label.grid(row=3, column=0, padx=10)
    entry_port.grid(row=3, column=1, pady=10, padx=10)
    entry_name_label.grid(row=4, column=0, padx=10)
    entry_name.grid(row=4, column=1, pady=10, padx=10)
    create_server_button.grid(row=5, column=0, columnspan="2")
    warning_label.grid(row=6, column=0, columnspan="2", pady=5, padx=5)


def delete_starting_widgets():
    heading_side.grid_remove()
    entry_host_label.grid_remove()
    entry_host.grid_remove()
    entry_port_label.grid_remove()
    entry_port.grid_remove()
    entry_name_label.grid_remove()
    entry_name.grid_remove()
    create_server_button.grid_remove()
    warning_label.grid_remove()


def showing_connected_clients():
    server_status_widget.grid(row=1, column=0)
    server_stop_button.grid(row=1, column=1)
    clients_status.grid(row=2, column=0, columnspan="2")
    send_message.grid(row=3, column=0, columnspan="2", pady=5)
    send_message_button.grid(row=4, column=0, columnspan="2", pady=5)


def delete_showing_connected_clients():
    server_status_widget.grid_remove()
    clients_status.grid_remove()
    server_stop_button.grid_remove()
    send_message.grid_remove()
    send_message_button.grid_remove()


# function to create server
def create_server():
    global HOST, PORT, NAME, server
    HOST = entry_host.get()
    PORT = entry_port.get()
    NAME = entry_name.get()

    if len(HOST) <= 0 and len(PORT) <= 0 and len(NAME) <= 0:
        warning_label.config(text="You could not leave any field empty!", bg="yellow")
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, int(PORT)))
        server.listen(5)
        delete_starting_widgets()
        showing_connected_clients()
        accept_client_thread = td.Thread(target=accept_client)
        accept_client_thread.start()


# function to stop server
def stop_server():
    for close_client in clientsocket:
        try:
            close_client.close()
        except:
            temp = 0
    server.close()
    delete_showing_connected_clients()
    insert_starting_widgets()


# function to accept client's join request
def accept_client():
    global clientsocket, address
    clientsocket = []
    address = []
    i = 0
    while True:
        try:
            temp_client, temp_address = server.accept()
            clientsocket.append(temp_client)
            address.append(temp_address)
            clientsocket[i].send(bytes("connected "+NAME, "utf-8"))
            temp_client_name = clientsocket[i].recv(1024).decode("utf-8")
            client_name.append(temp_client_name)
            clients_status.insert(INSERT, f"Accepted client {address[i]} > {client_name[i]}\n")
            td.Thread(target=receive_data, args=(clientsocket[i], address[i], client_name[i])).start()
            i = i + 1
        except:
            return 0


def send_message_to_client():
    got_msg = send_message.get()
    final_msg = f"Server | {NAME} > {got_msg}"
    for i in clientsocket:
        try:
            i.send(bytes(final_msg, "utf-8"))
            clients_status.insert(INSERT, f"{final_msg}\n")
        except:
            temp = 0
    send_message.delete(0, "end")
    if got_msg == "exit":
        for close_client in clientsocket:
            try:
                close_client.close()
            except:
                temp = 0
        server.close()
        delete_showing_connected_clients()
        insert_starting_widgets()


def receive_data(single_client, client_address, single_client_name):
    while True:
        try:
            client_message = single_client.recv(1024).decode("utf-8")
            if len(client_message) <= 0:
                temp = 0
            else:
                if client_message == "exit":
                    single_client.close()
                    print(f"client {client_address} disconnected")
                    clients_status.insert(INSERT, f"({client_address[0]}) {single_client_name} > Disconnected\n")
                    return 0
                else:
                    clients_status.insert(INSERT, f"({client_address[0]}) > {client_message}\n")
                    for num_clients in clientsocket:
                        try:
                            num_clients.send(bytes(client_message, "utf-8"))
                        except:
                            temp = 0
        except:
            print(f"client {client_address} disconnected")
            clients_status.insert(INSERT, f"({client_address[0]}) {single_client_name} > Disconnected\n")
            return 0


# window start
window = Tk()
window.title("Create Server")


def window_close():
    server.close()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", window_close)

# Starting widgets for get host, port and name.
# heading widget
heading = Label(window, text="N-CHAT R", font=("courier", 30))
heading_side = Label(window, text="Server", font=("courier", 15))

# Taking HOST IP
entry_host_label = Label(window, text="Host IP", font=("courier", 12))
entry_host = Entry(window)

# Taking HOST PORT
entry_port_label = Label(window, text="Host Port", font=("courier", 12))
entry_port = Entry(window)

# Taking HOST NAME (of user's choice)
entry_name_label = Label(window, text="Host Name", font=("courier", 12))
entry_name = Entry(window)

# Button to run create_server function
create_server_button = Button(window, text="     Create     ", command=create_server, font=("courier", 12))

# Label to display error or success message
warning_label = Label(window, text="")

heading.grid(row=0, column=0, columnspan=2, pady=5)

insert_starting_widgets()  # Insert widgets

# Starting widgets for showing connected clients.
server_status_widget = Label(window, text="Server Started", font=("courier", 12))
server_stop_button = Button(window, text="Stop Server", command=stop_server, font=("courier", 12))
clients_status = Text(window)
send_message = Entry(window)
send_message_button = Button(window, text="     Send     ", command=send_message_to_client)

window.mainloop()
# window end
