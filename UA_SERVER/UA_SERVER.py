import sys

sys.path.insert(0, "..")
from opcua import ua, Server
from opcua.server.user_manager import UserManager
from opcua.ua import NodeIdType, NodeId
from log.LOGS import LOGS
from converter.UpdateEventHandle import get_ua_type
from threading import Timer


# from opc_server_security import OPC_SERVER_SECURITY
users_db = {
    'user1': 'pw1',
    'user2': 'pw2'
}


def user_manager(isession, username, password):
    isession.user = UserManager.User
    return username in users_db and password == users_db[username]


class UA_SERVER:
    def __init__(self, endpoint='opc.tcp://127.0.0.1:4850', name='GAZAUTO_DA_to_UA_converter',
                 namespace='GAZAUTO_DA_to_UA_converter'):
        print('UA server initialization...')
        self.endpoint = endpoint
        self.server_name = name

        self.server = Server()
        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)


        self.server.set_security_IDs(["Username"])
        self.server.user_manager.set_user_manager(user_manager)

        self.nmspc = self.server.register_namespace(namespace)
        self.objects = self.server.get_objects_node()

        # print(self.server.get_namespace_index(namespace))

        # Добавление мигающего бита (True/False) проверка раюоты сервера
        self.signal_point = self.objects.add_object(self.nmspc, 'Signal')
        self.signal_point_value = self.signal_point.add_variable(self.nmspc, "Status", True)

        self.MonitorList = {}

    def add_folder(self, folder_name, folder=None):
        if folder is None:
            return self.objects.add_folder(self.nmspc, folder_name)
        else:
            return folder.add_folder(self.nmspc, folder_name)

    def add_value(self, value, folder=None):
        nodeID = NodeId(identifier=value['Name'], namespaceidx=self.nmspc, nodeidtype=NodeIdType.String)
        if folder == None:
            self.MonitorList[value['Name']] = self.objects.add_variable(nodeid=nodeID,
                                                                        bname=value['Name'].replace(':', '.'),
                                                                        val=value['Value'],
                                                                        varianttype=get_ua_type(value['Value']))
        else:
            self.MonitorList[value['Name']] = folder.add_variable(nodeid=nodeID, bname=value['Name'].replace(':', '.'),
                                                                  val=value['Value'],
                                                                  varianttype=get_ua_type(value['Value']))

        return self.MonitorList[value['Name']]

    def signal(self):
        if self.signal_point_value.get_value():
            self.signal_point_value.set_value(False)
        else:
            self.signal_point_value.set_value(True)
        t = Timer(20, self.signal)
        t.start()

    def create_tree(self, tree_dict, folder=None):
        if folder == None:
            main_folder = self.objects.add_folder(self.nmspc, "DATA")
            self.create_tree(tree_dict, main_folder)
        else:
            for val in tree_dict:
                if val['Type'] == 'folder':
                    fl = self.add_folder(val['Name'], folder)
                    for leaf in val['LeafArray']:
                        self.add_value(leaf, fl)
                    self.create_tree(val['BrancheArray'], fl)
                else:
                    self.add_value(val, folder)

        return True

    def stop(self):
        LOGS('UA_SERVER', 'Stopping UA SERVER! UA_HOST: {}'.format(self.endpoint), 'INFO')
        self.server.stop()

    def start(self):
        self.signal()
        LOGS('UA_SERVER', 'Start UA SERVER! UA_HOST: {}'.format(self.endpoint), 'INFO')
        try:
            self.server.start()
            # print(self.server.get_namespace_array())
        except OSError as err:
            print('Error: ', err)
            LOGS('UA_SERVER', 'Error: Another converter may be working, or there is a problem with the port', 'ERROR')
            sys.exit()
