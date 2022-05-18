import sys
sys.path.insert(0, "..")
import logging
import time
import asyncio
from urllib.parse import urlparse

from opcua import Client
from opcua import ua

client = Client("opc.tcp://127.0.0.1:4851")
# client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
try:

    client.connect()
    client.find_servers()
    # client.activate_session(username='user1', password='pw1', certificate=None)
    print(client.find_servers())
    # _username = server_url.username
    # _password = server_url.password
    # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    root = client.get_root_node()
    print("Root node is: ", root)
    objects = client.get_objects_node()
    print("Objects node is: ", objects.get_browse_name().Name)

    # Node objects have methods to read and write node attributes as well as browse or populate address space
    print("Children of root are: ", root.get_children())
    for x in root.get_children():
        print(x.get_browse_name().Name)
    # asyncio.Server.sockets()
finally:
    client.disconnect()