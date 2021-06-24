from colorama import init, Fore, Back, Style
import threading as thr
import socket as soc
import time as t
import os
init()

MY_IP = '127.0.0.1'
PORT = 4280
FORMAT = 'utf-8'
LIMIT = 999
LOG_FOLDER = os.path.join( os.path.dirname(__file__) , 'Logs' )
conn_list = []
conn_dict = {}

# Defining the socket type
server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
# Binding the socket to our IP Address
server.bind( (MY_IP, PORT) )

def send_msg_to_all(message):
    for i in conn_list:
        try:
            i.send(message.encode(FORMAT))
        except:
            continue

def get_names():
    ret = ''
    for i in conn_dict.keys():
        ret += conn_dict[i]['name'] + '  '
    return ret

def get_names_list():
    ret = []
    for i in conn_dict.keys():
        ret.append( conn_dict[i]['name'] )
    return ret

def log_write(to_write):
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(to_write)




def handle_client(conn, addr):
    # Adds the connection to the connection list
    conn_list.append(conn)
    is_connected = True
    # Gets the IP and name
    ip_and_name = conn.recv(LIMIT).decode(FORMAT)
    ip, name = ip_and_name.split(':')
    # Kicks if somebody with same name is in the server
    if name in get_names_list():
        conn.send(f'{Fore.RED}{Style.BRIGHT}Kicked because someone named {name} is already in the server{Style.RESET_ALL}'.encode(FORMAT))
        send_msg_to_all(f'{Fore.RED}{Style.BRIGHT}New {name} was kicked because someone named {name} is already in the server{Style.RESET_ALL}')
        log_write(f'New {name}:{ip}:{addr[1]} was kicked because someone named {name} is already in the server\n')
        conn.close()
        try:
            conn_list.remove(conn)
        except:
            pass
    # Adds the info to the dictionary
    conn_dict[conn] = {'ip': ip, 'name': name}
    # Prints info for who joined
    print(f'{Back.WHITE}{Fore.BLACK}{addr} {ip}:{name} joined. Current members: {Style.BRIGHT}{get_names()}{Style.RESET_ALL}')
    send_msg_to_all(f'{Back.WHITE}{Fore.BLACK}{name} joined. Current members: {Style.BRIGHT}{get_names()}{Style.RESET_ALL}')
    log_write(f'{addr} {ip}:{name} joined. Current members: {get_names()}\n')

    # Recieves message from client and processes it
    while is_connected:
        try:
            msg = conn.recv(LIMIT).decode(FORMAT)
            if len(msg):
                print(f'{Fore.CYAN}{name}: {msg}{Fore.RESET}')
                send_msg_to_all(f'{Fore.CYAN}{name}: {msg}{Fore.RESET}')
                log_write(f'{name}:{ip}:{addr[1]} : {msg}\n')
            else:
                raise 'Hello'
        # If theres an error, close connection
        except:
            try:
                conn.close()
            except:
                continue
            # Remove it from all the lists and dicts
            try:
                conn_list.remove(conn)
            except:
                continue
            conn_dict.pop(conn)
            # Send the leaving message
            print(f'{Back.WHITE}{Fore.BLACK}{addr} {ip}:{name} left. Current members: {Style.BRIGHT}{get_names()}{Style.RESET_ALL}')
            send_msg_to_all(f'{Back.WHITE}{Fore.BLACK}{name} left. Current members: {Style.BRIGHT}{get_names()}{Style.RESET_ALL}')
            log_write(f'{name}:{ip}:{addr} left. Current memebers: {get_names()}\n')
            break




# Makes log folder if not made
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)
# Speicifies log_file_path var
LOG_FILE_PATH = os.path.join( LOG_FOLDER , f'{int(t.time())}.txt' )


log_write(f'STARTING THE SERVER AT PORT {PORT}\n\n')
print(f'{Back.WHITE}{Fore.RED}{Style.BRIGHT}STARTING THE SERVER AT PORT {PORT}{Style.RESET_ALL}')
# Start listening for connections
server.listen()
# Accept all connections and always be listening for connections
while True:
    # Starts listening and accepting the connections
    connection, address = server.accept()
    thread_1 = thr.Thread(target = handle_client, args = (connection, address))
    thread_1.start()






# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL
