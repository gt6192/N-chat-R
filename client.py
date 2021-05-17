import socket
from tkinter import *
import threading as td
import sys

# All required server and client info variables
HOST = ''  # host ip
PORT = ''  # host port
NAME = ''  # user defined client name
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket
server_name = ''
recv_status = True


def insert_starting_widgets():
    window.protocol("WM_DELETE_WINDOW", window_close)
    heading_side.grid(row=1, column=0, columnspan="2")
    entry_host_label.grid(row=2, column=0, padx=10)
    entry_host.grid(row=2, column=1, pady=10, padx=10)
    entry_port_label.grid(row=3, column=0, padx=10)
    entry_port.grid(row=3, column=1, pady=10, padx=10)
    entry_name_label.grid(row=4, column=0, padx=10)
    entry_name.grid(row=4, column=1, pady=10, padx=10)
    connect_server_button.grid(row=5, column=0, columnspan="2")
    warning_label.grid(row=6, column=0, columnspan="2", pady=5, padx=5)


def delete_starting_widgets():
    heading_side.grid_remove()
    entry_host_label.grid_remove()
    entry_host.grid_remove()
    entry_port_label.grid_remove()
    entry_port.grid_remove()
    entry_name_label.grid_remove()
    entry_name.grid_remove()
    connect_server_button.grid_remove()
    warning_label.grid_remove()


def showing_messages():
    window.protocol("WM_DELETE_WINDOW", window_close2)
    server_status_widget.grid(row=1, column=0)
    server_stop_button.grid(row=1, column=1)
    clients_status.grid(row=2, column=0, columnspan="2")
    send_message.grid(row=3, column=0, columnspan="2", pady=5)
    send_message_button.grid(row=4, column=0, columnspan="2", pady=5)


def delete_showing_messages():
    server_status_widget.grid_remove()
    clients_status.grid_remove()
    server_stop_button.grid_remove()
    send_message.grid_remove()
    send_message_button.grid_remove()


def connect_server():
    global HOST, PORT, NAME, server, server_name, recv_status
    recv_status = True
    HOST = entry_host.get()
    PORT = entry_port.get()
    NAME = entry_name.get()
    if len(HOST) <= 0 and len(PORT) <= 0 and len(NAME) <= 0:
        warning_label.config(text="You could not leave any field empty!", bg="yellow")
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server.connect((HOST, int(PORT)))
            msg = server.recv(1024).decode("utf-8")
            temp1 = msg.split()
            server_name = temp1[1]
            window.title(server_name)
            server.send(bytes(NAME, "utf-8"))
            delete_starting_widgets()
            showing_messages()
            td.Thread(target=receive_data).start()
        except:
            print(f"Host {HOST} using port {PORT} is refusing connection")
            connect_server_button.config(text="Retry")
            warning_label.config(text=f"Host {HOST} using port {PORT} is refusing connection", bg="yellow")


def disconnect():
    global recv_status
    recv_status = False
    server.send(bytes("exit", "utf-8"))
    server.close()
    delete_showing_messages()
    insert_starting_widgets()


def send_message_to_server():
    got_msg = send_message.get()
    final_msg = f"{NAME} > {got_msg}"
    server.send(bytes(final_msg, "utf-8"))
    send_message.delete(0, "end")
    if got_msg == "exit":
        server.close()
        delete_showing_messages()
        insert_starting_widgets()


def receive_data():
    while recv_status:
        try:
            client_message = server.recv(1024).decode("utf-8")
            if len(client_message) <= 0:
                temp = 0
            else:
                if client_message == "exit":
                    server.close()
                    print(f"server {server_name} Closed")
                    delete_showing_messages()
                    insert_starting_widgets()
                    return 0
                else:
                    clients_status.insert(INSERT, f"{client_message}\n")

        except:
            print(f"server {server_name} Closed")
            server.close()
            delete_showing_messages()
            insert_starting_widgets()
            return 0
    return 0


# window start
window = Tk()
window.title("Connect Server")


def window_close():
    global recv_status
    recv_status = False
    window.destroy()
    sys.exit(0)


def window_close2():
    global recv_status
    server.send(bytes("exit", "utf-8"))
    recv_status = False
    server.close()
    window.destroy()
    sys.exit(0)


# Starting widgets for get host, port and name.
# heading widget
heading = Label(window, text="N-CHAT R", font=("courier", 30))
heading_side = Label(window, text="Client", font=("courier", 15))

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
connect_server_button = Button(window, text="     Connect     ", command=connect_server, font=("courier", 12))

# Label to display error or success message
warning_label = Label(window, text="")

heading.grid(row=0, column=0, columnspan=2, pady=5)

insert_starting_widgets()  # Insert widgets

# Starting widgets for showing connected clients.
server_status_widget = Label(window, text="Server Started", font=("courier", 12))
server_stop_button = Button(window, text="Disconnect", command=disconnect, font=("courier", 12))
clients_status = Text(window)
send_message = Entry(window)
send_message_button = Button(window, text="     Send     ", command=send_message_to_server)

window.mainloop()
# window end
