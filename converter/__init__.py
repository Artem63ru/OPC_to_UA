from tkinter import *
import sys
import argparse
import xml.etree.ElementTree as ET


def get_config(configFile='cfg.xml'):
    tree = ET.parse(configFile)
    root = tree.getroot()
    res = {}
    for child in root:
        res[child.tag] = child.text

    return res


def run():
    _old_excepthook = sys.excepthook

    def end_program():
        sys.exit()

    def on_exit_by_ctrl_c(exctype, value, traceback):
        if exctype == KeyboardInterrupt:
            end_program()
        else:
            _old_excepthook(exctype, value, traceback)

    sys.excepthook = on_exit_by_ctrl_c


    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    # parser.add_argument("--m", default='savetags', help="Mode of work (config or other)")
    parser.add_argument("--m", default='config', help="Mode of work (config or other)")
    parser.add_argument("--dh", default='localhost', help="DA SERVER HOST")
    parser.add_argument("--dn", default='Matrikon.OPC.Simulation.1', help="DA SERVER NAME")
    parser.add_argument("--cfg", default='cfg.xml', help="Path of config file")

    args = parser.parse_args()

    if args.m=='config':
        from dcom_da.DA_CLIENT import DA_CLIENT
        from UA_SERVER.UA_SERVER import UA_SERVER
        from .UpdateEventHandle import UpdateEventHandler

        config = get_config(args.cfg)
        da_client = DA_CLIENT(host=config['DA_HOST'], server_name=config['DA_NAME'], file=config['FILENAME'],
                              sheet=config['SHEET'], MonitorHandler=UpdateEventHandler,
                              UpdateRate=config['UPDATE_RATE'], mode=config['MODE'])
        da_client.Connect()

        ua_serv = UA_SERVER(config['UA_HOST'], config['UA_SERVER_NAME'], config['UA_ROOT_NAMESPACE'])
        ua_serv.create_tree(da_client.GetTree())
        ua_serv.start()

        def handleInit(handle):
            handle.set_lists(dalist=da_client.monitorItemsID, ualist=ua_serv.MonitorList)

        da_client.FormMonitorItemList()
        da_client.StartMonitor(handleInit)



    elif args.m=='servlist':
        from dcom_da.regsvr import get_serv_list
        get_serv_list()
        sys.exit()
    elif args.m=='savetags':
        from dcom_da.DA_CLIENT import DA_CLIENT
        from .UpdateEventHandle import UpdateEventHandler
        # da_client=DA_CLIENT(host=args.dh, server_name=args.dn)
        config = get_config(args.cfg)
        da_client = DA_CLIENT(host=config['DA_HOST'], server_name=config['DA_NAME'], file=config['FILENAME'],
                              sheet=config['SHEET'], MonitorHandler=UpdateEventHandler,
                              UpdateRate=config['UPDATE_RATE'], mode=config['MODE'])
        da_client.Connect()
        da_client.GetTree()
        da_client.SaveMonitorItemList()
        da_client.Disconnect()

        sys.exit()
    elif args.m=='savetree':
        from dcom_da.DA_CLIENT import DA_CLIENT
        da_client = DA_CLIENT(host=args.dh, server_name=args.dn)
        da_client.Connect()
        da_client.GetTree()
        da_client.Disconnect()

        sys.exit()
    elif args.m=='reg':
        from dcom_da.regsvr import regsvr
        regsvr()

        sys.exit()







