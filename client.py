from colorama import init, Fore, Back, Style
import threading as thr
import requests as rq
import socket as soc
import time as t
import sys
init()


FORMAT = 'utf-8'
LIMIT = 999
VALID_CHARACTERS = 'qwertyuiopasdfghjklzxcvbnm1234567890_-'
DISC_MSG = '!disc'
IP = rq.get('https://api.ipify.org').text



def test_validity(name):
    ret = True
    # Checks if its in the length range
    if len(name) < 3 or len(name) > 20:
        ret = False
    # Checks if its all valid characters
    for i in name:
        if not i.lower() in VALID_CHARACTERS:
            ret = False
    return ret

def print_msges():
    while True:
        try:
            # Gets messages from the server and prints them
            to_print = server.recv(LIMIT).decode(FORMAT)
            if len(to_print):
                print(to_print)
            else:
                raise 'Some error came'
        # If any error is there, it stops the execution
        except:
            server.close()
            sys.exit()

def send_msg(message):
    try:
        server.send(message.encode(FORMAT))
    except:
        server.close()
        sys.exit()

def process_server_id(server_id):
    global SERVER_IP
    global PORT

    # Checks if its a local host
    if server_id.startswith('loc') or server_id[0].isnumeric():
        SERVER_IP = '127.0.0.1'

        if server_id[0].isnumeric():
            PORT = int(server_id)
        elif server_id.startswith('loc-'):
            PORT = int(server_id[4:])
        else:
            PORT = int(server_id[3:])


    # Checks if its an indian ngrok server
    if server_id.startswith('in'):
        SERVER_IP = '0.tcp.in.ngrok.io'

        if server_id.startswith('in-'):
            PORT = int(server_id[2:])
        else:
            PORT = int(server_id[2:])



# Defining the socket type
server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)



# Asks for name
valid_name = False
print(f'{Fore.BLUE}Welcome to Mark\'s Chatroom! Please enter your name to continue{Fore.RESET}\n\n{Fore.GREEN}Your name must be:\nAtleast 3 characters long and maximum 20 charcaters long\nMust not contain any special characters other than - and _{Fore.RESET}\n')
while not valid_name:
    name = input(f'{Fore.RED}Enter your name{Fore.RESET}\n')
    valid_name = test_validity(name)
    if not valid_name:
        print('\nInvalid name, please try again')

# Asks for server ID
server_id = input(f'{Fore.RED}Enter the server ID{Fore.RESET}\n')
server_id = server_id.lower()
process_server_id(server_id)
print('\n')





# Joins the server
server.connect((SERVER_IP, PORT))
thread_print_msges = thr.Thread(target = print_msges)
thread_print_msges.start()
# Sends the IP and name
send_msg(f'{IP}:{name}')


while True:
    to_send = input()
    if not to_send == DISC_MSG:
        send_msg(to_send)
    else:
        server.close()
        sys.exit()

