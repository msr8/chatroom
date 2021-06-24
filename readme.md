# Modules required
<br>

Modules Required:
```
colorama
requests
```

To install these modules, type this in the command prompt/terminal (when the current directory is the folder contaning the files in this project):
```
pip install -r requirements.txt
```
(Replace `pip` with `pip3` if you are on MacOs or Linux)

<br>

# Configuration
## Port and disconnect command
<br>

By default, it is hosted on port `4280` and the disconnect message is `!disc`

Port in which the server is hosted can be changed by by changing line 9 in server.py ie `PORT = 4280`

Disconnect message/command can be changed by changing line 13 in clinet.py ie `DISC_MSG = '!disc'`

<br>

## Server ID
<br>

To join a server through the local host, the server id can be `[PORT]`,`loc[PORT]`, or `loc-[PORT]`. For example if I have hosted a server on port 660 on my localhost and trying to connect to it through the same localhost, the following server ids can get me connected to that server:
```
660
loc660
loc-660
```

<br>

To join a server hotsed on an india ngrok server, the server id can be `in[PORT]` or `in-[PORT]`. For example if I want to join the server with ip `0.tcp.in.ngrok.io` on port 5400, the following server ids can get me connected to that server:
```
in5400
in-5400
```

<br>

To join some other server, the server id would be `[SERVER IP]:[PORT]`. For example if I want to join a server with ip `2.tcp.ngrok.io` and port 8500, the following server id will get me connected to that server:
```
2.tcp.ngrok.io:8500
```

