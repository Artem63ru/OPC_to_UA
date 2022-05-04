from tkinter import *
import sys
import argparse
import xml.etree.ElementTree as ET
from log.LOGS import LOGS
import sched, time
# import win32serviceutil
# import win32service
# import servicemanager

s = sched.scheduler(time.time, time.sleep)

#
# class MyService:
#     _svc_name_ = 'MyService'
#     _svc_display_name_ = 'My Service display name'
#
#     def __init__(self):
#         self.a = 0
#         self.tim = time.localtime()
#         self.running = None
#
#     def stop_service(self):
#         """Stop the service"""
#         self.running = False
#
#     def run_service(self):
#         """Main service loop. This is where work is done!"""
#         self.running = True
#         self.tim = time.localtime()
#         print('start сервиса', time.strftime("%H:%M:%S", self.tim))
#         run()
#
#
# class MyServiceFramework(win32serviceutil.ServiceFramework):
#     _svc_name_ = 'MyService'
#     _svc_display_name_ = 'My Service display name'
#
#     def SvcDoRun(self):
#         self.service_impl = MyService()
#         self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
#         self.ReportServiceStatus(win32service.SERVICE_RUNNING)
#         self.service_impl.run_service()
#
#     def SvcStop(self):
#         """Stop the service"""
#         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
#         self.service_impl.stop_service()
#         self.ReportServiceStatus(win32service.SERVICE_STOPPED)
#

def restart_connection(object_cl):
    s.enter(5, 1, restart_connection)
    print(object_cl.CheckConnected())


def get_config(configFile='cfg.xml'):
    tree = ET.parse(configFile)
    root = tree.getroot()
    res = {}
    for child in root:
        res[child.tag] = child.text

    return res
def intro():
    print('='*54)
    # for i in range(8):
    #     print('|',13*'\t','|')
    #     if i == 3:
    #         print('|', 4 * '\t' + '  Convertor, v.04.05 ' + str(4 * '\t'), '|')
        # if i == 7:
        #     print('|', 6 * '\t' + '  Gazpr', '|')
    print(5 * '\t' + ' Gazprom Auto')
    print( 4 * '\t' + '  Convertor, v.04.05 ' + str(4 * '\t'))

    print('=' * 54)

def run():
    LOGS('Converter/run', 'Run Convertor ', 'INFO')
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

    if args.m == 'config':
        from dcom_da.DA_CLIENT import DA_CLIENT
        from UA_SERVER.UA_SERVER import UA_SERVER
        from .UpdateEventHandle import UpdateEventHandler

        config = get_config(args.cfg)
        da_client = DA_CLIENT(host=config['DA_HOST'], server_name=config['DA_NAME'], file=config['FILENAME'],
                              sheet=config['SHEET'], MonitorHandler=UpdateEventHandler,
                              UpdateRate=config['UPDATE_RATE'], mode=config['MODE'])

        da_client.Connect()

        # print(da_client.CheckConnected())
        ua_serv = UA_SERVER(config['UA_HOST'], config['UA_SERVER_NAME'], config['UA_ROOT_NAMESPACE'])
        ua_serv.create_tree(da_client.GetTree())
        ua_serv.start()
        da_client.s.run()

        def handleInit(handle):
            handle.set_lists(dalist=da_client.monitorItemsID, ualist=ua_serv.MonitorList)

        da_client.FormMonitorItemList()
        da_client.StartMonitor(handleInit)



    elif args.m == 'servlist':
        from dcom_da.regsvr import get_serv_list
        get_serv_list()
        LOGS('main_servlist', 'Exiting the program', 'INFO')
        sys.exit()
    elif args.m == 'savetags':
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
        LOGS('main_savetags', 'Exiting the program', 'INFO')
        sys.exit()
    elif args.m == 'savetree':
        from dcom_da.DA_CLIENT import DA_CLIENT
        da_client = DA_CLIENT(host=args.dh, server_name=args.dn)
        da_client.Connect()
        da_client.GetTree()
        da_client.Disconnect()
        LOGS('main_savetree', 'Exiting the program', 'INFO')
        sys.exit()

    elif args.m == 'reg':
        from dcom_da.regsvr import regsvr
        regsvr()
        LOGS('main_reg', 'Exiting the program', 'INFO')
        sys.exit()

    # elif args.m == 'install':
    #     win32serviceutil.HandleCommandLine(MyService, argv=['--startup=auto', 'install'])
    #     sys.exit()